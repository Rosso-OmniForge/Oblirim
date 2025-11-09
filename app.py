from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import psutil
import socket
import subprocess
import time
import os
import json
import threading
from components.system_specs_component import render_system_specs_component, get_specs_css
from components.eth_detector import eth_detector
from components.eth_workflow import eth_workflow
from components.tab_logger import tab_logger
from components.network_metrics import network_metrics

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

def handle_eth_workflow(state):
    """Handle Ethernet state changes and trigger workflows"""
    if state == 'connected':
        # Get current network info
        network_info = eth_detector.get_network_info()
        if network_info['ip']:
            # Start workflow in background thread
            def run_workflow():
                eth_workflow.run_workflow(network_info)
            workflow_thread = threading.Thread(target=run_workflow, daemon=True)
            workflow_thread.start()
        else:
            print("Ethernet connected but no IP assigned yet")
    elif state == 'disconnected':
        print("Ethernet disconnected - running fallback monitoring")

def handle_workflow_progress(progress_data):
    """Handle workflow progress updates"""
    socketio.emit('eth_progress', progress_data)

# Initialize workflow callbacks
eth_workflow.add_progress_callback(handle_workflow_progress)
eth_detector.workflow_callback = handle_eth_workflow
eth_detector.socketio = socketio  # Pass socketio to detector for events

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

        # Check network interfaces - more robust detection
        wlan0_state = wlan1_state = eth0_state = "Down"
        bt_state = "N/A"

        def check_interface(interface_name):
            """Check if interface exists and is up using multiple methods"""
            try:
                # Method 1: Check operstate file (most reliable)
                operstate_path = f'/sys/class/net/{interface_name}/operstate'
                if os.path.exists(operstate_path):
                    with open(operstate_path, 'r') as f:
                        state = f.read().strip()
                        # 'up' or 'unknown' (unknown can mean up on some systems)
                        if state in ['up', 'unknown']:
                            return "Up"
                
                # Method 2: Check if interface exists and has carrier
                carrier_path = f'/sys/class/net/{interface_name}/carrier'
                if os.path.exists(carrier_path):
                    try:
                        with open(carrier_path, 'r') as f:
                            if f.read().strip() == '1':
                                return "Up"
                    except:
                        pass  # Carrier file not readable if interface is down
                
                # Method 3: Use ip link show (fallback)
                result = subprocess.run(['ip', 'link', 'show', interface_name], 
                                      capture_output=True, text=True, timeout=2)
                if result.returncode == 0:
                    output = result.stdout
                    # Check for UP state (interface enabled) and optionally LOWER_UP (link detected)
                    if 'state UP' in output or '<UP,' in output:
                        return "Up"
                
                return "Down"
            except Exception as e:
                print(f"Error checking {interface_name}: {e}")
                return "Down"

        try:
            wlan0_state = check_interface('wlan0')
            wlan1_state = check_interface('wlan1')
            eth0_state = check_interface('eth0')
        except Exception as e:
            print(f"Interface check error: {e}")

        # Check Bluetooth - more robust detection
        try:
            # Method 1: hciconfig
            result = subprocess.run(['hciconfig'], capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                if 'UP RUNNING' in result.stdout:
                    bt_state = "Up"
                elif 'hci0' in result.stdout or 'hci1' in result.stdout:
                    bt_state = "Down"
            
            # Method 2: Check via rfkill if hciconfig failed
            if bt_state == "N/A":
                result = subprocess.run(['rfkill', 'list', 'bluetooth'], 
                                      capture_output=True, text=True, timeout=3)
                if result.returncode == 0 and 'Soft blocked: no' in result.stdout:
                    bt_state = "Up"
                elif result.returncode == 0:
                    bt_state = "Down"
        except Exception as e:
            print(f"Bluetooth check error: {e}")

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
        'pi_model': pi_model
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/components/specs')
def specs_component():
    return render_system_specs_component()

@app.route('/api/css/specs')
def specs_css():
    return get_specs_css(), 200, {'Content-Type': 'text/css'}

@app.route('/api/eth/status')
def eth_status():
    """Get Ethernet connection status"""
    try:
        status = eth_detector.get_eth0_state()
        network_info = eth_detector.get_network_info() if status else {}
        return {
            'connected': status,
            'ip': network_info.get('ip'),
            'gateway': network_info.get('gateway'),
            'subnet': network_info.get('subnet')
        }
    except Exception as e:
        return {'connected': False, 'error': str(e)}

@app.route('/api/network/tally')
def get_network_tally():
    """Get the network tally count"""
    try:
        tally_file = os.path.join(os.path.dirname(__file__), 'data', 'network_tally.json')
        if os.path.exists(tally_file):
            with open(tally_file, 'r') as f:
                return json.load(f)
        return {'total_networks': 0, 'last_updated': None}
    except Exception as e:
        return {'error': str(e)}

@app.route('/api/eth/metrics')
def get_eth_metrics():
    """Get current Ethernet network metrics"""
    try:
        # Get current network info
        network_info = eth_detector.get_network_info()
        if network_info.get('subnet'):
            # Calculate network range
            subnet_parts = network_info['subnet'].split('/')
            if len(subnet_parts) == 2:
                ip_addr = subnet_parts[0]
                cidr = subnet_parts[1]
                ip_parts = ip_addr.split('.')
                if len(ip_parts) == 4:
                    network_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/{cidr}"
                    metrics = network_metrics.get_network_metrics(network_range)
                    return jsonify(metrics)
        
        # Return empty metrics if no network
        return jsonify({
            'current': {'hosts': 0, 'ports': 0, 'vulnerabilities': 0, 'devices': 0},
            'historical': {'hosts': 0, 'ports': 0, 'vulnerabilities': 0, 'scans': 0},
            'metadata': {'first_seen': None, 'last_scan': None, 'scan_count': 0}
        })
    except Exception as e:
        return jsonify({'error': str(e)})

# Socket event handlers
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

@socketio.on('request_eth_logs')
def handle_request_eth_logs():
    """Handle Ethernet log viewing requests"""
    try:
        logs = tab_logger.get_recent_logs('eth', 100)
        socketio.emit('eth_log_data', logs)
    except Exception as e:
        socketio.emit('eth_log_data', f"Error reading ETH logs: {str(e)}")

@socketio.on('start_eth_scan')
def handle_start_eth_scan():
    """Handle manual Ethernet scan requests"""
    try:
        network_info = eth_detector.get_network_info()
        if network_info['ip']:
            def run_manual_workflow():
                eth_workflow.run_workflow(network_info)
            workflow_thread = threading.Thread(target=run_manual_workflow, daemon=True)
            workflow_thread.start()
            socketio.emit('eth_scan_started', {'status': 'started', 'message': 'Manual scan initiated'})
        else:
            socketio.emit('eth_scan_started', {'status': 'error', 'message': 'No Ethernet connection'})
    except Exception as e:
        socketio.emit('eth_scan_started', {'status': 'error', 'message': str(e)})

@socketio.on('stop_eth_scan')
def handle_stop_eth_scan():
    """Handle stop Ethernet scan requests"""
    try:
        # Stop the workflow
        eth_workflow.stop_workflow()
        # Log the stop event
        tab_logger.log_event('eth', 'Scan stopped by user')
        socketio.emit('eth_scan_stopped', {'status': 'stopped', 'message': 'Scan stopped successfully'})
    except Exception as e:
        socketio.emit('eth_scan_stopped', {'status': 'error', 'message': str(e)})

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    # Send initial data
    data = get_system_info()
    socketio.emit('update_data', data)
    
    # If a scan is running, send current progress
    if eth_workflow.is_running:
        socketio.emit('eth_scan_started', {'status': 'running', 'message': 'Scan in progress'})
        # Send current phase info if available
        if hasattr(eth_workflow, 'current_phase'):
            socketio.emit('eth_progress', eth_workflow.current_phase)

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

if __name__ == '__main__':
    import threading
    
    # Print startup banner
    print("\n" + "="*60)
    print(r"  ___  ____  _     ___ ____  ___ __  __ ")
    print(r" / _ \| __ )| |   |_ _|  _ \|_ _|  \/  |")
    print(r"| | | |  _ \| |    | || |_) || || |\/| |")
    print(r"| |_| | |_) | |___ | ||  _ < | || |  | |")
    print(r" \___/|____/|_____|___|_| \_\___|_|  |_|")
    print("\n  Ethernet Penetration Testing Interface")
    print("    FOR TESTING ONLY - NOT A FUCKING TOY ")
    print("="*60)
    print(" Starting Ethernet Detection Daemon...")
    print(" Starting Flask-SocketIO Server...")
    print("\n" + "="*60 + "\n")
    
    def background_thread():
        while True:
            time.sleep(2)
            data = get_system_info()
            socketio.emit('update_data', data)
    
    # Start background thread
    thread = threading.Thread(target=background_thread, daemon=True)
    thread.start()
    
    # Start Ethernet detector
    eth_detector.start()
    
    # Determine host to bind to
    # Prefer Bluetooth PAN interface (bnep0) if available, otherwise bind to localhost
    # This restricts web UI access to only Bluetooth PAN connections
    bind_host = '127.0.0.1'  # Default to localhost (for TUI access)
    bind_message = "localhost only (TUI access)"
    
    try:
        # Check if Bluetooth PAN interface exists and is up
        bnep_path = '/sys/class/net/bnep0/operstate'
        if os.path.exists(bnep_path):
            with open(bnep_path, 'r') as f:
                if f.read().strip() == 'up':
                    # Get bnep0 IP address
                    import netifaces
                    if 'bnep0' in netifaces.interfaces():
                        addrs = netifaces.ifaddresses('bnep0')
                        if netifaces.AF_INET in addrs:
                            bind_host = addrs[netifaces.AF_INET][0]['addr']
                            bind_message = f"Bluetooth PAN ({bind_host})"
    except Exception as e:
        print(f"Note: Bluetooth PAN interface not available, binding to localhost: {e}")
    
    print(f" Server starting on http://{bind_host}:5000")
    print(f" Web UI accessible via: {bind_message}")
    print(" Dashboard ready!")
    print("\n" + "="*60 + "\n")
    
    # Bind to determined host (bnep0 IP or localhost)
    # This ensures Web UI is only accessible via Bluetooth PAN when connected
    # or localhost for TUI access
    socketio.run(app, host=bind_host, port=5000, debug=False, allow_unsafe_werkzeug=True)