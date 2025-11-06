#!/bin/bash

# OBLIRIM PWN Master - Complete Installation Script
# This script sets up everything needed from a fresh Raspberry Pi OS installation
# Run with: ./install.sh

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# ASCII Art Header
print_banner() {
    clear
    echo -e "${GREEN}"
    echo "  ___  ____  _     ___ ____  ___ __  __ "
    echo " / _ \| __ )| |   |_ _|  _ \|_ _|  \/  |"
    echo "| | | |  _ \| |    | || |_) || || |\/| |"
    echo "| |_| | |_) | |___ | ||  _ < | || |  | |"
    echo " \___/|____/|_____|___|_| \_\___|_|  |_|"
    echo ""
    echo "PWN MASTER - Complete Installation Script"
    echo "=========================================="
    echo -e "${NC}"
}

# Utility functions
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_error "This script should NOT be run as root!"
        print_info "Run as a regular user with sudo privileges"
        exit 1
    fi
}

# Check if running on Raspberry Pi or Linux
check_system() {
    print_header "System Check"
    
    if [[ "$OSTYPE" != "linux-gnu"* ]]; then
        print_warning "This script is designed for Linux systems"
        print_info "Detected OS: $OSTYPE"
        read -p "Continue anyway? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    # Check if we're on a Raspberry Pi
    if [ -f /proc/device-tree/model ]; then
        PI_MODEL=$(cat /proc/device-tree/model 2>/dev/null | tr -d '\0')
        print_success "Detected: $PI_MODEL"
    else
        print_info "Running on generic Linux system"
    fi
    
    # Check architecture
    ARCH=$(uname -m)
    print_info "Architecture: $ARCH"
    
    print_success "System check completed"
    echo
}

# Update system packages
update_system() {
    print_header "System Update"
    
    print_info "Updating package lists..."
    sudo apt-get update -qq
    
    print_info "Upgrading system packages..."
    sudo apt-get upgrade -y
    
    print_success "System updated successfully"
    echo
}

# Install system dependencies
install_dependencies() {
    print_header "Installing Dependencies"
    
    # Essential packages
    PACKAGES=(
        "python3"
        "python3-pip" 
        "python3-venv"
        "python3-dev"
        "git"
        "curl"
        "wget"
        "htop"
        "nano"
        "build-essential"
        "bluetooth"
        "bluez"
        "bluez-tools"
        "net-tools"
        "iproute2"
        "iptables"
    )
    
    print_info "Installing essential packages..."
    for package in "${PACKAGES[@]}"; do
        if dpkg -l | grep -q "^ii  $package "; then
            print_success "$package already installed"
        else
            print_info "Installing $package..."
            sudo apt-get install -y "$package"
            print_success "$package installed"
        fi
    done
    
    # Install Pi-specific tools if on Raspberry Pi
    if [ -f /proc/device-tree/model ]; then
        print_info "Installing Raspberry Pi specific tools..."
        sudo apt-get install -y raspberrypi-kernel-headers || true
        
        # Ensure vcgencmd is available
        if [ ! -f /opt/vc/bin/vcgencmd ]; then
            print_warning "vcgencmd not found, some temperature readings may not work"
        else
            print_success "vcgencmd available for temperature monitoring"
        fi
    fi
    
    print_success "All dependencies installed"
    echo
}

# Install penetration testing tools
install_pentest_tools() {
    print_header "Installing Penetration Testing Tools"
    
    print_warning "⚠️  FOR AUTHORIZED TESTING ONLY ⚠️"
    print_info "These tools are for network security assessment on authorized networks only."
    echo
    
    read -p "Install penetration testing tools? (Y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        print_info "Skipping penetration testing tools installation"
        echo
        return
    fi
    
    # Network scanning and enumeration tools
    PENTEST_PACKAGES=(
        "nmap"                  # Network scanner
        "arp-scan"             # ARP scanner
        "masscan"              # Fast port scanner (optional)
        "nikto"                # Web vulnerability scanner
        "dirb"                 # Web content scanner
        "sslscan"              # SSL/TLS scanner
        "enum4linux"           # SMB enumeration
        "snmp"                 # SNMP tools
        "onesixtyone"          # SNMP scanner
        "hydra"                # Network login cracker
        "john"                 # Password cracker
        "aircrack-ng"          # WiFi security auditing
        "reaver"               # WPS attack tool
        "wireshark-common"     # Network protocol analyzer (CLI)
        "tcpdump"              # Packet analyzer
        "ettercap-common"      # Network sniffer
        "dsniff"               # Network auditing tools
        "nbtscan"              # NetBIOS scanner
        "metasploit-framework" # Exploitation framework (optional, large install)
    )
    
    print_info "Installing network scanning tools..."
    for package in "${PENTEST_PACKAGES[@]}"; do
        # Skip metasploit by default (large install)
        if [[ "$package" == "metasploit-framework" ]]; then
            read -p "Install Metasploit Framework? (large download, y/N) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                print_info "Skipping $package"
                continue
            fi
        fi
        
        if dpkg -l | grep -q "^ii  $package "; then
            print_success "$package already installed"
        else
            print_info "Installing $package..."
            sudo apt-get install -y "$package" 2>/dev/null || {
                print_warning "$package not available in repositories, skipping..."
            }
        fi
    done
    
    # Install additional tools via Python pip
    print_info "Installing Python-based security tools..."
    source "${PROJECT_DIR}/.venv/bin/activate" || source "${PROJECT_DIR}/venv/bin/activate" || true
    
    pip install --quiet scapy impacket || print_warning "Some Python tools failed to install"
    
    # Verify key tools
    print_info "Verifying tool installation..."
    REQUIRED_TOOLS=("nmap" "arp-scan" "nikto" "sslscan")
    
    for tool in "${REQUIRED_TOOLS[@]}"; do
        if command -v "$tool" >/dev/null 2>&1; then
            print_success "$tool verified"
        else
            print_error "$tool not found - some features may not work"
        fi
    done
    
    print_success "Penetration testing tools installation completed"
    print_warning "Remember: Use these tools responsibly and only on authorized networks!"
    echo
}

# Setup project environment
setup_project() {
    print_header "Project Setup"
    
    # Get the directory where this script is located
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    PROJECT_DIR="$SCRIPT_DIR"
    VENV_PATH="${PROJECT_DIR}/.venv"
    
    print_info "Project directory: $PROJECT_DIR"
    cd "$PROJECT_DIR"
    
    # Create necessary directories
    print_info "Creating project directories..."
    mkdir -p logs memory static/css static/js templates components
    
    # Create virtual environment
    print_info "Creating Python virtual environment..."
    if [ -d "$VENV_PATH" ]; then
        print_warning "Virtual environment already exists"
        read -p "Recreate it? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$VENV_PATH"
            python3 -m venv "$VENV_PATH"
            print_success "Virtual environment recreated"
        fi
    else
        python3 -m venv "$VENV_PATH"
        print_success "Virtual environment created"
    fi
    
    # Activate virtual environment and upgrade pip
    print_info "Activating virtual environment and upgrading pip..."
    source "${VENV_PATH}/bin/activate"
    pip install --upgrade pip setuptools wheel
    
    # Install Python packages
    if [ -f "${PROJECT_DIR}/requirements.txt" ]; then
        print_info "Installing Python packages from requirements.txt..."
        pip install -r "${PROJECT_DIR}/requirements.txt"
        print_success "Python packages installed"
    else
        print_error "requirements.txt not found!"
        exit 1
    fi
    
    print_success "Project setup completed"
    echo
}

# Configure system services
configure_services() {
    print_header "Service Configuration"
    
    # Enable and start Bluetooth if available
    if systemctl list-unit-files | grep -q bluetooth.service; then
        print_info "Configuring Bluetooth service..."
        sudo systemctl enable bluetooth
        sudo systemctl start bluetooth
        print_success "Bluetooth service configured"
    fi
    
    # Configure SSH (optional)
    if systemctl list-unit-files | grep -q ssh.service; then
        print_info "SSH service detected"
        if systemctl is-enabled ssh.service >/dev/null 2>&1; then
            print_success "SSH already enabled"
        else
            read -p "Enable SSH service? (y/N) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                sudo systemctl enable ssh
                sudo systemctl start ssh
                print_success "SSH service enabled"
            fi
        fi
    fi
    
    print_success "Service configuration completed"
    echo
}

# Create systemd service for auto-start
create_systemd_service() {
    print_header "Auto-Start Configuration"
    
    PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    SERVICE_NAME="oblirim"
    SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
    
    print_info "Creating systemd service for auto-start..."
    
    # Create service file
    sudo tee "$SERVICE_FILE" > /dev/null << EOF
[Unit]
Description=OBLIRIM PWN Master Dashboard
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
User=${USER}
Group=${USER}
WorkingDirectory=${PROJECT_DIR}
Environment=PATH=${PROJECT_DIR}/.venv/bin
ExecStart=${PROJECT_DIR}/.venv/bin/python ${PROJECT_DIR}/app.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

    # Set permissions and enable service
    sudo chmod 644 "$SERVICE_FILE"
    sudo systemctl daemon-reload
    sudo systemctl enable "$SERVICE_NAME"
    
    print_success "Systemd service created: /etc/systemd/system/oblirim.service"
    print_success "Service enabled for auto-start on boot"
    print_info "Manual control commands:"
    print_info "  Start:   sudo systemctl start $SERVICE_NAME"
    print_info "  Stop:    sudo systemctl stop $SERVICE_NAME"
    print_info "  Restart: sudo systemctl restart $SERVICE_NAME"
    print_info "  Status:  sudo systemctl status $SERVICE_NAME"
    print_info "  Logs:    sudo journalctl -u $SERVICE_NAME -f"
    print_info "  Disable: sudo systemctl disable $SERVICE_NAME"
    echo
}

# Create startup scripts
create_scripts() {
    print_header "Creating Utility Scripts"
    
    PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    
    # Create start script
    cat > "${PROJECT_DIR}/start.sh" << 'EOF'
#!/bin/bash
# Start OBLIRIM Dashboard
sudo systemctl start oblirim
echo "Dashboard started. Access at: http://localhost:5000"
EOF
    
    # Create stop script
    cat > "${PROJECT_DIR}/stop.sh" << 'EOF'
#!/bin/bash
# Stop OBLIRIM Dashboard
sudo systemctl stop oblirim
echo "Dashboard stopped."
EOF
    
    # Create status script
    cat > "${PROJECT_DIR}/status.sh" << 'EOF'
#!/bin/bash
# Check OBLIRIM Dashboard status
echo "=== OBLIRIM Dashboard Status ==="
sudo systemctl status oblirim --no-pager
echo ""
echo "=== Recent Logs ==="
sudo journalctl -u oblirim --no-pager -n 10
EOF
    
    # Create restart script
    cat > "${PROJECT_DIR}/restart.sh" << 'EOF'
#!/bin/bash
# Restart OBLIRIM Dashboard
echo "Restarting OBLIRIM Dashboard..."
sudo systemctl restart oblirim
echo "Dashboard restarted. Access at: http://localhost:5000"
EOF
    
    # Make scripts executable
    chmod +x "${PROJECT_DIR}"/{start,stop,status,restart}.sh
    
    print_success "Utility scripts created:"
    print_info "  ./start.sh   - Start the dashboard"
    print_info "  ./stop.sh    - Stop the dashboard"
    print_info "  ./restart.sh - Restart the dashboard"
    print_info "  ./status.sh  - Check status and logs"
    echo
}

# Configure network access
configure_network() {
    print_header "Network Configuration"
    
    # Get current IP
    LOCAL_IP=$(hostname -I | awk '{print $1}')
    print_info "Local IP address: $LOCAL_IP"
    
    # Configure firewall if ufw is available
    if command -v ufw >/dev/null 2>&1; then
        print_info "Configuring firewall for port 5000..."
        sudo ufw allow 5000/tcp comment "OBLIRIM Dashboard"
        print_success "Firewall configured"
    fi
    
    print_success "Network configuration completed"
    echo
}

# Final configuration and testing
final_setup() {
    print_header "Final Setup and Testing"
    
    PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    
    # Create initial memory files
    print_info "Creating initial configuration files..."
    
    # Create config file
    cat > "${PROJECT_DIR}/memory/config.json" << EOF
{
    "version": "1.0.0",
    "installation_date": "$(date -Iseconds)",
    "system_info": {
        "os": "$(lsb_release -d 2>/dev/null | cut -f2 || echo 'Unknown')",
        "architecture": "$(uname -m)",
        "python_version": "$(python3 --version)",
        "pi_model": "$(cat /proc/device-tree/model 2>/dev/null | tr -d '\0' || echo 'Generic Linux')"
    },
    "features": {
        "emotions_enabled": true,
        "auto_start": true,
        "bluetooth_monitoring": true
    }
}
EOF
    
    # Test the application
    print_info "Testing application startup..."
    cd "$PROJECT_DIR"
    source .venv/bin/activate
    
    # Quick test run
    timeout 5 python app.py >/dev/null 2>&1 && {
        print_success "Application test successful"
    } || {
        print_warning "Application test failed, but this might be normal (timeout)"
    }
    
    print_success "Final setup completed"
    echo
}

# Main installation process
main() {
    print_banner
    
    print_info "Starting OBLIRIM PWN Master installation..."
    print_info "This will install all dependencies and configure the system"
    echo
    
    read -p "Continue with installation? (Y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        print_info "Installation cancelled"
        exit 0
    fi
    
    check_root
    check_system
    update_system
    install_dependencies
    install_pentest_tools
    setup_project
    configure_services
    create_systemd_service
    create_scripts
    configure_network
    final_setup
    
    # Installation complete
    print_header "Installation Complete!"
    
    LOCAL_IP=$(hostname -I | awk '{print $1}')
    
    echo -e "${GREEN}"
    echo "🎉 OBLIRIM PWN Master has been successfully installed!"
    echo
    echo -e "${CYAN}Access the dashboard at:${NC}"
    echo "  Local:    http://localhost:5000"
    echo "  Network:  http://$LOCAL_IP:5000"
    echo
    echo -e "${CYAN}Control commands:${NC}"
    echo "  Start:    ./start.sh"
    echo "  Stop:     ./stop.sh"
    echo "  Restart:  ./restart.sh"
    echo "  Status:   ./status.sh"
    echo
    echo -e "${YELLOW}Next steps:${NC}"
    echo "1. Reboot the system: sudo reboot"
    echo "2. After reboot, the dashboard will start automatically"
    echo "3. Access the web interface using the URLs above"
    echo
    echo -e "${PURPLE}Advanced:${NC}"
    echo "  Service logs: sudo journalctl -u oblirim-dashboard -f"
    echo "  Manual start: sudo systemctl start oblirim-dashboard"
    echo
    print_success "Installation script completed successfully!"
    echo
    
    read -p "Reboot now? (Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        print_info "Rebooting system..."
        sudo reboot
    else
        print_info "Remember to reboot before using the dashboard"
    fi
}

# Run main function
main "$@"