#!/bin/bash

# Launch script for Raspberry Pi Dashboard
# Starts the Flask-SocketIO server headlessly

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
APP_PATH="${SCRIPT_DIR}/app.py"
LOG_DIR="${SCRIPT_DIR}/logs"
LOG_FILE="${LOG_DIR}/dashboard.log"
PID_FILE="${SCRIPT_DIR}/.dashboard_pid"

print_header "Raspberry Pi Dashboard - Launcher"

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    print_error "Virtual environment not found at $VENV_PATH"
    echo -e "${YELLOW}Please run ./install.sh first to set up the environment${NC}"
    exit 1
fi

# Create logs directory if it doesn't exist
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
    print_success "Created logs directory"
fi

# Check if app.py exists
if [ ! -f "$APP_PATH" ]; then
    print_error "app.py not found at $APP_PATH"
    exit 1
fi

# Check if already running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if kill -0 "$OLD_PID" 2>/dev/null; then
        print_warning "Dashboard is already running (PID: $OLD_PID)"
        read -p "Do you want to restart it? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_warning "Stopping existing process..."
            kill "$OLD_PID"
            sleep 2
        else
            exit 0
        fi
    else
        rm -f "$PID_FILE"
    fi
fi

print_warning "Starting Raspberry Pi Dashboard..."

# Activate virtual environment and run the app in the background
(
    source "${VENV_PATH}/bin/activate"
    cd "$SCRIPT_DIR"
    python "$APP_PATH" >> "$LOG_FILE" 2>&1
) &

# Save the PID
APP_PID=$!
echo "$APP_PID" > "$PID_FILE"

# Give it a moment to start
sleep 2

# Check if process is still running
if kill -0 "$APP_PID" 2>/dev/null; then
    print_success "Dashboard started successfully (PID: $APP_PID)"
    echo ""
    echo -e "${BLUE}Dashboard Information:${NC}"
    echo "  URL: http://localhost:5000"
    echo "  PID: $APP_PID"
    echo "  Log file: $LOG_FILE"
    echo ""
    echo -e "${YELLOW}To stop the server, run:${NC}"
    echo "  kill $APP_PID"
    echo "  or"
    echo "  ./stop.sh"
    echo ""
    print_success "Dashboard is running headlessly in the background"
else
    print_error "Failed to start the dashboard"
    echo -e "${YELLOW}Check the log file for details:${NC}"
    echo "  tail -f $LOG_FILE"
    rm -f "$PID_FILE"
    exit 1
fi
