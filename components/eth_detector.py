"""
Ethernet Detection Daemon
Monitors eth0 connection state and triggers penetration testing workflows
"""

import threading
import time
import subprocess
import os
import json
from datetime import datetime
import logging

class EthernetDetector:
    def __init__(self, log_callback=None, workflow_callback=None, socketio=None):
        self.is_running = False
        self.last_state = None
        self.last_scanned_network = None  # Track last scanned network to avoid duplicates
        self.log_callback = log_callback
        self.workflow_callback = workflow_callback
        self.socketio = socketio
        self.check_interval = 3  # seconds
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        self.blocking_detected = False
        self.last_successful_check = None
        self.blocked_count = 0
        
        # Ensure directories exist
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        os.makedirs(os.path.join(self.logs_dir, 'eth'), exist_ok=True)
        
        # Initialize network tally
        self.network_tally_file = os.path.join(self.data_dir, 'network_tally.json')
        if not os.path.exists(self.network_tally_file):
            with open(self.network_tally_file, 'w') as f:
                json.dump({'total_networks': 0, 'last_updated': datetime.now().isoformat()}, f)

    def get_eth0_state(self):
        """Check if eth0 is connected using multiple methods for reliability"""
        try:
            # Method 1: Check carrier file (most direct)
            carrier_path = '/sys/class/net/eth0/carrier'
            if os.path.exists(carrier_path):
                try:
                    with open(carrier_path, 'r') as f:
                        carrier = f.read().strip()
                        if carrier == '1':
                            return True
                except (IOError, OSError):
                    # Carrier file exists but can't read - interface might be down
                    pass
            
            # Method 2: Check operstate file
            operstate_path = '/sys/class/net/eth0/operstate'
            if os.path.exists(operstate_path):
                with open(operstate_path, 'r') as f:
                    state = f.read().strip()
                    # 'up' means connected, 'unknown' can also mean up on some systems
                    if state == 'up':
                        return True
            
            # Method 3: Use ip link show as fallback
            result = subprocess.run(['ip', 'link', 'show', 'eth0'], 
                                  capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                output = result.stdout
                # Check for both UP (interface enabled) and LOWER_UP (link detected)
                if 'state UP' in output or ('LOWER_UP' in output and '<UP,' in output):
                    return True
            
            return False
        except (FileNotFoundError, IOError, OSError) as e:
            self.log(f"Error checking eth0 state: {e}")
            return False

    def get_eth0_info(self):
        """Get detailed eth0 interface information"""
        try:
            # Try to get state from operstate file first (most reliable)
            operstate_path = '/sys/class/net/eth0/operstate'
            if os.path.exists(operstate_path):
                with open(operstate_path, 'r') as f:
                    state = f.read().strip()
                    if state in ['up', 'unknown']:
                        return {'state': 'up', 'interface': 'eth0'}
                    else:
                        return {'state': 'down', 'interface': 'eth0'}
            
            # Fallback to ip link show
            result = subprocess.run(['ip', 'link', 'show', 'eth0'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'eth0:' in line or '<' in line:
                        # Extract state - check for UP and LOWER_UP
                        state = ('UP' in line or 'state UP' in line) and \
                               ('LOWER_UP' in line or 'state UP' in line)
                        return {
                            'state': 'up' if state else 'down',
                            'interface': 'eth0'
                        }
        except Exception as e:
            self.log(f"Error getting eth0 info: {e}")
        return {'state': 'unknown', 'interface': 'eth0'}

    def get_network_info(self):
        """Get IP, gateway, and network information"""
        info = {
            'ip': None,
            'subnet': None,
            'gateway': None,
            'dns': []
        }
        
        try:
            # Get IP and subnet
            result = subprocess.run(['ip', 'addr', 'show', 'eth0'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'inet ' in line and 'eth0' in line:
                        parts = line.strip().split()
                        if len(parts) >= 2:
                            ip_subnet = parts[1]
                            info['ip'] = ip_subnet.split('/')[0]
                            info['subnet'] = ip_subnet
                            break
        except Exception as e:
            self.log(f"Error getting IP info: {e}")

        try:
            # Get gateway
            result = subprocess.run(['ip', 'route', 'show', 'default'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'default via' in line and 'eth0' in line:
                        parts = line.split()
                        if len(parts) >= 3:
                            info['gateway'] = parts[2]
                            break
        except Exception as e:
            self.log(f"Error getting gateway info: {e}")

        try:
            # Get DNS servers
            with open('/etc/resolv.conf', 'r') as f:
                for line in f:
                    if line.startswith('nameserver'):
                        dns = line.split()[1]
                        info['dns'].append(dns)
        except Exception as e:
            self.log(f"Error getting DNS info: {e}")

        return info

    def increment_network_tally(self):
        """Increment the global network counter"""
        try:
            with open(self.network_tally_file, 'r') as f:
                data = json.load(f)
            
            data['total_networks'] += 1
            data['last_updated'] = datetime.now().isoformat()
            
            with open(self.network_tally_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            self.log(f"Network tally incremented to {data['total_networks']}")
        except Exception as e:
            self.log(f"Error updating network tally: {e}")

    def log(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        
        if self.log_callback:
            self.log_callback(log_entry)

    def log_to_readme(self, session_id, phase, details):
        """Append structured log to eth/README.md"""
        readme_path = os.path.join(self.logs_dir, 'eth', 'README.md')
        
        try:
            # Create file if it doesn't exist
            if not os.path.exists(readme_path):
                with open(readme_path, 'w') as f:
                    f.write("# Ethernet Penetration Testing Logs\n\n")
            
            # Append log entry
            with open(readme_path, 'a') as f:
                if phase == 'session_start':
                    f.write(f"## Session: {session_id}\n")
                elif phase == 'connected':
                    f.write(f"- **Connected:** {details}\n")
                elif phase == 'interface':
                    f.write(f"- **Interface:** {details}\n")
                elif phase == 'ip':
                    f.write(f"- **IP:** {details}\n")
                elif phase == 'gateway':
                    f.write(f"- **Gateway:** {details}\n")
                elif phase.startswith('phase'):
                    f.write(f"- **{phase.replace('_', ' ').title()}:** {details}\n")
                elif phase == 'disconnected':
                    f.write(f"- **Disconnected:** {details}\n")
                else:
                    f.write(f"- **{phase}:** {details}\n")
                f.write("\n")
                
        except Exception as e:
            self.log(f"Error writing to README: {e}")

    def trigger_connected_workflow(self):
        """Trigger the full Ethernet penetration testing workflow - ONLY when IP is assigned"""
        # Wait for IP assignment
        network_info = self.get_network_info()
        
        if not network_info or not network_info.get('ip'):
            self.log("Ethernet connected but waiting for IP assignment...")
            return
        
        # Check if we've already scanned this network in this session
        network_id = network_info.get('subnet', network_info['ip'])
        if self.last_scanned_network == network_id:
            self.log(f"Network {network_id} already scanned in this session - skipping")
            return
        
        self.last_scanned_network = network_id
        self.log(f"IP assigned: {network_info['ip']} - Starting penetration testing workflow")
        
        # Check for blocking first
        if self.check_for_blocking():
            self.log("Network blocking detected - workflow may be limited")
        
        if self.workflow_callback:
            self.workflow_callback('connected')
        else:
            self.log("No workflow callback defined - running basic detection")
            self.run_basic_detection()
        
        # Emit connection change to clients
        if self.socketio:
            self.socketio.emit('eth_connection_change', {'connected': True, 'ip': network_info['ip']})
            # Emit auto-scan started
            self.socketio.emit('eth_scan_started', {'status': 'auto', 'message': f"Auto-triggered for {network_info['ip']}"})
    
    def check_for_blocking(self):
        """Check if network operations are being blocked"""
        try:
            # Try a simple ping to gateway
            result = subprocess.run(['ping', '-c', '1', '-W', '2', '8.8.8.8'], 
                                  capture_output=True, timeout=3)
            if result.returncode == 0:
                self.last_successful_check = datetime.now()
                if self.blocking_detected:
                    self.log("Network blocking cleared")
                    self.blocking_detected = False
                    self.blocked_count = 0
                return False
            else:
                self.blocked_count += 1
                if self.blocked_count >= 3 and not self.blocking_detected:
                    self.blocking_detected = True
                    self.log("NETWORK BLOCKING DETECTED - Cannot reach external network")
                    self.log_to_readme('', 'blocked', f'Network blocking detected at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
                    
                    # Emit to clients
                    if self.socketio:
                        self.socketio.emit('network_blocked', {
                            'message': 'Network blocking detected',
                            'count': self.blocked_count,
                            'timestamp': datetime.now().isoformat()
                        })
                    return True
        except Exception as e:
            self.log(f"Error checking for blocking: {e}")
        return False

    def trigger_disconnected_workflow(self):
        """Trigger fallback/disconnected tools"""
        if self.workflow_callback:
            self.workflow_callback('disconnected')
        else:
            self.log("Ethernet disconnected - running fallback monitoring")

    def run_basic_detection(self):
        """Run basic network detection when connected"""
        try:
            network_info = self.get_network_info()
            if network_info['ip']:
                self.log(f"Network detected: {network_info['ip']}")
                self.increment_network_tally()
            else:
                self.log("Connected but no IP assigned yet")
        except Exception as e:
            self.log(f"Error in basic detection: {e}")

    def monitor_loop(self):
        """Main monitoring loop"""
        self.log("Starting eth0 monitor daemon...")
        
        while self.is_running:
            try:
                current_state = self.get_eth0_state()
                
                # State changed
                if current_state != self.last_state:
                    if current_state:
                        self.log("eth0 CONNECTED - Auto-triggering workflow")
                        self.trigger_connected_workflow()
                    else:
                        self.log("eth0 DISCONNECTED")
                        self.last_scanned_network = None  # Reset so we can scan again on reconnect
                        # Emit disconnection to clients
                        if self.socketio:
                            self.socketio.emit('eth_connection_change', {'connected': False})
                    
                    self.last_state = current_state
                
                # Periodically check for blocking if connected (every 5 loops = 15 seconds)
                if current_state and self.is_running:
                    if not hasattr(self, '_blocking_check_counter'):
                        self._blocking_check_counter = 0
                    self._blocking_check_counter += 1
                    
                    if self._blocking_check_counter >= 5:
                        self.check_for_blocking()
                        self._blocking_check_counter = 0
                
                time.sleep(3)  # Check every 3 seconds
                
            except Exception as e:
                self.log(f"Error in monitor loop: {e}")
                time.sleep(3)

    def start(self):
        """Start the detection daemon"""
        if not self.is_running:
            self.is_running = True
            self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
            self.monitor_thread.start()
            self.log("Ethernet detection daemon thread started")

    def stop(self):
        """Stop the detection daemon"""
        self.is_running = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=5)
        self.log("Ethernet detection daemon stopped")

# Global instance
eth_detector = EthernetDetector()