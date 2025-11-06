"""
Tab-Specific Logger
Handles structured logging to README.md files for different tabs
"""

import os
import json
from datetime import datetime
import threading

class TabLogger:
    def __init__(self, base_logs_dir=None):
        if base_logs_dir is None:
            base_logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        self.base_logs_dir = base_logs_dir
        self.lock = threading.Lock()
        
        # Ensure base directory exists
        os.makedirs(base_logs_dir, exist_ok=True)

    def get_tab_dir(self, tab_name):
        """Get the directory for a specific tab"""
        return os.path.join(self.base_logs_dir, tab_name)

    def ensure_tab_dir(self, tab_name):
        """Ensure the tab directory exists"""
        tab_dir = self.get_tab_dir(tab_name)
        os.makedirs(tab_dir, exist_ok=True)
        return tab_dir

    def create_session_id(self, network_info=''):
        """Create a unique session ID"""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        if network_info:
            # Clean network info for filename
            clean_network = network_info.replace('/', '-').replace('.', '-')
            return f"{timestamp}_{clean_network}"
        return timestamp

    def log_session_start(self, tab_name, session_id, network_info=None):
        """Start a new session log"""
        with self.lock:
            tab_dir = self.ensure_tab_dir(tab_name)
            readme_path = os.path.join(tab_dir, 'README.md')
            
            # Create or append to README
            mode = 'a' if os.path.exists(readme_path) else 'w'
            with open(readme_path, mode) as f:
                if mode == 'w':
                    f.write(f"# {tab_name.upper()} Penetration Testing Logs\n\n")
                
                f.write(f"## Session: {session_id}\n")
                if network_info:
                    f.write(f"- **Network:** {network_info}\n")
                f.write(f"- **Started:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    def log_event(self, tab_name, session_id, event_type, details):
        """Log a specific event"""
        with self.lock:
            tab_dir = self.ensure_tab_dir(tab_name)
            readme_path = os.path.join(tab_dir, 'README.md')
            
            with open(readme_path, 'a') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"- **{event_type}:** {details} ({timestamp})\n")

    def log_phase(self, tab_name, session_id, phase_number, description, details=""):
        """Log a workflow phase"""
        phase_name = f"Phase {phase_number}"
        full_details = description
        if details:
            full_details += f" → {details}"
        self.log_event(tab_name, session_id, phase_name, full_details)

    def log_completion(self, tab_name, session_id, summary=""):
        """Log session completion"""
        with self.lock:
            tab_dir = self.ensure_tab_dir(tab_name)
            readme_path = os.path.join(tab_dir, 'README.md')
            
            with open(readme_path, 'a') as f:
                f.write(f"- **Completed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                if summary:
                    f.write(f"- **Summary:** {summary}\n")
                f.write("\n---\n\n")

    def log_error(self, tab_name, session_id, error_msg):
        """Log an error"""
        self.log_event(tab_name, session_id, "ERROR", error_msg)

    def get_recent_logs(self, tab_name, lines=50):
        """Get recent log entries"""
        tab_dir = self.ensure_tab_dir(tab_name)
        readme_path = os.path.join(tab_dir, 'README.md')
        
        if not os.path.exists(readme_path):
            return "No logs available"
        
        try:
            with open(readme_path, 'r') as f:
                content = f.read()
                lines_list = content.split('\n')
                return '\n'.join(lines_list[-lines:])
        except Exception as e:
            return f"Error reading logs: {e}"

    def get_session_summary(self, tab_name, session_id):
        """Get summary for a specific session"""
        logs = self.get_recent_logs(tab_name, 200)
        # Extract session block
        lines = logs.split('\n')
        session_lines = []
        in_session = False
        
        for line in lines:
            if f"## Session: {session_id}" in line:
                in_session = True
            elif line.startswith("## Session:") and in_session:
                break
            elif in_session:
                session_lines.append(line)
        
        return '\n'.join(session_lines) if session_lines else "Session not found"

# Global instance
tab_logger = TabLogger()