#!/bin/bash

# Install script for Raspberry Pi Dashboard
# This script installs system dependencies, creates a virtual environment, and installs Python packages

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
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

# Main installation
print_header "Raspberry Pi Dashboard - Installation Script"

# Check if running on Raspberry Pi or Linux system
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    print_warning "This script is designed for Linux systems. You may encounter issues on other platforms."
fi

# Step 1: Update system packages
print_header "Step 1: Updating system packages"
if sudo -n true 2>/dev/null; then
    # User has sudo privileges without password
    sudo apt-get update
    sudo apt-get upgrade -y
    print_success "System packages updated"
else
    print_warning "Sudo password may be required. Please enter your password if prompted."
    sudo apt-get update
    sudo apt-get upgrade -y
    print_success "System packages updated"
fi

# Step 2: Install system dependencies
print_header "Step 2: Installing system dependencies"

# Check and install Python3 and pip
if ! command -v python3 &> /dev/null; then
    print_warning "Python3 not found. Installing..."
    sudo apt-get install -y python3
    print_success "Python3 installed"
else
    print_success "Python3 is already installed: $(python3 --version)"
fi

if ! command -v pip3 &> /dev/null; then
    print_warning "pip3 not found. Installing..."
    sudo apt-get install -y python3-pip
    print_success "pip3 installed"
else
    print_success "pip3 is already installed: $(pip3 --version)"
fi

# Install python3-venv if not present
if ! python3 -c "import venv" 2>/dev/null; then
    print_warning "python3-venv not found. Installing..."
    sudo apt-get install -y python3-venv
    print_success "python3-venv installed"
else
    print_success "python3-venv is available"
fi

# Install git (optional but recommended)
if ! command -v git &> /dev/null; then
    print_warning "Git not found. Installing..."
    sudo apt-get install -y git
    print_success "Git installed"
else
    print_success "Git is already installed: $(git --version)"
fi

# Step 3: Get the directory where this script is located
print_header "Step 3: Setting up virtual environment"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_PATH="${SCRIPT_DIR}/.venv"

print_warning "Script directory: $SCRIPT_DIR"
print_warning "Virtual environment path: $VENV_PATH"

# Step 4: Create virtual environment
if [ -d "$VENV_PATH" ]; then
    print_warning "Virtual environment already exists at $VENV_PATH"
    read -p "Do you want to recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$VENV_PATH"
        python3 -m venv "$VENV_PATH"
        print_success "Virtual environment recreated"
    else
        print_success "Using existing virtual environment"
    fi
else
    python3 -m venv "$VENV_PATH"
    print_success "Virtual environment created at $VENV_PATH"
fi

# Step 5: Activate virtual environment and install packages
print_header "Step 4: Installing Python packages"

# Source the activate script
source "${VENV_PATH}/bin/activate"
print_success "Virtual environment activated"

# Upgrade pip, setuptools, and wheel
print_warning "Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel
print_success "pip, setuptools, and wheel upgraded"

# Install requirements
if [ -f "${SCRIPT_DIR}/requirements.txt" ]; then
    print_warning "Installing packages from requirements.txt..."
    pip install -r "${SCRIPT_DIR}/requirements.txt"
    print_success "All Python packages installed successfully"
else
    print_error "requirements.txt not found in $SCRIPT_DIR"
    exit 1
fi

# Step 6: Summary and next steps
print_header "Installation Complete!"
print_success "All dependencies have been installed successfully"

echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. To activate the virtual environment, run:"
echo -e "   ${YELLOW}source ${VENV_PATH}/bin/activate${NC}"
echo ""
echo "2. To start the application, run:"
echo -e "   ${YELLOW}python ${SCRIPT_DIR}/app.py${NC}"
echo ""
echo "3. Access the dashboard at:"
echo -e "   ${YELLOW}http://localhost:5000${NC}"
echo ""
echo -e "${BLUE}To deactivate the virtual environment, run:${NC}"
echo -e "   ${YELLOW}deactivate${NC}"
echo ""

print_success "Installation script completed!"
