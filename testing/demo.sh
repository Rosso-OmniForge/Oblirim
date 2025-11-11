#!/bin/bash

# OBLIRIM PWN Master - Demo Script
# Shows current system status and dashboard info

# Color codes
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}"
echo "  ___  ____  _     ___ ____  ___ __  __ "
echo " / _ \| __ )| |   |_ _|  _ \|_ _|  \/  |"
echo "| | | |  _ \| |    | || |_) || || |\/| |"
echo "| |_| | |_) | |___ | ||  _ < | || |  | |"
echo " \___/|____/|_____|___|_| \_\___|_|  |_|"
echo ""
echo "PWN MASTER - System Demo"
echo "========================"
echo -e "${NC}"

# Check if service is running
if systemctl is-active --quiet oblirim; then
    echo -e "${GREEN}✓ Dashboard service is running${NC}"
    LOCAL_IP=$(hostname -I | awk '{print $1}')
    echo -e "${CYAN}Access at: http://$LOCAL_IP:5000${NC}"
else
    echo -e "${YELLOW}⚠ Dashboard service not running${NC}"
    echo "Start with: ./start.sh"
fi

echo ""
echo -e "${CYAN}System Information:${NC}"
echo "Pi Model: $(cat /proc/device-tree/model 2>/dev/null | tr -d '\0' || echo 'Generic Linux')"
echo "CPU Usage: $(top -bn1 | grep load | awk '{printf "%.1f%%\n", $(NF-2)*100}')"
echo "Memory: $(free | grep Mem | awk '{printf "%.1f%%\n", ($3/$2) * 100.0}')"
echo "Temperature: $(vcgencmd measure_temp 2>/dev/null | cut -d= -f2 || echo 'N/A')"

echo ""
echo -e "${CYAN}Available Commands:${NC}"
echo "./start.sh    - Start dashboard"
echo "./stop.sh     - Stop dashboard"
echo "./restart.sh  - Restart dashboard"
echo "./status.sh   - Check status"
echo "./install.sh  - Full installation"
echo ""