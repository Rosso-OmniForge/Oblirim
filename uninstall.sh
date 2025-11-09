#!/bin/bash

# OBLIRIM - Ethernet Penetration Testing Interface
# Complete Uninstallation Script
# Run with: ./uninstall.sh

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
    echo -e "${RED}"
    echo "  ___  ____  _     ___ ____  ___ __  __ "
    echo " / _ \| __ )| |   |_ _|  _ \|_ _|  \/  |"
    echo "| | | |  _ \| |    | || |_) || || |\/| |"
    echo "| |_| | |_) | |___ | ||  _ < | || |  | |"
    echo " \___/|____/|_____|___|_| \_\___|_|  |_|"
    echo ""
    echo "UNINSTALLATION SCRIPT"
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

# Stop all OBLIRIM services
stop_services() {
    print_header "Stopping Services"
    
    # Stop kiosk service
    if systemctl is-active --quiet oblirim-kiosk 2>/dev/null; then
        print_info "Stopping kiosk service..."
        sudo systemctl stop oblirim-kiosk
        print_success "Kiosk service stopped"
    else
        print_info "Kiosk service not running"
    fi
    
    # Stop main service
    if systemctl is-active --quiet oblirim 2>/dev/null; then
        print_info "Stopping main OBLIRIM service..."
        sudo systemctl stop oblirim
        print_success "Main service stopped"
    else
        print_info "Main service not running"
    fi
    
    print_success "All services stopped"
    echo
}

# Disable auto-start services
disable_services() {
    print_header "Disabling Auto-Start"
    
    # Disable kiosk service
    if systemctl list-unit-files | grep -q "oblirim-kiosk.service"; then
        print_info "Disabling kiosk auto-start..."
        sudo systemctl disable oblirim-kiosk
        print_success "Kiosk auto-start disabled"
    else
        print_info "Kiosk service not found"
    fi
    
    # Disable main service
    if systemctl list-unit-files | grep -q "oblirim.service"; then
        print_info "Disabling OBLIRIM auto-start..."
        sudo systemctl disable oblirim
        print_success "OBLIRIM auto-start disabled"
    else
        print_info "Main service not found"
    fi
    
    print_success "Auto-start disabled"
    echo
}

# Remove systemd service files
remove_services() {
    print_header "Removing Service Files"
    
    # Remove kiosk service file
    if [ -f /etc/systemd/system/oblirim-kiosk.service ]; then
        print_info "Removing kiosk service file..."
        sudo rm /etc/systemd/system/oblirim-kiosk.service
        print_success "Kiosk service file removed"
    else
        print_info "Kiosk service file not found"
    fi
    
    # Remove main service file
    if [ -f /etc/systemd/system/oblirim.service ]; then
        print_info "Removing main service file..."
        sudo rm /etc/systemd/system/oblirim.service
        print_success "Main service file removed"
    else
        print_info "Main service file not found"
    fi
    
    # Reload systemd daemon
    print_info "Reloading systemd daemon..."
    sudo systemctl daemon-reload
    print_success "Systemd daemon reloaded"
    
    print_success "Service files removed"
    echo
}

# Remove kiosk script
remove_kiosk_script() {
    print_header "Removing Kiosk Scripts"
    
    PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    KIOSK_SCRIPT="${PROJECT_DIR}/start-kiosk.sh"
    
    if [ -f "$KIOSK_SCRIPT" ]; then
        print_info "Removing kiosk startup script..."
        rm "$KIOSK_SCRIPT"
        print_success "Kiosk script removed"
    else
        print_info "Kiosk script not found"
    fi
    
    print_success "Kiosk scripts cleaned up"
    echo
}

# Remove utility scripts
remove_utility_scripts() {
    print_header "Removing Utility Scripts"
    
    PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    
    SCRIPTS=("start.sh" "stop.sh" "status.sh" "restart.sh")
    
    for script in "${SCRIPTS[@]}"; do
        if [ -f "${PROJECT_DIR}/${script}" ]; then
            print_info "Removing ${script}..."
            rm "${PROJECT_DIR}/${script}"
            print_success "${script} removed"
        fi
    done
    
    print_success "Utility scripts removed"
    echo
}

# Remove firewall rules
remove_firewall_rules() {
    print_header "Removing Firewall Rules"
    
    if command -v ufw >/dev/null 2>&1; then
        print_info "Removing firewall rule for port 5000..."
        sudo ufw delete allow 5000/tcp 2>/dev/null || print_info "Firewall rule not found"
        print_success "Firewall rules cleaned up"
    else
        print_info "UFW not installed, skipping firewall cleanup"
    fi
    
    echo
}

# Remove display rotation configuration
remove_display_config() {
    print_header "Removing Display Configuration"
    
    if [ -f /boot/firmware/config.txt ]; then
        if grep -q "^display_rotate=" /boot/firmware/config.txt; then
            print_info "Removing display rotation from config.txt..."
            sudo sed -i '/^display_rotate=/d' /boot/firmware/config.txt
            print_success "Display rotation configuration removed"
            print_warning "Reboot required for display changes to take effect"
        else
            print_info "No display rotation configuration found"
        fi
    else
        print_info "config.txt not found, skipping"
    fi
    
    echo
}

# Optional: Remove installed packages
remove_packages() {
    print_header "Package Removal (Optional)"
    
    print_warning "This will remove packages that were installed by OBLIRIM"
    print_info "Some packages may be used by other applications"
    read -p "Remove installed packages? (y/N) " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Skipping package removal"
        echo
        return
    fi
    
    # Packages to potentially remove
    PACKAGES=(
        "chromium-browser"
        "unclutter"
        "xdotool"
        "nmap"
        "nikto"
        "sslscan"
        "enum4linux"
        "snmp"
        "snmp-mibs-downloader"
        "onesixtyone"
        "tcpdump"
        "nbtscan"
        "dirb"
        "masscan"
        "arp-scan"
    )
    
    print_info "Removing OBLIRIM-specific packages..."
    for package in "${PACKAGES[@]}"; do
        if dpkg -l | grep -q "^ii  $package "; then
            print_info "Removing $package..."
            sudo apt-get remove -y "$package" 2>/dev/null || print_warning "Failed to remove $package"
        fi
    done
    
    # Clean up unused dependencies
    print_info "Cleaning up unused dependencies..."
    sudo apt-get autoremove -y
    
    print_success "Package removal completed"
    echo
}

# Optional: Remove Python virtual environment
remove_venv() {
    print_header "Virtual Environment Removal (Optional)"
    
    PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    VENV_PATH="${PROJECT_DIR}/.venv"
    
    if [ -d "$VENV_PATH" ]; then
        read -p "Remove Python virtual environment? (y/N) " -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Removing virtual environment..."
            rm -rf "$VENV_PATH"
            print_success "Virtual environment removed"
        else
            print_info "Keeping virtual environment"
        fi
    else
        print_info "Virtual environment not found"
    fi
    
    echo
}

# Optional: Remove project files
remove_project_files() {
    print_header "Project Files Removal (Optional)"
    
    PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    
    print_warning "⚠️  DANGER ZONE ⚠️"
    print_warning "This will remove logs, memory, and data files"
    print_info "The following directories will be removed:"
    print_info "  - logs/"
    print_info "  - memory/"
    print_info "  - data/"
    echo
    read -p "Remove project data files? (y/N) " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Keeping project files"
        echo
        return
    fi
    
    # Remove logs
    if [ -d "${PROJECT_DIR}/logs" ]; then
        print_info "Removing logs directory..."
        rm -rf "${PROJECT_DIR}/logs"
        print_success "Logs removed"
    fi
    
    # Remove memory
    if [ -d "${PROJECT_DIR}/memory" ]; then
        print_info "Removing memory directory..."
        rm -rf "${PROJECT_DIR}/memory"
        print_success "Memory removed"
    fi
    
    # Remove data
    if [ -d "${PROJECT_DIR}/data" ]; then
        print_info "Removing data directory..."
        rm -rf "${PROJECT_DIR}/data"
        print_success "Data removed"
    fi
    
    print_success "Project data files removed"
    echo
}

# Optional: Complete removal
complete_removal() {
    print_header "Complete Project Removal (Optional)"
    
    PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    
    print_warning "⚠️  EXTREME DANGER ZONE ⚠️"
    print_warning "This will remove the ENTIRE OBLIRIM project directory"
    print_info "Project directory: $PROJECT_DIR"
    echo
    print_error "THIS CANNOT BE UNDONE!"
    echo
    read -p "Type 'DELETE EVERYTHING' to confirm complete removal: " CONFIRMATION
    
    if [[ "$CONFIRMATION" != "DELETE EVERYTHING" ]]; then
        print_info "Complete removal cancelled"
        echo
        return
    fi
    
    print_info "Removing entire project directory..."
    cd /tmp  # Move out of the project directory
    rm -rf "$PROJECT_DIR"
    print_success "Project completely removed"
    print_info "Uninstall script has removed its own directory"
    echo
    
    exit 0
}

# Final summary
print_summary() {
    print_header "Uninstallation Summary"
    
    echo -e "${GREEN}OBLIRIM has been uninstalled!${NC}"
    echo
    echo -e "${CYAN}What was removed:${NC}"
    echo "  ✓ Systemd services stopped and disabled"
    echo "  ✓ Service files removed from /etc/systemd/system/"
    echo "  ✓ Kiosk and utility scripts removed"
    echo "  ✓ Firewall rules cleaned up"
    echo
    echo -e "${YELLOW}What remains (if not removed):${NC}"
    echo "  - Python virtual environment (.venv/)"
    echo "  - Project files (logs, memory, data)"
    echo "  - Installed system packages"
    echo "  - Core application files (app.py, components/, etc.)"
    echo
    echo -e "${CYAN}Next steps:${NC}"
    echo "  - Reboot if you removed display configuration"
    echo "  - Manually remove project directory if desired"
    echo "  - Run 'sudo apt autoremove' to clean up unused packages"
    echo
    print_success "Uninstallation completed successfully!"
    echo
}

# Main uninstallation process
main() {
    print_banner
    
    print_warning "⚠️  OBLIRIM UNINSTALLATION ⚠️"
    print_info "This will stop and remove OBLIRIM services"
    echo
    
    read -p "Continue with uninstallation? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Uninstallation cancelled"
        exit 0
    fi
    
    check_root
    stop_services
    disable_services
    remove_services
    remove_kiosk_script
    remove_utility_scripts
    remove_firewall_rules
    remove_display_config
    remove_packages
    remove_venv
    remove_project_files
    
    # Ask about complete removal last
    read -p "Perform complete project removal? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        complete_removal
        # This function exits, so code below won't run if complete removal is done
    fi
    
    print_summary
    
    read -p "Reboot now? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Rebooting system..."
        sudo reboot
    else
        print_info "Remember to reboot if display configuration was changed"
    fi
}

# Run main function
main "$@"