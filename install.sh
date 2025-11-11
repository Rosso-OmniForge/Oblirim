#!/bin/bash

# OBLIRIM - Ethernet Penetration Testing Interface
# Complete Installation Script for Raspberry Pi
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
    echo "Ethernet Penetration Testing Interface"
    echo "⚠️  FOR TESTING ONLY - NOT A FUCKING TOY ⚠️"
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
    
    print_warning "⚠️  FOR TESTING ONLY - NOT A FUCKING TOY ⚠️"
    print_info "These tools are for network security assessment."
    echo
    
    # Essential penetration testing packages
    PENTEST_PACKAGES=(
        "nmap"                  # Network scanner - ESSENTIAL
        "nikto"                # Web vulnerability scanner
        "sslscan"              # SSL/TLS scanner
        "enum4linux"           # SMB enumeration for Linux
        "snmp"                 # SNMP tools base
        "snmp-mibs-downloader" # SNMP MIBs for better enumeration
        "onesixtyone"          # SNMP scanner
        "tcpdump"              # Packet analyzer
        "nbtscan"              # NetBIOS scanner
        "dirb"                 # Web content scanner
        "masscan"              # Ultra-fast port scanner
    )
    
    # Optional but useful tools
    OPTIONAL_PACKAGES=(
        "hydra"                # Network login cracker
        "john"                 # Password cracker
        "aircrack-ng"          # WiFi security auditing
        "wireshark-common"     # Network protocol analyzer (CLI)
        "ettercap-common"      # Network sniffer
        "dsniff"               # Network auditing tools
    )
    
    print_info "Installing essential penetration testing tools..."
    for package in "${PENTEST_PACKAGES[@]}"; do
        if dpkg -l | grep -q "^ii  $package "; then
            print_success "$package already installed"
        else
            print_info "Installing $package..."
            sudo DEBIAN_FRONTEND=noninteractive apt-get install -y "$package" 2>&1 | grep -v "^Get:" || {
                print_warning "$package not available, skipping..."
            }
        fi
    done
    
    # Install arp-scan (requires special handling on some systems)
    if ! command -v arp-scan >/dev/null 2>&1; then
        print_info "Installing arp-scan..."
        sudo DEBIAN_FRONTEND=noninteractive apt-get install -y arp-scan || print_warning "arp-scan installation failed"
    else
        print_success "arp-scan already installed"
    fi
    
    # Install snmp-check separately (may be in different repos)
    print_info "Checking for snmp-check..."
    if ! command -v snmp-check >/dev/null 2>&1; then
        print_warning "snmp-check not in default repos - attempting alternative installation..."
        # Try to install from source or alternative repo
        sudo DEBIAN_FRONTEND=noninteractive apt-get install -y snmp-check 2>/dev/null || \
            print_warning "snmp-check unavailable - some SNMP features will be limited"
    else
        print_success "snmp-check already installed"
    fi
    
    # Verify CRITICAL tools
    print_info "Verifying critical tool installation..."
    REQUIRED_TOOLS=("nmap" "nikto")
    RECOMMENDED_TOOLS=("sslscan" "enum4linux" "onesixtyone")
    
    ALL_OK=true
    for tool in "${REQUIRED_TOOLS[@]}"; do
        if command -v "$tool" >/dev/null 2>&1; then
            VERSION=$($tool --version 2>&1 | head -1 || echo "installed")
            print_success "$tool verified: $VERSION"
        else
            print_error "$tool NOT FOUND - workflow will fail!"
            ALL_OK=false
        fi
    done
    
    for tool in "${RECOMMENDED_TOOLS[@]}"; do
        if command -v "$tool" >/dev/null 2>&1; then
            print_success "$tool verified"
        else
            print_warning "$tool not found - some features may not work"
        fi
    done
    
    if [ "$ALL_OK" = true ]; then
        print_success "All critical penetration testing tools installed successfully!"
    else
        print_error "Some critical tools are missing - please install manually"
    fi
    
    print_warning "Remember: FOR TESTING ONLY - NOT A FUCKING TOY!"
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

# Configure display rotation for Raspberry Pi
configure_display() {
    print_header "Display Configuration"

    if [ -f /boot/firmware/config.txt ]; then
        print_info "Configuring display rotation (90 degrees) in config.txt..."
        if grep -q "^display_rotate=" /boot/firmware/config.txt; then
            print_warning "display_rotate already present in config.txt"
            sudo sed -i 's/^display_rotate=.*/display_rotate=1/' /boot/firmware/config.txt
            print_success "Updated display_rotate=1"
        else
            if grep -q "^\[all\]" /boot/firmware/config.txt; then
                sudo sed -i '/^\[all\]/a display_rotate=1' /boot/firmware/config.txt
                print_success "Added display_rotate=1 to [all] section"
            else
                echo "" | sudo tee -a /boot/firmware/config.txt > /dev/null
                echo "[all]" | sudo tee -a /boot/firmware/config.txt > /dev/null
                echo "display_rotate=1" | sudo tee -a /boot/firmware/config.txt > /dev/null
                print_success "Created [all] section with display_rotate=1"
            fi
        fi
    else
        print_warning "/boot/firmware/config.txt not found – skipping config.txt part"
    fi

    CMDLINE="/boot/firmware/cmdline.txt"
    VIDEO_PARAM="video=HDMI-1:1920x1080@60,rotate=180"

    if [ -f "$CMDLINE" ]; then
        print_info "Adding '$VIDEO_PARAM' to $CMDLINE ..."
        if grep -q "video=HDMI-1:" "$CMDLINE"; then
            print_warning "A video=HDMI-1: parameter already exists – updating it"
            # Replace any existing HDMI-1 video= line
            sudo sed -i "s|video=HDMI-1:[^ ]*|$VIDEO_PARAM|g" "$CMDLINE"
            print_success "Updated video parameter in $CMDLINE"
        else
            # Append at the end (ensure a space before the new param)
            echo -n " $VIDEO_PARAM" | sudo tee -a "$CMDLINE" > /dev/null
            print_success "Appended '$VIDEO_PARAM' to $CMDLINE"
        fi
        print_warning "Changes to cmdline.txt require a reboot to take effect"
    else
        print_warning "$CMDLINE not found – skipping cmdline.txt part"
    fi

    print_warning "Display rotation (both methods) requires a reboot to take effect"
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
        
        # Configure Bluetooth PAN (Personal Area Network)
        print_info "Configuring Bluetooth PAN for Web UI access..."
        
        # Create NAP (Network Access Point) configuration
        # This allows devices to connect via Bluetooth and access the network
        if [ -f /etc/bluetooth/main.conf ]; then
            # Ensure PAN is enabled in bluetooth config
            if ! grep -q "^Class = 0x020300" /etc/bluetooth/main.conf; then
                print_info "Adding Bluetooth PAN class configuration..."
                echo "" | sudo tee -a /etc/bluetooth/main.conf > /dev/null
                echo "# Bluetooth PAN Configuration for OBLIRIM" | sudo tee -a /etc/bluetooth/main.conf > /dev/null
                echo "Class = 0x020300" | sudo tee -a /etc/bluetooth/main.conf > /dev/null
            fi
            
            # Enable discoverable mode by default
            if ! grep -q "^DiscoverableTimeout = 0" /etc/bluetooth/main.conf; then
                echo "DiscoverableTimeout = 0" | sudo tee -a /etc/bluetooth/main.conf > /dev/null
                print_info "Bluetooth set to always discoverable"
            fi
        fi
        
        # Create Bluetooth PAN network configuration script
        BT_PAN_SCRIPT="/usr/local/bin/setup-bt-pan.sh"
        sudo tee "$BT_PAN_SCRIPT" > /dev/null << 'BTPANEOF'
#!/bin/bash
# Bluetooth PAN Network Setup for OBLIRIM
# This script sets up the bnep0 interface when Bluetooth PAN connects

INTERFACE="bnep0"
IP_ADDRESS="10.0.0.1"
NETMASK="255.255.255.0"

# Wait for interface to appear
if [ -d "/sys/class/net/$INTERFACE" ]; then
    # Configure the interface
    ip addr add ${IP_ADDRESS}/${NETMASK} dev $INTERFACE
    ip link set $INTERFACE up
    
    # Enable IP forwarding for internet sharing (optional)
    echo 1 > /proc/sys/net/ipv4/ip_forward
    
    echo "Bluetooth PAN interface $INTERFACE configured: $IP_ADDRESS"
fi
BTPANEOF
        
        sudo chmod +x "$BT_PAN_SCRIPT"
        print_success "Bluetooth PAN configuration script created"
        
        print_info "Bluetooth PAN setup completed"
        print_warning "To connect via Bluetooth PAN:"
        print_info "  1. Pair your device with the Raspberry Pi"
        print_info "  2. Connect to Bluetooth PAN network"
        print_info "  3. Access Web UI at http://10.0.0.1:5000"
    else
        print_warning "Bluetooth service not available"
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
    
    # Create service file with proper environment activation
    sudo tee "$SERVICE_FILE" > /dev/null << EOF
[Unit]
Description=OBLIRIM PWN Master Dashboard
After=network-online.target
Wants=network-online.target
Requires=network-online.target

[Service]
Type=simple
User=${USER}
Group=${USER}
WorkingDirectory=${PROJECT_DIR}
Environment="PATH=${PROJECT_DIR}/.venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="VIRTUAL_ENV=${PROJECT_DIR}/.venv"
Environment="PYTHONPATH=${PROJECT_DIR}"

# Ensure directories exist before starting
ExecStartPre=/bin/mkdir -p ${PROJECT_DIR}/logs ${PROJECT_DIR}/data ${PROJECT_DIR}/memory
ExecStartPre=/bin/mkdir -p ${PROJECT_DIR}/logs/eth ${PROJECT_DIR}/logs/wifi ${PROJECT_DIR}/logs/wireless
ExecStartPre=/bin/bash -c '[ -f ${PROJECT_DIR}/data/network_tally.json ] || echo "{\"total_networks\": 0, \"last_updated\": null}" > ${PROJECT_DIR}/data/network_tally.json'

# Verify virtual environment exists
ExecStartPre=/bin/bash -c '[ -d ${PROJECT_DIR}/.venv ] || exit 1'

# Start the application
ExecStart=${PROJECT_DIR}/.venv/bin/python ${PROJECT_DIR}/app.py

# Restart configuration
Restart=always
RestartSec=10
StartLimitBurst=5
StartLimitIntervalSec=120

# Logging
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

    # Set permissions and enable service
    sudo chmod 644 "$SERVICE_FILE"
    sudo systemctl daemon-reload
    sudo systemctl enable "$SERVICE_NAME"
    
    print_success "Systemd service created: /etc/systemd/system/${SERVICE_NAME}.service"
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

# Create Textual TUI systemd service for HDMI display
create_tui_service() {
    print_header "TUI Display Configuration"
    
    PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    SERVICE_NAME="oblirim-tui"
    SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
    HDMI_CHECK_SCRIPT="/usr/local/bin/check-hdmi.sh"
    
    print_info "Creating Textual TUI service for HDMI display..."
    
    # Install HDMI detection script
    if [ -f "${PROJECT_DIR}/check-hdmi.sh" ]; then
        sudo cp "${PROJECT_DIR}/check-hdmi.sh" "$HDMI_CHECK_SCRIPT"
        sudo chmod +x "$HDMI_CHECK_SCRIPT"
        print_success "HDMI detection script installed"
    else
        print_warning "check-hdmi.sh not found, TUI will start without HDMI check"
        HDMI_CHECK_SCRIPT=""
    fi
    
    # Add user to tty group for display access
    print_info "Adding user to tty group for display access..."
    sudo usermod -a -G tty ${USER}
    print_success "User added to tty group (will take effect after logout/reboot)"
    
    # Create systemd service file
    sudo tee "$SERVICE_FILE" > /dev/null << EOF
[Unit]
Description=OBLIRIM TUI Display (Textual Interface on HDMI)
After=oblirim.service network-online.target
Requires=oblirim.service
Wants=network-online.target

[Service]
Type=simple
User=${USER}
Group=tty
WorkingDirectory=${PROJECT_DIR}
Environment="PATH=${PROJECT_DIR}/.venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="VIRTUAL_ENV=${PROJECT_DIR}/.venv"
Environment="PYTHONPATH=${PROJECT_DIR}"
Environment="TERM=xterm-256color"

StandardInput=tty
StandardOutput=tty
TTYPath=/dev/tty1
TTYReset=yes
TTYVHangup=yes

# Check if HDMI display is connected before starting${HDMI_CHECK_SCRIPT:+
ExecStartPre=$HDMI_CHECK_SCRIPT}

# Disable console blanking
ExecStartPre=/bin/bash -c 'setterm -blank 0 -powerdown 0 < /dev/tty1 > /dev/tty1 2>/dev/null || true'

# Wait for backend to be ready (with timeout)
ExecStartPre=/bin/bash -c 'timeout 60 bash -c "until curl -sf http://localhost:5000 > /dev/null 2>&1; do sleep 1; done" || (echo "Backend not ready after 60s" && exit 1)'

# Verify virtual environment exists
ExecStartPre=/bin/bash -c '[ -d ${PROJECT_DIR}/.venv ] || exit 1'

# Start the TUI
ExecStart=${PROJECT_DIR}/.venv/bin/python ${PROJECT_DIR}/tui_app.py

# Restart configuration
Restart=always
RestartSec=10
StartLimitBurst=3
StartLimitIntervalSec=120

[Install]
WantedBy=multi-user.target
EOF

    # Set permissions and enable service
    sudo chmod 644 "$SERVICE_FILE"
    sudo systemctl daemon-reload
    sudo systemctl enable "$SERVICE_NAME"
    
    print_success "Textual TUI service created: /etc/systemd/system/${SERVICE_NAME}.service"
    print_success "TUI display enabled for auto-start on tty1"
    print_success "TUI will wait for backend to be ready before starting"
    if [ -n "$HDMI_CHECK_SCRIPT" ]; then
        print_success "TUI will only start when HDMI display is connected"
    fi
    print_info "TUI control commands:"
    print_info "  Start:   sudo systemctl start $SERVICE_NAME"
    print_info "  Stop:    sudo systemctl stop $SERVICE_NAME"
    print_info "  Restart: sudo systemctl restart $SERVICE_NAME"
    print_info "  Status:  sudo systemctl status $SERVICE_NAME"
    print_info "  Disable: sudo systemctl disable $SERVICE_NAME"
    print_info "Note: The TUI will display on tty1 (main console on HDMI)"
    print_info "To access console: Switch to tty2-6 with Ctrl+Alt+F2-F6"
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
    
    print_success "Network configuration completed"
    print_info "Web UI will be accessible at:"
    print_info "  Local:    http://localhost:5000"
    print_info "  Network:  http://$LOCAL_IP:5000"
    print_info ""
    print_warning "Note: No firewall rules applied"
    print_info "If you want to restrict access, configure firewall manually:"
    print_info "  sudo ufw allow 5000  # Allow from all"
    print_info "  sudo ufw enable      # Enable firewall"
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
    
    PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    
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
    configure_display
    configure_services
    create_systemd_service
    create_tui_service
    create_scripts
    configure_network
    final_setup
    
    # Verify services are enabled before declaring success
    print_header "Installation Verification"
    
    print_info "Verifying service installation..."
    ALL_OK=true
    
    if systemctl is-enabled oblirim >/dev/null 2>&1; then
        print_success "Main service (oblirim) enabled for auto-start"
    else
        print_error "Main service (oblirim) NOT enabled"
        ALL_OK=false
    fi
    
    if systemctl is-enabled oblirim-tui >/dev/null 2>&1; then
        print_success "TUI service (oblirim-tui) enabled for auto-start"
    else
        print_error "TUI service (oblirim-tui) NOT enabled"
        ALL_OK=false
    fi
    
    # Check virtual environment
    if [ -d "${PROJECT_DIR}/.venv" ]; then
        print_success "Virtual environment created"
    else
        print_error "Virtual environment missing"
        ALL_OK=false
    fi
    
    # Check critical tools
    for tool in nmap nikto python3; do
        if command -v $tool >/dev/null 2>&1; then
            print_success "$tool installed"
        else
            print_warning "$tool not found (some features may not work)"
        fi
    done
    
    if [ "$ALL_OK" = false ]; then
        print_error "Installation verification failed!"
        print_error "Some services are not properly configured"
        print_warning "Please review the errors above before rebooting"
        exit 1
    fi
    
    print_success "All critical components verified successfully!"
    echo ""
    
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