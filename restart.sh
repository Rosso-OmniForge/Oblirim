#!/bin/bash

# Restart script for OBLIRIM Backend Server
# ONLY restarts the Flask server (NOT the TUI)
# For TUI control, use: sudo systemctl restart oblirim-tui

# Color codes for output
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}OBLIRIM Backend Server - Restart${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${BLUE}ℹ This script ONLY restarts the Flask backend${NC}"
echo -e "${BLUE}ℹ TUI is controlled separately: sudo systemctl restart oblirim-tui${NC}"
echo ""

# Stop the server
bash "${SCRIPT_DIR}/stop.sh"

# Wait a moment
sleep 2

# Start the server
bash "${SCRIPT_DIR}/launch.sh"
