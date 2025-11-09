"""
Wireless Tools - WiFi Scanning, Wardriving, and Open Network Hunter
Scans for WiFi networks, auto-connects to open networks, and performs wardriving captures
"""

import subprocess
import threading
import time
import json
import os
from datetime import datetime
from collections import defaultdict

class WirelessTools:
    def __init__(self, socketio=None):
        self.socketio = socketio
        self.is_running = False
        self.is_scanning = False
        self.stop_requested = False
        
        # Configuration
        self.scan_interval = 30  # seconds between scans
        self.auto_connect_enabled = True
        self.max_connection_attempts = 3
        
        # Blacklist for networks to never connect to
        self.blacklist = [
            'xfinitywifi', 'attwifi', 'optimumwifi', 'spectrumwifi',
            'comcast', 'cablewifi', '_nomap'
        ]
        
        # Whitelist (if not empty, only connect to these)
        self.whitelist = []
        
        # Directories
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(os.path.join(self.logs_dir, 'wireless'), exist_ok=True)
        
        # Wardrive database
        self.wardrive_db = os.path.join(self.data_dir, 'wardrive.json')
        if not os.path.exists(self.wardrive_db):
            with open(self.wardrive_db, 'w') as f:
                json.dump({'networks': {}, 'metadata': {'total_scans': 0, 'last_scan': None}}, f)
        
        # Connection history
        self.connection_history = []
        self.attempted_networks = set()
        
        # Callbacks
        self.on_open_network_found = None
        self.on_connection_success = None
        self.on_connection_failed = None
    
    def log(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[WIRELESS_TOOLS {timestamp}] {message}"
        print(log_entry)
        
        # Emit to dashboard
        if self.socketio:
            self.socketio.emit('wireless_tools_log', {'message': message, 'timestamp': timestamp})
    
    def scan_wifi_networks(self, interface='wlan0'):
        """
        Scan for WiFi networks using nmcli
        Returns list of networks with details
        """
        self.log(f"Scanning for WiFi networks on {interface}...")
        
        networks = []
        
        try:
            # Use nmcli for scanning
            # First, rescan
            subprocess.run(['nmcli', 'device', 'wifi', 'rescan'], 
                         capture_output=True, timeout=10)
            time.sleep(2)  # Wait for scan to complete
            
            # Get scan results
            result = subprocess.run(
                ['nmcli', '-t', '-f', 
                 'SSID,BSSID,CHAN,SIGNAL,SECURITY', 
                 'device', 'wifi', 'list'],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if not line:
                        continue
                    
                    parts = line.split(':')
                    if len(parts) >= 5:
                        ssid = parts[0]
                        bssid = parts[1]
                        channel = parts[2]
                        signal = parts[3]
                        security = parts[4]
                        
                        # Skip hidden networks (no SSID)
                        if not ssid or ssid == '--':
                            continue
                        
                        network = {
                            'ssid': ssid,
                            'bssid': bssid,
                            'channel': channel,
                            'signal': int(signal) if signal.lstrip('-').isdigit() else -100,
                            'security': security,
                            'is_open': security == '' or security == '--',
                            'timestamp': datetime.now().isoformat()
                        }
                        
                        networks.append(network)
                
                self.log(f"✓ Found {len(networks)} networks")
            else:
                self.log(f"nmcli scan failed: {result.stderr}")
                
        except FileNotFoundError:
            self.log("nmcli not found - trying iwlist...")
            # Fallback to iwlist
            try:
                result = subprocess.run(
                    ['sudo', 'iwlist', interface, 'scan'],
                    capture_output=True, text=True, timeout=30
                )
                
                if result.returncode == 0:
                    # Parse iwlist output (more complex)
                    networks = self._parse_iwlist_output(result.stdout)
                    self.log(f"✓ Found {len(networks)} networks (iwlist)")
                else:
                    self.log("iwlist scan failed - may need root privileges")
            except Exception as e:
                self.log(f"iwlist error: {e}")
        
        except Exception as e:
            self.log(f"Scan error: {e}")
        
        return networks
    
    def _parse_iwlist_output(self, output):
        """Parse iwlist scan output"""
        networks = []
        current_network = {}
        
        for line in output.split('\n'):
            line = line.strip()
            
            if 'Cell' in line and 'Address:' in line:
                if current_network:
                    networks.append(current_network)
                current_network = {
                    'bssid': line.split('Address:')[1].strip(),
                    'timestamp': datetime.now().isoformat()
                }
            elif 'ESSID:' in line:
                ssid = line.split('ESSID:')[1].strip().strip('"')
                current_network['ssid'] = ssid
            elif 'Channel:' in line:
                current_network['channel'] = line.split('Channel:')[1].strip()
            elif 'Signal level=' in line:
                try:
                    signal = line.split('Signal level=')[1].split()[0]
                    current_network['signal'] = int(signal)
                except:
                    current_network['signal'] = -100
            elif 'Encryption key:off' in line:
                current_network['is_open'] = True
                current_network['security'] = ''
            elif 'Encryption key:on' in line:
                current_network['is_open'] = False
                current_network['security'] = 'WPA/WPA2'
        
        if current_network:
            networks.append(current_network)
        
        return networks
    
    def filter_open_networks(self, networks):
        """Filter for open networks, apply whitelist/blacklist"""
        open_networks = [n for n in networks if n.get('is_open', False)]
        
        # Apply blacklist
        filtered = []
        for network in open_networks:
            ssid = network['ssid'].lower()
            
            # Check blacklist
            if any(blocked in ssid for blocked in self.blacklist):
                self.log(f"⊗ Skipping blacklisted network: {network['ssid']}")
                continue
            
            # Check whitelist (if defined)
            if self.whitelist:
                if not any(allowed in ssid for allowed in self.whitelist):
                    self.log(f"⊗ Skipping non-whitelisted network: {network['ssid']}")
                    continue
            
            filtered.append(network)
        
        # Sort by signal strength (strongest first)
        filtered.sort(key=lambda x: x['signal'], reverse=True)
        
        return filtered
    
    def connect_to_network(self, ssid, interface='wlan0'):
        """
        Attempt to connect to an open WiFi network
        Returns (success, ip_address)
        """
        self.log(f"Attempting to connect to: {ssid}")
        
        try:
            # Disconnect from current network first
            subprocess.run(['nmcli', 'device', 'disconnect', interface],
                         capture_output=True, timeout=5)
            time.sleep(1)
            
            # Connect to network
            result = subprocess.run(
                ['nmcli', 'device', 'wifi', 'connect', ssid, 'ifname', interface],
                capture_output=True, text=True, timeout=30
            )
            
            if result.returncode == 0:
                # Wait for IP assignment
                for i in range(10):
                    time.sleep(1)
                    ip = self._get_interface_ip(interface)
                    if ip:
                        self.log(f"✓ Connected to {ssid} - IP: {ip}")
                        
                        # Log connection
                        self.connection_history.append({
                            'ssid': ssid,
                            'timestamp': datetime.now().isoformat(),
                            'success': True,
                            'ip': ip
                        })
                        
                        if self.on_connection_success:
                            self.on_connection_success(ssid, ip)
                        
                        return True, ip
                
                self.log(f"✗ Connected to {ssid} but no IP assigned")
                return False, None
            else:
                self.log(f"✗ Failed to connect to {ssid}: {result.stderr}")
                
                # Log failed attempt
                self.connection_history.append({
                    'ssid': ssid,
                    'timestamp': datetime.now().isoformat(),
                    'success': False,
                    'error': result.stderr
                })
                
                if self.on_connection_failed:
                    self.on_connection_failed(ssid, result.stderr)
                
                return False, None
                
        except Exception as e:
            self.log(f"Connection error: {e}")
            return False, None
    
    def _get_interface_ip(self, interface):
        """Get IP address of interface"""
        try:
            result = subprocess.run(
                ['ip', 'addr', 'show', interface],
                capture_output=True, text=True, timeout=5
            )
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'inet ' in line:
                        parts = line.strip().split()
                        if len(parts) >= 2:
                            return parts[1].split('/')[0]
        except:
            pass
        return None
    
    def update_wardrive_database(self, networks):
        """Update wardrive database with discovered networks"""
        try:
            with open(self.wardrive_db, 'r') as f:
                db = json.load(f)
            
            # Update networks
            for network in networks:
                bssid = network['bssid']
                
                if bssid not in db['networks']:
                    # New network
                    db['networks'][bssid] = {
                        'ssid': network['ssid'],
                        'bssid': bssid,
                        'first_seen': network['timestamp'],
                        'last_seen': network['timestamp'],
                        'channel': network.get('channel'),
                        'security': network.get('security', ''),
                        'is_open': network.get('is_open', False),
                        'times_seen': 1,
                        'best_signal': network['signal']
                    }
                else:
                    # Update existing
                    db['networks'][bssid]['last_seen'] = network['timestamp']
                    db['networks'][bssid]['times_seen'] += 1
                    
                    # Update best signal if stronger
                    if network['signal'] > db['networks'][bssid].get('best_signal', -100):
                        db['networks'][bssid]['best_signal'] = network['signal']
            
            # Update metadata
            db['metadata']['total_scans'] += 1
            db['metadata']['last_scan'] = datetime.now().isoformat()
            db['metadata']['total_networks'] = len(db['networks'])
            
            # Save
            with open(self.wardrive_db, 'w') as f:
                json.dump(db, f, indent=2)
            
            self.log(f"Wardrive DB updated: {len(db['networks'])} total networks")
            
        except Exception as e:
            self.log(f"Error updating wardrive DB: {e}")
    
    def open_network_hunter_mode(self):
        """
        Mode A: Scan for open networks and auto-connect
        """
        self.log("=== Open Network Hunter Mode ===")
        
        while self.is_running and not self.stop_requested:
            # Scan for networks
            networks = self.scan_wifi_networks()
            
            if not networks:
                self.log("No networks found - retrying in 30s")
                time.sleep(30)
                continue
            
            # Update wardrive database
            self.update_wardrive_database(networks)
            
            # Filter for open networks
            open_networks = self.filter_open_networks(networks)
            
            if not open_networks:
                self.log(f"No open networks found ({len(networks)} total networks scanned)")
                
                # Emit status
                if self.socketio:
                    self.socketio.emit('wireless_scan_complete', {
                        'total_networks': len(networks),
                        'open_networks': 0,
                        'timestamp': datetime.now().isoformat()
                    })
                
                time.sleep(self.scan_interval)
                continue
            
            self.log(f"✓ Found {len(open_networks)} open networks")
            
            # Emit open networks to dashboard
            if self.socketio:
                self.socketio.emit('open_networks_found', {
                    'count': len(open_networks),
                    'networks': open_networks[:5],  # Send top 5
                    'timestamp': datetime.now().isoformat()
                })
            
            # Try to connect to each open network (if not already attempted)
            if self.auto_connect_enabled:
                for network in open_networks:
                    if self.stop_requested:
                        break
                    
                    ssid = network['ssid']
                    
                    # Skip if already attempted
                    if ssid in self.attempted_networks:
                        self.log(f"Already attempted {ssid} - skipping")
                        continue
                    
                    self.attempted_networks.add(ssid)
                    
                    # Notify callback
                    if self.on_open_network_found:
                        self.on_open_network_found(network)
                    
                    # Attempt connection
                    success, ip = self.connect_to_network(ssid)
                    
                    if success:
                        self.log(f"✓ Successfully connected to {ssid}")
                        # Network orchestrator will handle the rest (Net Test, etc.)
                        return  # Exit scanning mode
                    else:
                        self.log(f"✗ Failed to connect to {ssid}")
            
            # Wait before next scan
            if not self.stop_requested:
                time.sleep(self.scan_interval)
    
    def passive_wardriving_mode(self):
        """
        Mode B: Passive scanning and logging (no connections)
        """
        self.log("=== Passive Wardriving Mode ===")
        
        while self.is_running and not self.stop_requested:
            # Scan for networks
            networks = self.scan_wifi_networks()
            
            if networks:
                self.update_wardrive_database(networks)
                
                # Log summary
                open_count = sum(1 for n in networks if n.get('is_open', False))
                self.log(f"Logged {len(networks)} networks ({open_count} open)")
                
                # Emit to dashboard
                if self.socketio:
                    self.socketio.emit('wardrive_update', {
                        'total': len(networks),
                        'open': open_count,
                        'timestamp': datetime.now().isoformat()
                    })
            
            time.sleep(self.scan_interval)
    
    def start(self, mode='hunter'):
        """
        Start wireless tools
        Modes: 'hunter' (auto-connect) or 'passive' (just scan)
        """
        if self.is_running:
            self.log("Wireless tools already running")
            return
        
        self.is_running = True
        self.stop_requested = False
        self.attempted_networks.clear()  # Reset attempted networks
        
        if mode == 'hunter':
            self.log("Starting in Open Network Hunter mode")
            self.scan_thread = threading.Thread(
                target=self.open_network_hunter_mode,
                daemon=True
            )
        else:
            self.log("Starting in Passive Wardriving mode")
            self.scan_thread = threading.Thread(
                target=self.passive_wardriving_mode,
                daemon=True
            )
        
        self.scan_thread.start()
    
    def stop(self):
        """Stop wireless tools"""
        if self.is_running:
            self.log("Stopping wireless tools...")
            self.stop_requested = True
            self.is_running = False
            
            if hasattr(self, 'scan_thread'):
                self.scan_thread.join(timeout=5)
            
            self.log("Wireless tools stopped")
    
    def get_wardrive_stats(self):
        """Get wardrive database statistics"""
        try:
            with open(self.wardrive_db, 'r') as f:
                db = json.load(f)
            
            total_networks = len(db['networks'])
            open_networks = sum(1 for n in db['networks'].values() if n.get('is_open', False))
            
            return {
                'total_networks': total_networks,
                'open_networks': open_networks,
                'total_scans': db['metadata'].get('total_scans', 0),
                'last_scan': db['metadata'].get('last_scan'),
                'connection_attempts': len(self.connection_history),
                'successful_connections': sum(1 for c in self.connection_history if c['success'])
            }
        except:
            return {
                'total_networks': 0,
                'open_networks': 0,
                'total_scans': 0,
                'last_scan': None,
                'connection_attempts': 0,
                'successful_connections': 0
            }

# Global instance
wireless_tools = WirelessTools()
