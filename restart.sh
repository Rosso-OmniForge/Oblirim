#!/bin/bash

# Restart script for Raspberry Pi Dashboard
# Stops and starts the server in one command

# Color codes for output
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Raspberry Pi Dashboard - Restart${NC}"
echo -e "${BLUE}========================================${NC}"

# Stop the server
bash "${SCRIPT_DIR}/stop.sh"

# Wait a moment
sleep 2

# Start the server
bash "${SCRIPT_DIR}/launch.sh"
