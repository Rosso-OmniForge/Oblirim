"""
Network Metrics Tracker
Stores and aggregates penetration testing metrics per network with historical data
"""

import json
import os
from datetime import datetime
from typing import Dict, Any

class NetworkMetrics:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.metrics_file = os.path.join(self.data_dir, 'network_metrics.json')
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize or load metrics
        self.metrics = self._load_metrics()
    
    def _load_metrics(self) -> Dict:
        """Load metrics from disk"""
        if os.path.exists(self.metrics_file):
            try:
                with open(self.metrics_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'networks': {},  # Per-network metrics
            'global': {      # Global totals
                'total_networks_scanned': 0,
                'total_hosts_found': 0,
                'total_ports_found': 0,
                'total_vulnerabilities': 0,
                'last_updated': None
            }
        }
    
    def _save_metrics(self):
        """Save metrics to disk"""
        try:
            with open(self.metrics_file, 'w') as f:
                json.dump(self.metrics, f, indent=2)
        except Exception as e:
            print(f"Error saving metrics: {e}")
    
    def get_network_key(self, network_range: str) -> str:
        """Get normalized network key (e.g., 10.0.5.0/24)"""
        return network_range.strip()
    
    def init_network(self, network_range: str):
        """Initialize a new network in metrics"""
        key = self.get_network_key(network_range)
        if key not in self.metrics['networks']:
            self.metrics['networks'][key] = {
                'first_seen': datetime.now().isoformat(),
                'last_scan': None,
                'scan_count': 0,
                'current_session': {
                    'hosts': 0,
                    'ports': 0,
                    'vulnerabilities': 0,
                    'devices': {}
                },
                'historical': {
                    'total_hosts': 0,
                    'total_ports': 0,
                    'total_vulnerabilities': 0,
                    'total_scans': 0
                }
            }
            self.metrics['global']['total_networks_scanned'] += 1
            self._save_metrics()
    
    def update_current_session(self, network_range: str, hosts: int = 0, ports: int = 0, 
                              vulnerabilities: int = 0, device: str = None):
        """Update current session metrics"""
        key = self.get_network_key(network_range)
        self.init_network(network_range)
        
        net = self.metrics['networks'][key]
        
        # Update current session
        if hosts > 0:
            net['current_session']['hosts'] = hosts
        if ports > 0:
            net['current_session']['ports'] += ports
        if vulnerabilities > 0:
            net['current_session']['vulnerabilities'] += vulnerabilities
        if device:
            net['current_session']['devices'][device] = {
                'last_seen': datetime.now().isoformat()
            }
        
        net['last_scan'] = datetime.now().isoformat()
        self._save_metrics()
    
    def finalize_session(self, network_range: str):
        """Move current session data to historical and reset current"""
        key = self.get_network_key(network_range)
        if key not in self.metrics['networks']:
            return
        
        net = self.metrics['networks'][key]
        current = net['current_session']
        
        # Add to historical
        net['historical']['total_hosts'] += current['hosts']
        net['historical']['total_ports'] += current['ports']
        net['historical']['total_vulnerabilities'] += current['vulnerabilities']
        net['historical']['total_scans'] += 1
        net['scan_count'] += 1
        
        # Update global totals
        self.metrics['global']['total_hosts_found'] += current['hosts']
        self.metrics['global']['total_ports_found'] += current['ports']
        self.metrics['global']['total_vulnerabilities'] += current['vulnerabilities']
        self.metrics['global']['last_updated'] = datetime.now().isoformat()
        
        # Reset current session
        net['current_session'] = {
            'hosts': 0,
            'ports': 0,
            'vulnerabilities': 0,
            'devices': {}
        }
        
        self._save_metrics()
    
    def get_network_metrics(self, network_range: str) -> Dict[str, Any]:
        """Get metrics for a specific network"""
        key = self.get_network_key(network_range)
        if key not in self.metrics['networks']:
            self.init_network(network_range)
        
        net = self.metrics['networks'][key]
        current = net['current_session']
        historical = net['historical']
        
        return {
            'current': {
                'hosts': current['hosts'],
                'ports': current['ports'],
                'vulnerabilities': current['vulnerabilities'],
                'devices': len(current['devices'])
            },
            'historical': {
                'hosts': historical['total_hosts'],
                'ports': historical['total_ports'],
                'vulnerabilities': historical['total_vulnerabilities'],
                'scans': historical['total_scans']
            },
            'metadata': {
                'first_seen': net['first_seen'],
                'last_scan': net['last_scan'],
                'scan_count': net['scan_count']
            }
        }
    
    def get_global_metrics(self) -> Dict[str, Any]:
        """Get global aggregated metrics"""
        return self.metrics['global']

# Global instance
network_metrics = NetworkMetrics()
