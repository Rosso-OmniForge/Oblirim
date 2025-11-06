#!/bin/bash

# OBLIRIM Installation Test Script
# Verifies that all components are properly installed

set -e

# Colors
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

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_header "OBLIRIM Installation Test"
echo

# Check Python version
print_header "Python Environment"
if command -v python3 >/dev/null 2>&1; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python installed: $PYTHON_VERSION"
else
    print_error "Python 3 not found"
    exit 1
fi

# Check virtual environment
if [ -d "venv" ] || [ -d ".venv" ]; then
    print_success "Virtual environment found"
else
    print_warning "Virtual environment not found"
fi

# Check requirements.txt
if [ -f "requirements.txt" ]; then
    print_success "requirements.txt exists"
else
    print_error "requirements.txt not found"
fi
echo

# Check penetration testing tools
print_header "Penetration Testing Tools"
TOOLS=("nmap" "arp-scan" "nikto" "dirb" "sslscan" "enum4linux")
MISSING_TOOLS=()

for tool in "${TOOLS[@]}"; do
    if command -v "$tool" >/dev/null 2>&1; then
        VERSION=$($tool --version 2>&1 | head -1 || echo "installed")
        print_success "$tool: $VERSION"
    else
        print_error "$tool not installed"
        MISSING_TOOLS+=("$tool")
    fi
done
echo

# Check network interfaces
print_header "Network Interfaces"
if [ -d "/sys/class/net/eth0" ]; then
    ETH0_STATUS=$(cat /sys/class/net/eth0/operstate 2>/dev/null || echo "unknown")
    print_success "eth0 exists (status: $ETH0_STATUS)"
else
    print_warning "eth0 not found"
fi

if [ -d "/sys/class/net/wlan0" ]; then
    WLAN0_STATUS=$(cat /sys/class/net/wlan0/operstate 2>/dev/null || echo "unknown")
    print_success "wlan0 exists (status: $WLAN0_STATUS)"
else
    print_warning "wlan0 not found"
fi
echo

# Check project structure
print_header "Project Structure"
REQUIRED_FILES=("app.py" "requirements.txt" "install.sh")
REQUIRED_DIRS=("components" "templates" "logs" "data")

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_success "$file exists"
    else
        print_error "$file not found"
    fi
done

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        print_success "$dir/ directory exists"
    else
        print_warning "$dir/ directory not found (will be created on startup)"
    fi
done
echo

# Check Python modules
print_header "Python Modules"
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

PYTHON_MODULES=("flask" "flask_socketio" "psutil")
for module in "${PYTHON_MODULES[@]}"; do
    if python3 -c "import $module" 2>/dev/null; then
        print_success "Python module: $module"
    else
        print_error "Python module: $module not installed"
    fi
done
echo

# Check systemd service
print_header "Systemd Service"
if systemctl list-unit-files | grep -q oblirim; then
    SERVICE_STATUS=$(systemctl is-enabled oblirim 2>/dev/null || echo "not enabled")
    print_success "Systemd service: $SERVICE_STATUS"
else
    print_warning "Systemd service not installed (optional)"
fi
echo

# Summary
print_header "Summary"
if [ ${#MISSING_TOOLS[@]} -eq 0 ]; then
    print_success "All penetration testing tools installed"
else
    print_warning "Missing tools: ${MISSING_TOOLS[*]}"
    echo -e "${YELLOW}To install missing tools:${NC}"
    echo "  sudo apt install ${MISSING_TOOLS[*]}"
fi

echo
print_success "Installation test completed!"
echo
echo -e "${BLUE}To start the application:${NC}"
echo "  source venv/bin/activate"
echo "  python app.py"
echo
echo -e "${BLUE}Or use the control scripts:${NC}"
echo "  ./start.sh"
echo "  ./status.sh"
echo
