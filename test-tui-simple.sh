#!/bin/bash

# OBLIRIM TUI Simple Test
# Uses existing launch scripts for easier testing

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${GREEN}"
echo "  ___  ____  _     ___ ____  ___ __  __ "
echo " / _ \| __ )| |   |_ _|  _ \|_ _|  \/  |"
echo "| | | |  _ \| |    | || |_) || || |\/| |"
echo "| |_| | |_) | |___ | ||  _ < | || |  | |"
echo " \___/|____/|_____|___|_| \_\___|_|  |_|"
echo ""
echo "TUI SIMPLE TEST"
echo "==============="
echo -e "${NC}"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${CYAN}This script will launch the TUI in a simple way:${NC}"
echo ""
echo "1. Ensure virtual environment exists"
echo "2. Launch TUI (which will offer to start backend)"
echo ""

# Check for venv
if [ ! -d "${SCRIPT_DIR}/.venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv "${SCRIPT_DIR}/.venv"
    source "${SCRIPT_DIR}/.venv/bin/activate"
    pip install --upgrade pip >/dev/null 2>&1
    pip install -r "${SCRIPT_DIR}/requirements.txt"
    echo -e "${GREEN}✓ Virtual environment ready${NC}"
else
    echo -e "${GREEN}✓ Virtual environment exists${NC}"
fi

echo ""
echo -e "${CYAN}Launching TUI...${NC}"
echo -e "${YELLOW}The TUI will check for backend and offer to start it if needed${NC}"
echo ""
sleep 2

# Run the TUI launcher
exec "${SCRIPT_DIR}/launch-tui.sh"
