#!/usr/bin/env python3
"""
OBLIRIM TUI Application
Textual-based Terminal User Interface for Raspberry Pi HDMI Display
Replaces Chromium kiosk mode with lightweight TUI
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import Header, Footer, Static, Label, ProgressBar, DataTable
from textual.reactive import reactive
from textual import work
from textual.worker import Worker
import psutil
import socket
import subprocess
import os
import json
import time
from datetime import datetime
from components.eth_detector import eth_detector
from components.eth_workflow import eth_workflow
from components.network_metrics import network_metrics


class SystemStatsWidget(Static):
    """Display system statistics"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.border_title = "SYSTEM STATS"
    
    def compose(self) -> ComposeResult:
        yield Static(id="sys-content")
    
    def get_pi_model(self):
        """Detect Raspberry Pi model"""
        try:
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if line.startswith('Model'):
                        return line.split(':')[1].strip()
            with open('/proc/device-tree/model', 'r') as f:
                return f.read().strip().replace('\x00', '')
        except:
            return "Unknown"
    
    def get_temperature(self):
        """Get CPU temperature"""
        temp_paths = [
            '/sys/class/thermal/thermal_zone0/temp',
            '/opt/vc/bin/vcgencmd'
        ]
        
        for path in temp_paths:
            try:
                if path.endswith('vcgencmd'):
                    result = subprocess.run([path, 'measure_temp'], 
                                          capture_output=True, text=True, timeout=3)
                    if result.returncode == 0:
                        return result.stdout.strip().replace('temp=', '')
                else:
                    with open(path, 'r') as f:
                        temp_c = int(f.read().strip()) / 1000
                        return f"{temp_c:.1f}°C"
            except:
                continue
        return "N/A"
    
    def check_interface(self, interface_name):
        """Check if network interface is up"""
        try:
            operstate_path = f'/sys/class/net/{interface_name}/operstate'
            if os.path.exists(operstate_path):
                with open(operstate_path, 'r') as f:
                    state = f.read().strip()
                    if state in ['up', 'unknown']:
                        return "Up"
            return "Down"
        except:
            return "Down"
    
    def update_stats(self):
        """Update system statistics"""
        try:
            # Get IP address
            ip = "N/A"
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                s.close()
            except:
                pass
            
            # Get interface states
            wlan0 = self.check_interface('wlan0')
            wlan1 = self.check_interface('wlan1')
            eth0 = self.check_interface('eth0')
            
            # Get temperature
            temp = self.get_temperature()
            
            # Get CPU usage
            cpu = psutil.cpu_percent(interval=0.5)
            
            # Get memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used = round(memory.used / (1024**3), 2)
            memory_total = round(memory.total / (1024**3), 2)
            
            # Get disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_used = round(disk.used / (1024**3), 2)
            disk_total = round(disk.total / (1024**3), 2)
            
            # Get Pi model
            pi_model = self.get_pi_model()
            
            # Format the output
            content = f"""[bold cyan]Model:[/bold cyan]    {pi_model}
[bold cyan]IP:[/bold cyan]       {ip}
[bold cyan]WiFi0:[/bold cyan]    [{'green' if wlan0 == 'Up' else 'red'}]{wlan0}[/]
[bold cyan]WiFi1:[/bold cyan]    [{'green' if wlan1 == 'Up' else 'red'}]{wlan1}[/]
[bold cyan]ETH:[/bold cyan]      [{'green' if eth0 == 'Up' else 'red'}]{eth0}[/]
[bold cyan]Temp:[/bold cyan]     {temp}
[bold cyan]CPU:[/bold cyan]      {cpu:.1f}%
[bold cyan]RAM:[/bold cyan]      {memory_percent:.1f}% ({memory_used:.2f}GB / {memory_total:.2f}GB)
[bold cyan]Disk:[/bold cyan]     {disk_percent:.1f}% ({disk_used:.2f}GB / {disk_total:.2f}GB)"""
            
            # Update the content
            content_widget = self.query_one("#sys-content", Static)
            content_widget.update(content)
            
        except Exception as e:
            content_widget = self.query_one("#sys-content", Static)
            content_widget.update(f"[red]Error updating stats: {str(e)}[/red]")


class EthernetStatusWidget(Static):
    """Display Ethernet connection status and scan progress"""
    
    connection_status = reactive("DISCONNECTED")
    scan_phase = reactive("Idle")
    scan_progress = reactive(0)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.border_title = "ETHERNET STATUS"
        self.network_info = {}
        self.metrics = {
            'current': {'hosts': 0, 'ports': 0, 'vulnerabilities': 0},
            'historical': {'hosts': 0, 'ports': 0, 'vulnerabilities': 0, 'scans': 0}
        }
    
    def compose(self) -> ComposeResult:
        yield Static(id="eth-content")
        yield ProgressBar(total=100, show_eta=False, id="eth-progress")
    
    def update_status(self):
        """Update Ethernet status and metrics"""
        try:
            # Get Ethernet state
            eth_state = eth_detector.get_eth0_state()
            
            if eth_state:
                self.connection_status = "CONNECTED"
                network_info = eth_detector.get_network_info()
                self.network_info = network_info
                
                # Get network tally
                tally_file = os.path.join(os.path.dirname(__file__), 'data', 'network_tally.json')
                total_networks = 0
                if os.path.exists(tally_file):
                    with open(tally_file, 'r') as f:
                        tally_data = json.load(f)
                        total_networks = tally_data.get('total_networks', 0)
                
                # Get current metrics if we have a subnet
                if network_info.get('subnet'):
                    subnet_parts = network_info['subnet'].split('/')
                    if len(subnet_parts) == 2:
                        ip_addr = subnet_parts[0]
                        cidr = subnet_parts[1]
                        ip_parts = ip_addr.split('.')
                        if len(ip_parts) == 4:
                            network_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/{cidr}"
                            self.metrics = network_metrics.get_network_metrics(network_range)
                
                # Format output
                content = f"""[bold green]Status:[/bold green]    CONNECTED
[bold cyan]IP:[/bold cyan]        {network_info.get('ip', 'N/A')}
[bold cyan]Gateway:[/bold cyan]   {network_info.get('gateway', 'N/A')}
[bold cyan]Subnet:[/bold cyan]    {network_info.get('subnet', 'N/A')}
[bold cyan]Networks:[/bold cyan]  {total_networks}

[bold yellow]Scan Metrics:[/bold yellow]
[bold cyan]Hosts:[/bold cyan]     Current: {self.metrics['current'].get('hosts', 0)} | Historical: {self.metrics['historical'].get('hosts', 0)}
[bold cyan]Ports:[/bold cyan]     Current: {self.metrics['current'].get('ports', 0)} | Historical: {self.metrics['historical'].get('ports', 0)}
[bold red]Vulns:[/bold red]     Current: {self.metrics['current'].get('vulnerabilities', 0)} | Historical: {self.metrics['historical'].get('vulnerabilities', 0)}
[bold cyan]Scans:[/bold cyan]     {self.metrics['historical'].get('scans', 0)}

[bold yellow]Current Phase:[/bold yellow] {self.scan_phase}"""
            else:
                self.connection_status = "DISCONNECTED"
                content = f"""[bold red]Status:[/bold red]    DISCONNECTED

[dim]Waiting for Ethernet connection...[/dim]

[bold yellow]Historical Metrics:[/bold yellow]
[bold cyan]Hosts:[/bold cyan]     {self.metrics['historical'].get('hosts', 0)}
[bold cyan]Ports:[/bold cyan]     {self.metrics['historical'].get('ports', 0)}
[bold red]Vulns:[/bold red]     {self.metrics['historical'].get('vulnerabilities', 0)}
[bold cyan]Scans:[/bold cyan]     {self.metrics['historical'].get('scans', 0)}"""
            
            # Update content
            content_widget = self.query_one("#eth-content", Static)
            content_widget.update(content)
            
            # Update progress bar
            progress_bar = self.query_one("#eth-progress", ProgressBar)
            progress_bar.update(progress=self.scan_progress)
            
        except Exception as e:
            content_widget = self.query_one("#eth-content", Static)
            content_widget.update(f"[red]Error: {str(e)}[/red]")
    
    def update_scan_progress(self, phase: str, progress: int, message: str = ""):
        """Update scan progress"""
        self.scan_phase = phase
        self.scan_progress = progress
        self.update_status()


class LogViewerWidget(ScrollableContainer):
    """Display scrollable log output"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.border_title = "ETHERNET LOGS"
    
    def compose(self) -> ComposeResult:
        yield Static(id="log-content")
    
    def update_logs(self):
        """Update log display"""
        try:
            from components.tab_logger import tab_logger
            logs = tab_logger.get_recent_logs('eth', 50)
            
            if logs:
                log_widget = self.query_one("#log-content", Static)
                log_widget.update(logs)
        except Exception as e:
            log_widget = self.query_one("#log-content", Static)
            log_widget.update(f"[red]Error loading logs: {str(e)}[/red]")


class OblirimTUI(App):
    """Main Textual TUI Application for OBLIRIM"""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    Header {
        background: $primary;
        color: $text;
        text-style: bold;
    }
    
    Footer {
        background: $primary;
    }
    
    #main-container {
        height: 100%;
        width: 100%;
        background: $surface;
    }
    
    #top-panel {
        height: auto;
        max-height: 20;
        layout: horizontal;
    }
    
    #bottom-panel {
        height: 1fr;
        margin-top: 1;
    }
    
    SystemStatsWidget {
        width: 50%;
        height: 100%;
        border: solid $primary;
        padding: 1;
    }
    
    EthernetStatusWidget {
        width: 50%;
        height: 100%;
        border: solid $accent;
        padding: 1;
    }
    
    LogViewerWidget {
        height: 100%;
        border: solid $warning;
        padding: 1;
    }
    
    #sys-content, #eth-content, #log-content {
        height: auto;
    }
    
    ProgressBar {
        margin-top: 1;
    }
    """
    
    TITLE = "OBLIRIM PWN MASTER"
    SUB_TITLE = "⚠️  FOR AUTHORIZED TESTING ONLY  ⚠️"
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
        ("s", "scan", "Start Scan"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create child widgets"""
        yield Header(show_clock=True)
        with Container(id="main-container"):
            with Horizontal(id="top-panel"):
                yield SystemStatsWidget()
                yield EthernetStatusWidget()
            with Vertical(id="bottom-panel"):
                yield LogViewerWidget()
        yield Footer()
    
    def on_mount(self) -> None:
        """When app is mounted, start update loops"""
        self.update_timer = self.set_interval(2.0, self.update_display)
        self.log_timer = self.set_interval(5.0, self.update_logs)
        
        # Initialize Ethernet detector
        def handle_eth_workflow(state):
            """Handle Ethernet state changes"""
            if state == 'connected':
                network_info = eth_detector.get_network_info()
                if network_info['ip']:
                    # Start workflow in background
                    self.run_worker(self.run_workflow_async(network_info))
        
        def handle_workflow_progress(progress_data):
            """Handle workflow progress updates"""
            eth_widget = self.query_one(EthernetStatusWidget)
            phase = progress_data.get('phase', 'Unknown')
            progress = progress_data.get('progress', 0)
            message = progress_data.get('message', '')
            eth_widget.update_scan_progress(phase, progress, message)
        
        eth_workflow.add_progress_callback(handle_workflow_progress)
        eth_detector.workflow_callback = handle_eth_workflow
        eth_detector.start()
    
    @work(exclusive=True)
    async def run_workflow_async(self, network_info):
        """Run workflow asynchronously"""
        eth_workflow.run_workflow(network_info)
    
    def update_display(self) -> None:
        """Update all display widgets"""
        try:
            sys_widget = self.query_one(SystemStatsWidget)
            sys_widget.update_stats()
            
            eth_widget = self.query_one(EthernetStatusWidget)
            eth_widget.update_status()
        except Exception as e:
            pass  # Ignore errors during updates
    
    def update_logs(self) -> None:
        """Update log display"""
        try:
            log_widget = self.query_one(LogViewerWidget)
            log_widget.update_logs()
        except Exception as e:
            pass  # Ignore errors during log updates
    
    def action_refresh(self) -> None:
        """Manually refresh all data"""
        self.update_display()
        self.update_logs()
    
    def action_scan(self) -> None:
        """Start manual Ethernet scan"""
        try:
            network_info = eth_detector.get_network_info()
            if network_info['ip']:
                self.run_worker(self.run_workflow_async(network_info))
        except Exception as e:
            pass


def main():
    """Main entry point"""
    app = OblirimTUI()
    app.run()


if __name__ == "__main__":
    main()
