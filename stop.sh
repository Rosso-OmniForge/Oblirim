#!/bin/bash

# Stop script for OBLIRIM Backend Server
# ONLY stops the Flask server (NOT the TUI)
# For TUI control, use: sudo systemctl stop oblirim-tui

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

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PID_FILE="${SCRIPT_DIR}/.dashboard_pid"
LOG_DIR="${SCRIPT_DIR}/logs"
LOG_FILE="${LOG_DIR}/dashboard.log"

print_header "OBLIRIM Backend Server - Stop"
print_info "This script ONLY stops the Flask backend"
print_info "TUI is controlled separately: sudo systemctl stop oblirim-tui"
echo ""

# Check if PID file exists
if [ ! -f "$PID_FILE" ]; then
    print_warning "Dashboard does not appear to be running (PID file not found)"
    exit 0
fi

# Get the PID
APP_PID=$(cat "$PID_FILE")

# Check if process is still running
if ! kill -0 "$APP_PID" 2>/dev/null; then
    print_warning "Process with PID $APP_PID is not running"
    rm -f "$PID_FILE"
    exit 0
fi

print_warning "Stopping Dashboard (PID: $APP_PID)..."

# Gracefully terminate the process
kill "$APP_PID"

# Wait a bit for graceful shutdown
sleep 2

# Check if process still exists, if so force kill
if kill -0 "$APP_PID" 2>/dev/null; then
    print_warning "Graceful shutdown timeout, force killing..."
    kill -9 "$APP_PID"
    sleep 1
fi

# Remove PID file
rm -f "$PID_FILE"

print_success "Dashboard stopped successfully"
echo ""
echo -e "${BLUE}Dashboard Information:${NC}"
echo "  Log file: $LOG_FILE"
echo ""
echo -e "${YELLOW}To view the last log entries:${NC}"
echo "  tail -20 $LOG_FILE"
echo ""
echo -e "${YELLOW}To view full logs with live updates:${NC}"
echo "  tail -f $LOG_FILE"
