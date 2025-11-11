#!/bin/bash

# Quick Test Launcher for OBLIRIM
# Fast testing without full installation

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}OBLIRIM Quick Test${NC}"
echo "=================="
echo

# Quick options
echo -e "${CYAN}Quick test options:${NC}"
echo "1. Full test suite (./test-dev.sh --full)"
echo "2. Start test server (./test-dev.sh --server)"
echo "3. Interactive test menu (./test-dev.sh)"
echo "4. Test TUI with auto-backend (./test-tui.sh)"
echo "5. Launch TUI only (./launch-tui.sh)"
echo "6. Launch Web server only (./launch.sh)"
echo

read -p "Choose option (1-6): " choice

case $choice in
    1)
        echo -e "${YELLOW}Running full test suite...${NC}"
        ./test-dev.sh --full
        ;;
    2)
        echo -e "${YELLOW}Starting test server...${NC}"
        ./test-dev.sh --server
        ;;
    3)
        echo -e "${YELLOW}Opening interactive test menu...${NC}"
        ./test-dev.sh
        ;;
    4)
        echo -e "${YELLOW}Testing TUI (with auto-backend)...${NC}"
        ./test-tui.sh
        ;;
    5)
        echo -e "${YELLOW}Launching TUI...${NC}"
        ./launch-tui.sh
        ;;
    6)
        echo -e "${YELLOW}Launching web server...${NC}"
        ./launch.sh
        ;;
    *)
        echo -e "${YELLOW}Invalid choice. Running interactive menu...${NC}"
        ./test-dev.sh
        ;;
esac