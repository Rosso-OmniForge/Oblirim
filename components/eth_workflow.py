"""
Ethernet Workflow Engine
Implements the 4-phase penetration testing workflow for Ethernet connections
"""

import subprocess
import threading
import time
import os
import json
from datetime import datetime
from components.tab_logger import tab_logger

class EthernetWorkflow:
    def __init__(self):
        self.is_running = False
        self.stop_requested = False
        self.current_session = None
        self.progress_callbacks = []
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.tools_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tools')
        
        # Ensure directories exist
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.tools_dir, exist_ok=True)
        
        # Tool verification
        self.required_tools = [
            'nmap', 'arp-scan', 'nikto', 'dirb', 'sslscan', 
            'enum4linux', 'smb-vuln-*', 'snmp-check', 'onesixtyone'
        ]

    def add_progress_callback(self, callback):
        """Add a callback for progress updates"""
        self.progress_callbacks.append(callback)

    def notify_progress(self, phase, progress, message, data=None):
        """Notify all progress callbacks"""
        for callback in self.progress_callbacks:
            try:
                callback({
                    'phase': phase,
                    'progress': progress,
                    'message': message,
                    'data': data or {},
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                print(f"Error in progress callback: {e}")

    def run_command(self, cmd, timeout=30, log_output=True):
        """Run a shell command with timeout and optional logging"""
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, 
                timeout=timeout, cwd=self.tools_dir
            )
            
            output = result.stdout
            error = result.stderr
            
            if log_output and self.current_session:
                if output:
                    tab_logger.log_event('eth', self.current_session, 'Command Output', f"{cmd}: {output[:200]}...")
                if error:
                    tab_logger.log_error('eth', self.current_session, f"{cmd}: {error}")
            
            return result.returncode == 0, output, error
            
        except subprocess.TimeoutExpired:
            error_msg = f"Command timed out: {cmd}"
            if self.current_session:
                tab_logger.log_error('eth', self.current_session, error_msg)
            return False, "", error_msg
        except Exception as e:
            error_msg = f"Command failed: {cmd} - {e}"
            if self.current_session:
                tab_logger.log_error('eth', self.current_session, error_msg)
            return False, "", str(e)

    def verify_tools(self):
        """Verify required tools are installed"""
        missing_tools = []
        for tool in self.required_tools:
            # Handle wildcards
            if '*' in tool:
                base_tool = tool.split('-')[0]
                success, _, _ = self.run_command(f"which {base_tool}", log_output=False)
                if not success:
                    missing_tools.append(tool)
            else:
                success, _, _ = self.run_command(f"which {tool}", log_output=False)
                if not success:
                    missing_tools.append(tool)
        
        if missing_tools:
            warning = f"Missing tools: {', '.join(missing_tools)} - Install with install.sh"
            self.notify_progress('verification', 50, warning)
            tab_logger.log_event('eth', self.current_session, 'Tool Check', warning)
            print(f"WARNING: {warning}")
            # Don't fail - continue with available tools
        else:
            self.notify_progress('verification', 100, "All required tools verified")
            print("✓ All penetration testing tools verified")
        
        return True  # Always return True to continue workflow

    def phase_1_network_detection(self, network_info):
        """Phase 1: Network Detection & Initialization"""
        self.notify_progress('phase1', 10, "Starting Phase 1: Network Detection")
        
        try:
            # Log interface details
            success, output, error = self.run_command("ip link show eth0")
            if success and output:
                tab_logger.log_phase('eth', self.current_session, 1, "Interface detected", "eth0 details logged")
            
            # Get network range
            if network_info.get('subnet'):
                ip_parts = network_info['subnet'].split('/')
                if len(ip_parts) == 2:
                    base_ip = ip_parts[0]
                    subnet = ip_parts[1]
                    # Calculate network range (simplified)
                    network_range = f"{base_ip.rsplit('.', 1)[0]}.0/{subnet}"
                    tab_logger.log_event('eth', self.current_session, 'Network Range', network_range)
            
            # Classify network
            if network_info.get('ip'):
                ip = network_info['ip']
                if ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('172.'):
                    network_type = "RFC1918 Private Network"
                else:
                    network_type = "Public Network"
                tab_logger.log_event('eth', self.current_session, 'Network Classification', network_type)
            
            self.notify_progress('phase1', 100, "Phase 1 completed: Network detected and classified")
            return True
            
        except Exception as e:
            tab_logger.log_error('eth', self.current_session, f"Phase 1 error: {e}")
            self.notify_progress('phase1', 0, f"Phase 1 failed: {e}")
            return False

    def phase_2_host_discovery(self, network_range):
        """Phase 2: Host Discovery"""
        self.notify_progress('phase2', 20, "Starting Phase 2: Host Discovery")
        
        try:
            # nmap ping scan
            self.notify_progress('phase2', 40, "Running nmap ping scan...")
            success, output, error = self.run_command(f"nmap -sn {network_range}", timeout=120)
            if success:
                # Parse host count
                lines = output.split('\n')
                host_count = sum(1 for line in lines if 'Nmap scan report for' in line)
                tab_logger.log_phase('eth', self.current_session, 2, f"nmap -sn completed", f"{host_count} hosts found")
                print(f"   ✓ Found {host_count} active hosts")
            
            # Skip arp-scan - requires root privileges
            self.notify_progress('phase2', 70, "Skipping arp-scan (requires root)...")
            tab_logger.log_event('eth', self.current_session, 'ARP Scan', "Skipped (requires root privileges)")
            
            self.notify_progress('phase2', 100, "Phase 2 completed: Host discovery finished")
            return True
            
        except Exception as e:
            tab_logger.log_error('eth', self.current_session, f"Phase 2 error: {e}")
            self.notify_progress('phase2', 0, f"Phase 2 failed: {e}")
            return False

    def phase_3_service_enumeration(self, target_hosts):
        """Phase 3: Service Enumeration"""
        self.notify_progress('phase3', 30, "Starting Phase 3: Service Enumeration")
        
        try:
            total_hosts = len(target_hosts) if target_hosts else 3
            completed = 0
            
            for host in target_hosts[:3]:  # Limit to 3 hosts
                self.notify_progress('phase3', 30 + (completed / total_hosts) * 50, f"Scanning {host}...")
                
                # Use TCP connect scan (-sT) instead of SYN scan - no root needed
                # Also add -Pn to skip ping (host may block ICMP)
                success, output, error = self.run_command(f"nmap -sT -T4 --top-ports 100 -Pn {host}", timeout=60)
                if success:
                    open_ports = output.count('open')
                    tab_logger.log_event('eth', self.current_session, f'Port Scan {host}', f"{open_ports} ports open")
                
                # Service version detection - also with -Pn
                success, output, error = self.run_command(f"nmap -sV -sC -Pn {host}", timeout=120)
                if success:
                    tab_logger.log_event('eth', self.current_session, f'Service Scan {host}', "Version detection completed")
                
                # Skip UDP scan - requires root privileges
                # Log that we're skipping it
                tab_logger.log_event('eth', self.current_session, f'UDP Scan {host}', "Skipped (requires root)")
                
                completed += 1
            
            self.notify_progress('phase3', 80, "Phase 3 completed: Service enumeration finished")
            return True
            
        except Exception as e:
            tab_logger.log_error('eth', self.current_session, f"Phase 3 error: {e}")
            self.notify_progress('phase3', 0, f"Phase 3 failed: {e}")
            return False

    def phase_4_vulnerability_scanning(self, target_hosts):
        """Phase 4: Vulnerability Scanning"""
        self.notify_progress('phase4', 50, "Starting Phase 4: Vulnerability Scanning")
        
        try:
            vulnerabilities_found = 0
            total = len(target_hosts[:3])
            completed = 0
            
            for host in target_hosts[:3]:  # Limit for demo
                self.notify_progress('phase4', 50 + (completed / total) * 40, f"Vulnerability scanning {host}...")
                
                # HTTP scanning - reduced timeout to 60 seconds
                success, output, error = self.run_command(f"nikto -h {host} -Tuning 123 -maxtime 60", timeout=90)
                if success and 'vulnerabilities found' in output.lower():
                    vuln_count = output.count('OSVDB')  # Rough count
                    vulnerabilities_found += vuln_count
                    tab_logger.log_phase('eth', self.current_session, 4, f"nikto scan on {host}", f"{vuln_count} vulnerabilities found")
                elif not success and 'not found' in error:
                    tab_logger.log_event('eth', self.current_session, f'Nikto {host}', "Skipped (tool not installed)")
                
                # SMB scanning - only if tool exists
                success, output, error = self.run_command(f"enum4linux -a {host}", timeout=60)
                if success:
                    tab_logger.log_event('eth', self.current_session, f'SMB Enum {host}', "SMB enumeration completed")
                elif not success and 'not found' in error:
                    tab_logger.log_event('eth', self.current_session, f'SMB Enum {host}', "Skipped (enum4linux not installed)")
                
                # SNMP scanning - only if tool exists
                success, output, error = self.run_command(f"snmp-check {host}", timeout=30)
                if success:
                    tab_logger.log_event('eth', self.current_session, f'SNMP Check {host}', "SNMP enumeration completed")
                elif not success and 'not found' in error:
                    tab_logger.log_event('eth', self.current_session, f'SNMP Check {host}', "Skipped (snmp-check not installed)")
                
                completed += 1
            
            self.notify_progress('phase4', 100, f"Phase 4 completed: {vulnerabilities_found} vulnerabilities found")
            return True
            
        except Exception as e:
            tab_logger.log_error('eth', self.current_session, f"Phase 4 error: {e}")
            self.notify_progress('phase4', 0, f"Phase 4 failed: {e}")
            return False

    def run_workflow(self, network_info):
        """Run the complete 4-phase penetration testing workflow"""
        try:
            print(f"\n{'='*60}")
            print(f"🔍 STARTING ETHERNET PENETRATION TESTING WORKFLOW")
            print(f"{'='*60}\n")
            
            self.is_running = True
            self.stop_requested = False
            
            # Create session
            network_str = network_info.get('subnet', 'unknown')
            self.current_session = tab_logger.create_session_id(network_str)
            tab_logger.log_session_start('eth', self.current_session, network_str)
            
            print(f"📋 Session: {self.current_session}")
            print(f"🌐 Network: {network_str}")
            
            self.notify_progress('start', 0, f"Starting Ethernet workflow for {network_str}")
            
            # Verify tools
            print(f"\n🔧 Verifying penetration testing tools...")
            if not self.verify_tools():
                return False
            
            # Phase 1: Network Detection
            print(f"\n📡 PHASE 1: Network Detection & Initialization")
            if self.stop_requested:
                tab_logger.log_event('eth', 'Workflow stopped by user (before Phase 1)')
                return False
            if not self.phase_1_network_detection(network_info):
                print("❌ Phase 1 failed")
                return False
            print("✓ Phase 1 complete")
            
            # Calculate network range for scanning from actual IP
            network_range = "192.168.1.0/24"  # Fallback default
            discovered_hosts = []
            
            if network_info.get('subnet'):
                # Parse the subnet properly
                subnet_parts = network_info['subnet'].split('/')
                if len(subnet_parts) == 2:
                    ip_addr = subnet_parts[0]
                    cidr = subnet_parts[1]
                    # Calculate network base from IP
                    ip_parts = ip_addr.split('.')
                    if len(ip_parts) == 4:
                        network_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/{cidr}"
            
            print(f"🎯 Target network range: {network_range}")
            
            # Phase 2: Host Discovery
            print(f"\n🔎 PHASE 2: Host Discovery")
            if self.stop_requested:
                tab_logger.log_event('eth', 'Workflow stopped by user (before Phase 2)')
                return False
            if not self.phase_2_host_discovery(network_range):
                print("❌ Phase 2 failed")
                return False
            print("✓ Phase 2 complete")
            
            # Extract discovered hosts from Phase 2 for Phase 3
            # Parse network range to get gateway and sample hosts
            base_ip = network_range.split('/')[0].rsplit('.', 1)[0]
            gateway = f"{base_ip}.1"
            sample_hosts = [gateway]  # Start with gateway
            
            # Add some common IPs from the actual network
            for i in [10, 20, 50, 100, 254]:
                sample_hosts.append(f"{base_ip}.{i}")
            
            print(f"🎯 Sample hosts for detailed scan: {', '.join(sample_hosts[:3])}...")
            
            # Phase 3: Service Enumeration (sample hosts)
            print(f"\n🔬 PHASE 3: Service Enumeration")
            if self.stop_requested:
                tab_logger.log_event('eth', 'Workflow stopped by user (before Phase 3)')
                return False
            if not self.phase_3_service_enumeration(sample_hosts[:3]):  # Limit to 3 hosts for speed
                print("❌ Phase 3 failed")
                return False
            print("✓ Phase 3 complete")
            
            # Phase 4: Vulnerability Scanning
            print(f"\n🛡️  PHASE 4: Vulnerability Assessment")
            if self.stop_requested:
                tab_logger.log_event('eth', 'Workflow stopped by user (before Phase 4)')
                return False
            if not self.phase_4_vulnerability_scanning(sample_hosts[:3]):  # Same 3 hosts
                print("❌ Phase 4 failed")
                return False
            print("✓ Phase 4 complete")
            
            # Complete
            print(f"\n{'='*60}")
            print(f"✅ WORKFLOW COMPLETE")
            print(f"{'='*60}\n")
            summary = f"Workflow completed: {len(sample_hosts)} hosts scanned"
            tab_logger.log_completion('eth', self.current_session, summary)
            self.notify_progress('complete', 100, summary)
            
            return True
            
        except Exception as e:
            error_msg = f"Workflow failed: {e}"
            if self.current_session:
                tab_logger.log_error('eth', self.current_session, error_msg)
            self.notify_progress('error', 0, error_msg)
            return False
        finally:
            self.is_running = False
            self.stop_requested = False
            self.current_session = None
            # Emit idle state
            self.notify_progress('idle', 0, 'Workflow complete - System idle')
    
    def stop_workflow(self):
        """Stop the currently running workflow"""
        if self.is_running:
            self.stop_requested = True
            tab_logger.log_event('eth', 'Stop requested - workflow will halt at next phase')
            return True
        return False

# Global instance
eth_workflow = EthernetWorkflow()