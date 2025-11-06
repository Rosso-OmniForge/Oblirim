from flask import Flask, render_template
from flask_socketio import SocketIO
import psutil
import socket
import subprocess
import time
import os
import json
from components.emotions import emotion_engine
from components.face_component import render_face_component, get_face_css
from components.system_specs_component import render_system_specs_component, get_specs_css

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

def get_pi_model():
    """Detect Raspberry Pi model"""
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('Model'):
                    return line.split(':')[1].strip()
        
        # Fallback method
        with open('/proc/device-tree/model', 'r') as f:
            return f.read().strip().replace('\x00', '')
    except:
        return "Unknown"

def get_system_info():
    try:
        # Get IP address - try multiple methods
        ip = "N/A"
        try:
            # Method 1: Connect to external server
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
        except:
            try:
                # Method 2: hostname resolution
                ip = socket.gethostbyname(socket.gethostname())
            except:
                pass

        # Check network interfaces
        wlan0_state = wlan1_state = eth0_state = "Down"
        bt_state = "N/A"

        try:
            result = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True, timeout=5)
            for line in result.stdout.splitlines():
                if 'wlan0:' in line and 'UP' in line:
                    wlan0_state = "Up"
                if 'wlan1:' in line and 'UP' in line:
                    wlan1_state = "Up"
                if 'eth0:' in line and 'UP' in line:
                    eth0_state = "Up"
        except Exception as e:
            print(f"Interface check error: {e}")

        # Check Bluetooth
        try:
            result = subprocess.run(['hciconfig'], capture_output=True, text=True, timeout=3)
            if result.returncode == 0 and 'UP RUNNING' in result.stdout:
                bt_state = "Up"
            elif result.returncode == 0:
                bt_state = "Down"
        except:
            pass

        # Get temperature - try multiple paths for different Pi models
        temp = "N/A"
        temp_paths = [
            '/sys/class/thermal/thermal_zone0/temp',
            '/opt/vc/bin/vcgencmd'
        ]
        
        for path in temp_paths:
            try:
                if path.endswith('vcgencmd'):
                    # Use vcgencmd for older Pi models
                    result = subprocess.run([path, 'measure_temp'], capture_output=True, text=True, timeout=3)
                    if result.returncode == 0:
                        temp_str = result.stdout.strip()
                        temp = temp_str.replace('temp=', '')
                        break
                else:
                    # Use thermal zone file
                    with open(path, 'r') as f:
                        temp_c = int(f.read().strip()) / 1000
                        temp = f"{temp_c:.1f}°C"
                        break
            except:
                continue

        # Get CPU usage
        cpu = psutil.cpu_percent(interval=1)

        # Get memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used = round(memory.used / (1024**3), 2)  # GB
        memory_total = round(memory.total / (1024**3), 2)  # GB

        # Get disk usage
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_used = round(disk.used / (1024**3), 2)  # GB
        disk_total = round(disk.total / (1024**3), 2)  # GB

        # Get Pi model
        pi_model = get_pi_model()

    except Exception as e:
        print(f"Error getting system info: {e}")
        # Return default values
        return {
            'ip': 'Error',
            'wlan0': 'Error',
            'wlan1': 'Error',
            'eth0': 'Error',
            'bluetooth': 'Error',
            'temperature': 'Error',
            'cpu': 'Error',
            'memory_percent': 'Error',
            'memory_usage': 'Error',
            'disk_percent': 'Error',
            'disk_usage': 'Error',
            'pi_model': 'Error'
        }

    return {
        'ip': ip,
        'wlan0': wlan0_state,
        'wlan1': wlan1_state,
        'eth0': eth0_state,
        'bluetooth': bt_state,
        'temperature': temp,
        'cpu': f"{cpu:.1f}%",
        'memory_percent': f"{memory_percent:.1f}%",
        'memory_usage': f"{memory_used:.2f}GB / {memory_total:.2f}GB",
        'disk_percent': f"{disk_percent:.1f}%",
        'disk_usage': f"{disk_used:.2f}GB / {disk_total:.2f}GB",
        'pi_model': pi_model,
        'emotion': emotion_engine.get_emotion({
            'cpu': f"{cpu:.1f}%",
            'temperature': temp,
            'memory_percent': f"{memory_percent:.1f}%"
        }),
        'ascii_face': emotion_engine.get_face(emotion_engine.get_emotion({
            'cpu': f"{cpu:.1f}%",
            'temperature': temp,
            'memory_percent': f"{memory_percent:.1f}%"
        }))
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/components/face')
def face_component():
    return render_face_component()

@app.route('/api/components/specs')
def specs_component():
    return render_system_specs_component()

@app.route('/api/css/face')
def face_css():
    return get_face_css(), 200, {'Content-Type': 'text/css'}

@app.route('/api/css/specs')
def specs_css():
    return get_specs_css(), 200, {'Content-Type': 'text/css'}

# Socket event handlers
@socketio.on('request_face_update')
def handle_face_update():
    """Send current face and emotion state"""
    data = get_system_info()
    emotion = emotion_engine.get_emotion({
        'cpu': data['cpu'],
        'temperature': data['temperature'],
        'memory_percent': data['memory_percent']
    })
    face = emotion_engine.get_face(emotion)
    
    socketio.emit('face_update', {
        'face': face,
        'emotion': emotion
    })

@socketio.on('run_script')
def handle_run_script(data):
    """Handle script execution requests"""
    script_name = data.get('script', 'example')
    try:
        # This is a placeholder - implement actual script running logic
        output = f"Running script: {script_name}\nScript executed successfully!"
        socketio.emit('script_output', {'output': output})
    except Exception as e:
        socketio.emit('script_output', {'error': str(e)})

@socketio.on('request_logs')
def handle_request_logs():
    """Handle log viewing requests"""
    try:
        # Read recent logs - adjust path as needed
        log_path = '/home/nero/dev/oblirim/logs/dashboard.log'
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                logs = f.read()[-2000:]  # Last 2000 characters
        else:
            logs = "No logs available"
        socketio.emit('log_data', logs)
    except Exception as e:
        socketio.emit('log_data', f"Error reading logs: {str(e)}")

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    # Send initial data
    data = get_system_info()
    socketio.emit('update_data', data)
    
    # Send initial face
    emotion = emotion_engine.get_emotion({
        'cpu': data['cpu'],
        'temperature': data['temperature'],
        'memory_percent': data['memory_percent']
    })
    face = emotion_engine.get_face(emotion)
    socketio.emit('face_update', {
        'face': face,
        'emotion': emotion
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

if __name__ == '__main__':
    import threading
    
    def background_thread():
        while True:
            time.sleep(2)
            data = get_system_info()
            socketio.emit('update_data', data)
            
            # Update face based on system state every 10 seconds
            if int(time.time()) % 10 == 0:
                emotion = emotion_engine.get_emotion({
                    'cpu': data['cpu'],
                    'temperature': data['temperature'],
                    'memory_percent': data['memory_percent']
                })
                face = emotion_engine.get_face(emotion)
                socketio.emit('face_update', {
                    'face': face,
                    'emotion': emotion
                })
    
    # Start background thread
    thread = threading.Thread(target=background_thread, daemon=True)
    thread.start()
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)