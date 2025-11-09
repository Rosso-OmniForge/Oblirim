"""
Net Test - Network Connectivity and Captive Portal Detection
Detects internet access, captive portals, and network device presence
"""

import subprocess
import requests
import time
import json
import os
from datetime import datetime
from urllib.parse import urlparse

class NetTest:
    def __init__(self, log_callback=None):
        self.log_callback = log_callback
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(os.path.join(self.logs_dir, 'wifi'), exist_ok=True)
        
        # Test configuration
        self.test_urls = [
            'http://detectportal.firefox.com/success.txt',
            'http://captive.apple.com/hotspot-detect.html',
            'http://www.msftconnecttest.com/connecttest.txt'
        ]
        self.dns_servers = ['8.8.8.8', '1.1.1.1', '9.9.9.9']
        self.timeout = 10
        
        # Captive portal database
        self.captive_portal_log = os.path.join(self.data_dir, 'captive_portals.json')
        if not os.path.exists(self.captive_portal_log):
            with open(self.captive_portal_log, 'w') as f:
                json.dump([], f)
    
    def log(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[NET_TEST {timestamp}] {message}"
        print(log_entry)
        
        if self.log_callback:
            self.log_callback(log_entry)
    
    def test_dns_connectivity(self):
        """Test if DNS servers are reachable"""
        self.log("Testing DNS connectivity...")
        
        for dns in self.dns_servers:
            try:
                result = subprocess.run(
                    ['ping', '-c', '1', '-W', '2', dns],
                    capture_output=True, timeout=3
                )
                if result.returncode == 0:
                    self.log(f"✓ DNS server {dns} reachable")
                    return True, dns
            except Exception as e:
                self.log(f"DNS test to {dns} failed: {e}")
        
        self.log("✗ No DNS servers reachable")
        return False, None
    
    def test_http_connectivity(self):
        """Test HTTP connectivity and detect captive portals"""
        self.log("Testing HTTP connectivity...")
        
        for test_url in self.test_urls:
            try:
                response = requests.get(
                    test_url,
                    timeout=self.timeout,
                    allow_redirects=False,
                    headers={'User-Agent': 'Mozilla/5.0 (OBLIRIM NetTest)'}
                )
                
                # Check for redirects (captive portal signature)
                if response.status_code in [301, 302, 303, 307, 308]:
                    redirect_url = response.headers.get('Location', 'Unknown')
                    self.log(f"⚠ Captive portal detected - Redirect to: {redirect_url}")
                    return {
                        'success': False,
                        'captive_portal': True,
                        'portal_url': redirect_url,
                        'portal_type': self.identify_portal_type(redirect_url)
                    }
                
                # Check for known success responses
                if response.status_code == 200:
                    # Firefox success.txt should contain "success"
                    if 'detectportal.firefox.com' in test_url:
                        if 'success' in response.text.lower():
                            self.log("✓ Internet access confirmed (Firefox portal test)")
                            return {
                                'success': True,
                                'captive_portal': False,
                                'portal_url': None,
                                'portal_type': None
                            }
                    # Apple hotspot-detect should contain "Success"
                    elif 'captive.apple.com' in test_url:
                        if 'success' in response.text.lower():
                            self.log("✓ Internet access confirmed (Apple portal test)")
                            return {
                                'success': True,
                                'captive_portal': False,
                                'portal_url': None,
                                'portal_type': None
                            }
                    # Microsoft connecttest
                    elif 'msftconnecttest.com' in test_url:
                        if 'microsoft connect test' in response.text.lower():
                            self.log("✓ Internet access confirmed (Microsoft portal test)")
                            return {
                                'success': True,
                                'captive_portal': False,
                                'portal_url': None,
                                'portal_type': None
                            }
                    
                    # Generic 200 OK - likely internet access
                    self.log("✓ Internet access confirmed (200 OK)")
                    return {
                        'success': True,
                        'captive_portal': False,
                        'portal_url': None,
                        'portal_type': None
                    }
                
            except requests.exceptions.Timeout:
                self.log(f"Timeout testing {test_url}")
            except requests.exceptions.ConnectionError:
                self.log(f"Connection error testing {test_url}")
            except Exception as e:
                self.log(f"Error testing {test_url}: {e}")
        
        # All tests failed
        self.log("✗ No internet access detected")
        return {
            'success': False,
            'captive_portal': False,
            'portal_url': None,
            'portal_type': None
        }
    
    def identify_portal_type(self, portal_url):
        """Identify the type of captive portal based on URL"""
        if not portal_url:
            return "Unknown"
        
        url_lower = portal_url.lower()
        
        # Common portal types
        if 'wispr' in url_lower:
            return "WISPr"
        elif 'hotel' in url_lower or 'guest' in url_lower:
            return "Hotel/Guest"
        elif 'starbucks' in url_lower or 'coffee' in url_lower:
            return "Coffee Shop"
        elif 'airport' in url_lower:
            return "Airport"
        elif 'login' in url_lower or 'auth' in url_lower:
            return "Generic Auth"
        else:
            # Try to extract domain
            try:
                domain = urlparse(portal_url).netloc
                return f"Custom ({domain})"
            except:
                return "Unknown"
    
    def discover_network_devices(self, interface='wlan0', network_range=None):
        """
        Quick scan to discover other devices on the network
        Uses ping sweep and ARP scan
        """
        self.log(f"Discovering devices on {interface}...")
        
        # Get network range if not provided
        if not network_range:
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
                                subnet = parts[1]
                                # Extract network range (e.g., 192.168.1.0/24)
                                ip_parts = subnet.split('/')[0].split('.')
                                if len(ip_parts) == 4:
                                    network_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
                                    break
            except Exception as e:
                self.log(f"Error getting network range: {e}")
                return {'device_count': 0, 'devices': []}
        
        if not network_range:
            self.log("Could not determine network range")
            return {'device_count': 0, 'devices': []}
        
        self.log(f"Scanning network range: {network_range}")
        
        devices = []
        
        # Method 1: Quick nmap ping scan (no root required)
        try:
            result = subprocess.run(
                ['nmap', '-sn', '-T4', network_range],
                capture_output=True, text=True, timeout=60
            )
            if result.returncode == 0:
                # Parse output for hosts
                for line in result.stdout.split('\n'):
                    if 'Nmap scan report for' in line:
                        # Extract IP or hostname
                        parts = line.split('for')
                        if len(parts) > 1:
                            host_info = parts[1].strip()
                            devices.append({'host': host_info, 'method': 'nmap'})
                
                self.log(f"✓ nmap found {len(devices)} devices")
        except FileNotFoundError:
            self.log("nmap not installed - skipping")
        except Exception as e:
            self.log(f"nmap scan error: {e}")
        
        # Method 2: Check ARP table (already discovered devices)
        try:
            result = subprocess.run(
                ['ip', 'neigh', 'show'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                arp_count = 0
                for line in result.stdout.split('\n'):
                    if 'REACHABLE' in line or 'STALE' in line or 'DELAY' in line:
                        parts = line.split()
                        if len(parts) >= 1:
                            ip = parts[0]
                            # Check if already in devices list
                            if not any(ip in d['host'] for d in devices):
                                devices.append({'host': ip, 'method': 'arp'})
                                arp_count += 1
                
                if arp_count > 0:
                    self.log(f"✓ ARP table found {arp_count} additional devices")
        except Exception as e:
            self.log(f"ARP check error: {e}")
        
        self.log(f"Total devices discovered: {len(devices)}")
        
        return {
            'device_count': len(devices),
            'devices': devices,
            'network_range': network_range
        }
    
    def run_full_test(self, interface='wlan0', network_info=None):
        """
        Run complete network test
        Returns comprehensive results
        """
        self.log(f"=== Starting Net Test on {interface} ===")
        start_time = time.time()
        
        results = {
            'interface': interface,
            'timestamp': datetime.now().isoformat(),
            'dns_connectivity': False,
            'dns_server': None,
            'internet_access': False,
            'captive_portal': False,
            'portal_url': None,
            'portal_type': None,
            'devices_found': 0,
            'devices': [],
            'network_range': None,
            'trigger_network_tools': False,
            'test_duration': 0
        }
        
        # Add network info if provided
        if network_info:
            results['network_info'] = network_info
        
        # Step 1: Test DNS connectivity
        dns_ok, dns_server = self.test_dns_connectivity()
        results['dns_connectivity'] = dns_ok
        results['dns_server'] = dns_server
        
        if not dns_ok:
            self.log("⚠ DNS connectivity failed - network may be isolated")
            # Still try device discovery
        
        # Step 2: Test HTTP and detect captive portal
        http_results = self.test_http_connectivity()
        results['internet_access'] = http_results['success']
        results['captive_portal'] = http_results['captive_portal']
        results['portal_url'] = http_results['portal_url']
        results['portal_type'] = http_results['portal_type']
        
        # Log captive portal if detected
        if http_results['captive_portal']:
            self.log_captive_portal(interface, network_info, http_results)
        
        # Step 3: Discover network devices
        device_results = self.discover_network_devices(interface)
        results['devices_found'] = device_results['device_count']
        results['devices'] = device_results['devices']
        results['network_range'] = device_results['network_range']
        
        # Step 4: Determine if Network Tools should be triggered
        if results['devices_found'] > 0:
            results['trigger_network_tools'] = True
            self.log(f"✓ Network Tools will be triggered ({results['devices_found']} devices found)")
        else:
            results['trigger_network_tools'] = False
            self.log("⚠ No devices found - Network Tools will NOT be triggered")
        
        # Calculate duration
        results['test_duration'] = round(time.time() - start_time, 2)
        
        self.log(f"=== Net Test completed in {results['test_duration']}s ===")
        
        # Save results to file
        self.save_test_results(results)
        
        return results
    
    def log_captive_portal(self, interface, network_info, http_results):
        """Log detected captive portal to database"""
        try:
            with open(self.captive_portal_log, 'r') as f:
                portals = json.load(f)
            
            portal_entry = {
                'timestamp': datetime.now().isoformat(),
                'interface': interface,
                'ssid': network_info.get('ssid') if network_info else None,
                'portal_url': http_results['portal_url'],
                'portal_type': http_results['portal_type']
            }
            
            portals.append(portal_entry)
            
            with open(self.captive_portal_log, 'w') as f:
                json.dump(portals, f, indent=2)
            
            self.log(f"Captive portal logged: {http_results['portal_type']}")
            
        except Exception as e:
            self.log(f"Error logging captive portal: {e}")
    
    def save_test_results(self, results):
        """Save test results to file"""
        try:
            results_file = os.path.join(
                self.logs_dir, 'wifi',
                f"nettest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2)
            
            self.log(f"Test results saved: {results_file}")
            
        except Exception as e:
            self.log(f"Error saving test results: {e}")
    
    def get_recent_results(self, count=10):
        """Get recent test results"""
        try:
            results_dir = os.path.join(self.logs_dir, 'wifi')
            files = sorted(
                [f for f in os.listdir(results_dir) if f.startswith('nettest_')],
                reverse=True
            )[:count]
            
            results = []
            for filename in files:
                with open(os.path.join(results_dir, filename), 'r') as f:
                    results.append(json.load(f))
            
            return results
        except Exception as e:
            self.log(f"Error getting recent results: {e}")
            return []

# Global instance
net_test = NetTest()
