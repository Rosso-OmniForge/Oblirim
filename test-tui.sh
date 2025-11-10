#!/bin/bash

# OBLIRIM TUI Test Script
# Tests the TUI interface without full installation

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Banner
echo -e "${GREEN}"
echo "  ___  ____  _     ___ ____  ___ __  __ "
echo " / _ \| __ )| |   |_ _|  _ \|_ _|  \/  |"
echo "| | | |  _ \| |    | || |_) || || |\/| |"
echo "| |_| | |_) | |___ | ||  _ < | || |  | |"
echo " \___/|____/|_____|___|_| \_\___|_|  |_|"
echo ""
echo "TUI TEST - No Installation Required"
echo "====================================="
echo -e "${NC}"

# Functions
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

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_PATH="${SCRIPT_DIR}/.venv"
SERVER_PID=""

# Cleanup function
cleanup() {
    if [ -n "$SERVER_PID" ] && kill -0 "$SERVER_PID" 2>/dev/null; then
        print_info "Stopping test server (PID: $SERVER_PID)..."
        kill "$SERVER_PID" 2>/dev/null || true
        sleep 1
        # Force kill if still running
        kill -9 "$SERVER_PID" 2>/dev/null || true
    fi
    
    # Clean up temp files
    rm -f /tmp/oblirim_test_backend.sh
    rm -f /tmp/oblirim_backend.log
}

trap cleanup EXIT

# Step 1: Check virtual environment
if [ ! -d "$VENV_PATH" ]; then
    print_warning "Virtual environment not found. Creating one..."
    python3 -m venv "$VENV_PATH"
    source "${VENV_PATH}/bin/activate"
    pip install --upgrade pip >/dev/null 2>&1
    pip install -r "${SCRIPT_DIR}/requirements.txt" >/dev/null 2>&1
    print_success "Virtual environment created and dependencies installed"
else
    print_success "Virtual environment found"
    source "${VENV_PATH}/bin/activate"
fi

# Step 2: Check if backend is running
print_info "Checking for backend server..."
if curl -s http://localhost:5000 >/dev/null 2>&1; then
    print_success "Backend server is running on port 5000"
    BACKEND_RUNNING=true
else
    print_warning "Backend server not running on port 5000"
    print_info "Starting test backend server on port 5001..."
    
    # Start backend using the virtual environment
    cd "$SCRIPT_DIR"
    source "${VENV_PATH}/bin/activate"
    
    # Create a background script that uses the venv
    cat > /tmp/oblirim_test_backend.sh << 'BACKENDEOF'
#!/bin/bash
cd "$1"
source "$2/bin/activate"
python3 << 'PYEOF'
import sys
sys.path.insert(0, '.')
from app import app, socketio

print("Test backend starting on http://127.0.0.1:5001", flush=True)
socketio.run(app, host='127.0.0.1', port=5001, debug=False, allow_unsafe_werkzeug=True, use_reloader=False)
PYEOF
BACKENDEOF
    
    chmod +x /tmp/oblirim_test_backend.sh
    
    # Start backend in background
    /tmp/oblirim_test_backend.sh "$SCRIPT_DIR" "$VENV_PATH" > /tmp/oblirim_backend.log 2>&1 &
    SERVER_PID=$!
    print_info "Backend started (PID: $SERVER_PID)"
    
    # Wait for server to be ready
    print_info "Waiting for backend to be ready..."
    for i in {1..15}; do
        if curl -s http://localhost:5001 >/dev/null 2>&1; then
            print_success "Backend ready on port 5001"
            BACKEND_RUNNING=true
            export OBLIRIM_API_URL="http://localhost:5001"
            break
        fi
        sleep 1
    done
    
    if [ "$BACKEND_RUNNING" != "true" ]; then
        print_error "Failed to start backend server"
        print_info "Check logs: tail -f /tmp/oblirim_backend.log"
        exit 1
    fi
    
    # Cleanup temp script
    rm -f /tmp/oblirim_test_backend.sh
fi

# Step 3: Launch TUI
echo
print_info "Launching OBLIRIM TUI..."
echo -e "${YELLOW}═══════════════════════════════════════════${NC}"
echo -e "${CYAN}TUI Controls:${NC}"
echo "  q     - Quit TUI"
echo "  r     - Refresh display"
echo "  s     - Start manual scan"
echo "  Ctrl+C - Exit"
echo -e "${YELLOW}═══════════════════════════════════════════${NC}"
echo
sleep 2

# Ensure we're in the right directory and venv is activated
cd "$SCRIPT_DIR"
source "${VENV_PATH}/bin/activate"

# Verify textual is available
if ! python3 -c "import textual" 2>/dev/null; then
    print_error "Textual module not found in virtual environment"
    print_info "Reinstalling dependencies..."
    pip install -r requirements.txt
    if ! python3 -c "import textual" 2>/dev/null; then
        print_error "Failed to install textual. Check requirements.txt"
        exit 1
    fi
    print_success "Dependencies installed"
fi

# Run the TUI
print_info "Starting TUI application..."
python3 tui_app.py

# Done
echo
print_success "TUI test completed"
