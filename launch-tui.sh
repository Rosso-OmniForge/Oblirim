#!/bin/bash

# Launch script for OBLIRIM Textual TUI
# Starts the TUI interface on the current terminal

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

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_PATH="${SCRIPT_DIR}/.venv"
TUI_PATH="${SCRIPT_DIR}/tui_app.py"

print_header "OBLIRIM TUI - Launcher"

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    print_error "Virtual environment not found at $VENV_PATH"
    echo -e "${YELLOW}Please run ./install.sh first to set up the environment${NC}"
    exit 1
fi

# Check if tui_app.py exists
if [ ! -f "$TUI_PATH" ]; then
    print_error "tui_app.py not found at $TUI_PATH"
    exit 1
fi

# Check if Flask backend is running
if ! curl -s http://localhost:5000 > /dev/null 2>&1; then
    print_warning "Flask backend is not running on port 5000"
    print_warning "The TUI requires the backend service to be running"
    echo ""
    echo -e "${CYAN}Options:${NC}"
    echo "1. Start systemd service (if installed)"
    echo "2. Start development server (./launch.sh)"
    echo "3. Continue without backend (limited functionality)"
    echo ""
    read -p "Choose option (1-3): " -n 1 -r
    echo
    case $REPLY in
        1)
            print_info "Starting systemd service..."
            if systemctl list-unit-files | grep -q "oblirim.service"; then
                sudo systemctl start oblirim
                sleep 3
                if curl -s http://localhost:5000 > /dev/null 2>&1; then
                    print_success "Backend service started"
                else
                    print_error "Failed to start backend service"
                    echo -e "${YELLOW}Try: sudo systemctl start oblirim${NC}"
                    exit 1
                fi
            else
                print_error "Systemd service not installed"
                print_info "Run ./install.sh first or choose option 2"
                exit 1
            fi
            ;;
        2)
            print_info "Starting development server..."
            if [ -f "${SCRIPT_DIR}/launch.sh" ]; then
                "${SCRIPT_DIR}/launch.sh" &
                LAUNCH_PID=$!
                print_info "Development server started (PID: $LAUNCH_PID)"
                sleep 5
                if curl -s http://localhost:5000 > /dev/null 2>&1; then
                    print_success "Development server ready"
                else
                    print_warning "Development server may still be starting..."
                fi
            else
                print_error "launch.sh not found"
                exit 1
            fi
            ;;
        3)
            print_warning "Continuing without backend - some features may not work"
            ;;
        *)
            print_warning "Invalid option, continuing without backend"
            ;;
    esac
fi

print_success "Starting OBLIRIM TUI..."
echo ""
echo -e "${YELLOW}Controls:${NC}"
echo "  q     - Quit"
echo "  r     - Refresh display"
echo "  s     - Start manual scan"
echo "  Ctrl+C - Exit"
echo ""

# Activate virtual environment and run the TUI
cd "$SCRIPT_DIR"
source "${VENV_PATH}/bin/activate"
python "$TUI_PATH"

print_success "TUI exited normally"
