"""
Network Orchestrator
Central coordinator for multi-interface network detection and workflow management
"""

import threading
import time
import subprocess
import os
import json
from datetime import datetime
from enum import Enum

class NetworkState(Enum):
    """Network connection states"""
    NO_CONNECTION = "no_connection"
    ETH_CONNECTED = "eth_connected"
    WIFI_CONNECTED = "wifi_connected"
    BOTH_CONNECTED = "both_connected"

class ActiveTool(Enum):
    """Currently active tool"""
    NONE = "none"
    NETWORK_TOOLS_ETH = "network_tools_eth"
    NETWORK_TOOLS_WIFI = "network_tools_wifi"
    NET_TEST = "net_test"
    WIRELESS_TOOLS = "wireless_tools"

class NetworkOrchestrator:
    def __init__(self, socketio=None):
        self.socketio = socketio
        self.is_running = False
        self.check_interval = 3  # seconds
        
        # Interface states
        self.interfaces = {
            'eth0': {'state': False, 'ip': None, 'last_check': None},
            'wlan0': {'state': False, 'ip': None, 'ssid': None, 'last_check': None},
            'wlan1': {'state': False, 'ip': None, 'last_check': None}
        }
        
        # Current system state
        self.network_state = NetworkState.NO_CONNECTION
        self.active_tool = ActiveTool.NONE
        self.last_scanned_network = None
        
        # Callbacks for different workflows
        self.callbacks = {
            'eth_connected': None,
            'eth_disconnected': None,
            'wifi_connected': None,
            'wifi_disconnected': None,
            'no_connection': None,
            'tool_change': None
        }
        
        # Directories
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        os.makedirs(os.path.join(self.logs_dir, 'wifi'), exist_ok=True)
        os.makedirs(os.path.join(self.logs_dir, 'wireless'), exist_ok=True)
        
    def register_callback(self, event_name, callback):
        """Register a callback for specific events"""
        if event_name in self.callbacks:
            self.callbacks[event_name] = callback
            self.log(f"Registered callback for event: {event_name}")
        else:
            self.log(f"Warning: Unknown event name: {event_name}")
    
    def log(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[ORCHESTRATOR {timestamp}] {message}"
        print(log_entry)
        
        # Emit to dashboard
        if self.socketio:
            self.socketio.emit('orchestrator_log', {'message': message, 'timestamp': timestamp})
    
    def check_interface_state(self, interface_name):
        """Check if interface is up and has IP"""
        try:
            # Check if interface exists and is up
            operstate_path = f'/sys/class/net/{interface_name}/operstate'
            if not os.path.exists(operstate_path):
                return False, None
            
            with open(operstate_path, 'r') as f:
                state = f.read().strip()
                if state not in ['up', 'unknown']:
                    return False, None
            
            # Check for IP address
            result = subprocess.run(
                ['ip', 'addr', 'show', interface_name],
                capture_output=True, text=True, timeout=5
            )
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'inet ' in line and interface_name in result.stdout:
                        parts = line.strip().split()
                        if len(parts) >= 2:
                            ip_subnet = parts[1]
                            ip = ip_subnet.split('/')[0]
                            return True, ip
            
            return False, None
            
        except Exception as e:
            self.log(f"Error checking {interface_name}: {e}")
            return False, None
    
    def get_wifi_ssid(self, interface_name='wlan0'):
        """Get current WiFi SSID if connected"""
        try:
            # Try nmcli first
            result = subprocess.run(
                ['nmcli', '-t', '-f', 'active,ssid', 'dev', 'wifi'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line.startswith('yes:'):
                        return line.split(':', 1)[1].strip()
            
            # Fallback to iwgetid
            result = subprocess.run(
                ['iwgetid', interface_name, '-r'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
                
        except Exception as e:
            self.log(f"Error getting SSID: {e}")
        
        return None
    
    def get_network_info(self, interface_name):
        """Get detailed network information for an interface"""
        info = {
            'interface': interface_name,
            'ip': None,
            'subnet': None,
            'gateway': None,
            'dns': [],
            'ssid': None
        }
        
        # Get IP
        is_up, ip = self.check_interface_state(interface_name)
        if not is_up:
            return info
        
        info['ip'] = ip
        
        # Get subnet
        try:
            result = subprocess.run(
                ['ip', 'addr', 'show', interface_name],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'inet ' in line:
                        parts = line.strip().split()
                        if len(parts) >= 2:
                            info['subnet'] = parts[1]
                            break
        except Exception as e:
            self.log(f"Error getting subnet: {e}")
        
        # Get gateway
        try:
            result = subprocess.run(
                ['ip', 'route', 'show', 'default'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'default via' in line and interface_name in line:
                        parts = line.split()
                        if len(parts) >= 3:
                            info['gateway'] = parts[2]
                            break
        except Exception as e:
            self.log(f"Error getting gateway: {e}")
        
        # Get DNS
        try:
            with open('/etc/resolv.conf', 'r') as f:
                for line in f:
                    if line.startswith('nameserver'):
                        dns = line.split()[1]
                        info['dns'].append(dns)
        except Exception as e:
            self.log(f"Error getting DNS: {e}")
        
        # Get SSID for WiFi interfaces
        if interface_name.startswith('wlan'):
            info['ssid'] = self.get_wifi_ssid(interface_name)
        
        return info
    
    def update_interface_states(self):
        """Update state for all interfaces"""
        changes = []
        
        for interface_name in self.interfaces.keys():
            old_state = self.interfaces[interface_name]['state']
            old_ip = self.interfaces[interface_name]['ip']
            
            # Check current state
            is_up, ip = self.check_interface_state(interface_name)
            
            # Update state
            self.interfaces[interface_name]['state'] = is_up
            self.interfaces[interface_name]['ip'] = ip
            self.interfaces[interface_name]['last_check'] = datetime.now()
            
            # Get SSID for wlan0
            if interface_name == 'wlan0' and is_up:
                self.interfaces[interface_name]['ssid'] = self.get_wifi_ssid()
            
            # Detect changes
            if old_state != is_up or old_ip != ip:
                changes.append({
                    'interface': interface_name,
                    'old_state': old_state,
                    'new_state': is_up,
                    'old_ip': old_ip,
                    'new_ip': ip
                })
        
        return changes
    
    def determine_network_state(self):
        """Determine overall network state based on interface states"""
        eth0_up = self.interfaces['eth0']['state']
        wlan0_up = self.interfaces['wlan0']['state']
        
        if eth0_up and wlan0_up:
            return NetworkState.BOTH_CONNECTED
        elif eth0_up:
            return NetworkState.ETH_CONNECTED
        elif wlan0_up:
            return NetworkState.WIFI_CONNECTED
        else:
            return NetworkState.NO_CONNECTION
    
    def determine_active_tool(self):
        """
        Determine which tool should be active based on network state
        
        Priority:
        1. Ethernet → Network Tools (ETH)
        2. WiFi → Net Test → Network Tools (WiFi) or ISOLATED
        3. No connection → Wireless Tools
        """
        # Priority 1: Ethernet (most reliable)
        if self.interfaces['eth0']['state'] and self.interfaces['eth0']['ip']:
            return ActiveTool.NETWORK_TOOLS_ETH
        
        # Priority 2: WiFi connection
        elif self.interfaces['wlan0']['state'] and self.interfaces['wlan0']['ip']:
            # Net Test will determine if we should run Network Tools or not
            # For now, return NET_TEST - the callback will handle the decision
            return ActiveTool.NET_TEST
        
        # Priority 3: No connection
        else:
            return ActiveTool.WIRELESS_TOOLS
    
    def handle_tool_change(self, old_tool, new_tool):
        """Handle transition between tools"""
        if old_tool == new_tool:
            return  # No change
        
        self.log(f"Tool transition: {old_tool.value} → {new_tool.value}")
        
        # Stop old tool
        if old_tool == ActiveTool.NETWORK_TOOLS_ETH:
            if self.callbacks['eth_disconnected']:
                self.callbacks['eth_disconnected']()
        elif old_tool == ActiveTool.NETWORK_TOOLS_WIFI:
            if self.callbacks['wifi_disconnected']:
                self.callbacks['wifi_disconnected']()
        elif old_tool == ActiveTool.WIRELESS_TOOLS:
            # Will be handled by wireless_tools component
            pass
        
        # Start new tool
        if new_tool == ActiveTool.NETWORK_TOOLS_ETH:
            network_info = self.get_network_info('eth0')
            
            # Check if already scanned this network
            network_id = network_info.get('subnet', network_info['ip'])
            if self.last_scanned_network == network_id:
                self.log(f"Network {network_id} already scanned - skipping")
                return
            
            self.last_scanned_network = network_id
            
            if self.callbacks['eth_connected']:
                self.callbacks['eth_connected'](network_info)
            
        elif new_tool == ActiveTool.NET_TEST:
            network_info = self.get_network_info('wlan0')
            if self.callbacks['wifi_connected']:
                # wifi_connected callback will run Net Test
                self.callbacks['wifi_connected'](network_info)
                
        elif new_tool == ActiveTool.WIRELESS_TOOLS:
            if self.callbacks['no_connection']:
                self.callbacks['no_connection']()
        
        # Notify tool change
        if self.callbacks['tool_change']:
            self.callbacks['tool_change'](old_tool, new_tool)
        
        # Emit to dashboard
        if self.socketio:
            self.socketio.emit('active_tool_change', {
                'old_tool': old_tool.value,
                'new_tool': new_tool.value,
                'timestamp': datetime.now().isoformat()
            })
    
    def monitor_loop(self):
        """Main monitoring loop"""
        self.log("Network Orchestrator started - monitoring all interfaces")
        
        while self.is_running:
            try:
                # Update all interface states
                changes = self.update_interface_states()
                
                # Log any changes
                for change in changes:
                    iface = change['interface']
                    if change['new_state']:
                        self.log(f"{iface} CONNECTED - IP: {change['new_ip']}")
                    else:
                        self.log(f"{iface} DISCONNECTED")
                
                # Determine network state
                new_network_state = self.determine_network_state()
                if new_network_state != self.network_state:
                    self.log(f"Network state changed: {self.network_state.value} → {new_network_state.value}")
                    self.network_state = new_network_state
                
                # Determine which tool should be active
                new_active_tool = self.determine_active_tool()
                if new_active_tool != self.active_tool:
                    self.handle_tool_change(self.active_tool, new_active_tool)
                    self.active_tool = new_active_tool
                
                # Emit status update to dashboard
                if self.socketio:
                    self.socketio.emit('network_status', {
                        'interfaces': {
                            k: {'state': v['state'], 'ip': v['ip'], 'ssid': v.get('ssid')}
                            for k, v in self.interfaces.items()
                        },
                        'network_state': self.network_state.value,
                        'active_tool': self.active_tool.value,
                        'timestamp': datetime.now().isoformat()
                    })
                
                time.sleep(self.check_interval)
                
            except Exception as e:
                self.log(f"Error in monitor loop: {e}")
                time.sleep(self.check_interval)
    
    def start(self):
        """Start the orchestrator"""
        if not self.is_running:
            self.is_running = True
            self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
            self.monitor_thread.start()
            self.log("Network Orchestrator thread started")
    
    def stop(self):
        """Stop the orchestrator"""
        self.is_running = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=5)
        self.log("Network Orchestrator stopped")
    
    def get_status(self):
        """Get current status for API calls"""
        return {
            'interfaces': {
                k: {
                    'state': v['state'],
                    'ip': v['ip'],
                    'ssid': v.get('ssid'),
                    'last_check': v['last_check'].isoformat() if v['last_check'] else None
                }
                for k, v in self.interfaces.items()
            },
            'network_state': self.network_state.value,
            'active_tool': self.active_tool.value,
            'last_scanned_network': self.last_scanned_network
        }

# Global instance
network_orchestrator = NetworkOrchestrator()
