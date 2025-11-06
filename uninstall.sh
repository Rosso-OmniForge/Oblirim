#!/bin/bash

# OBLIRIM PWN Master - Uninstall Script
# This script removes the OBLIRIM installation and services

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_header "OBLIRIM PWN Master - Uninstall"

echo "This will remove the OBLIRIM dashboard service and files."
read -p "Are you sure you want to uninstall? (y/N) " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstall cancelled"
    exit 0
fi

# Stop and disable service
print_warning "Stopping and disabling service..."
sudo systemctl stop oblirim-dashboard 2>/dev/null || true
sudo systemctl disable oblirim-dashboard 2>/dev/null || true

# Remove service file
sudo rm -f /etc/systemd/system/oblirim-dashboard.service
sudo systemctl daemon-reload

print_success "Service removed"

# Option to remove project files
read -p "Remove project files? (y/N) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    print_warning "Removing project directory: $PROJECT_DIR"
    cd /tmp
    rm -rf "$PROJECT_DIR"
    print_success "Project files removed"
else
    print_warning "Project files kept - you can manually remove them later"
fi

print_success "Uninstall completed"