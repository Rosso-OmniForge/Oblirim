#!/bin/bash

# OBLIRIM Installation Verification Script
# Checks all components are properly installed and configured

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}OBLIRIM Installation Verification${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

ERRORS=0
WARNINGS=0

# Check virtual environment
if [ -d .venv ]; then
    echo -e "${GREEN}✓${NC} Virtual environment exists"
else
    echo -e "${RED}✗${NC} Virtual environment missing"
    ((ERRORS++))
fi

# Check services
if systemctl is-enabled oblirim >/dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Main service (oblirim) enabled"
    if systemctl is-active oblirim >/dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Main service is running"
    else
        echo -e "${YELLOW}⚠${NC} Main service enabled but not running"
        ((WARNINGS++))
    fi
else
    echo -e "${RED}✗${NC} Main service (oblirim) not enabled"
    ((ERRORS++))
fi

if systemctl is-enabled oblirim-tui >/dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} TUI service (oblirim-tui) enabled"
    if systemctl is-active oblirim-tui >/dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} TUI service is running"
    else
        echo -e "${YELLOW}⚠${NC} TUI service enabled but not running (may be waiting for HDMI)"
        ((WARNINGS++))
    fi
else
    echo -e "${RED}✗${NC} TUI service (oblirim-tui) not enabled"
    ((ERRORS++))
fi

# Check tools
echo ""
echo -e "${BLUE}Checking penetration testing tools:${NC}"
REQUIRED_TOOLS=("nmap" "nikto")
OPTIONAL_TOOLS=("sslscan" "onesixtyone" "nbtscan")

for tool in "${REQUIRED_TOOLS[@]}"; do
    if command -v $tool >/dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} $tool installed (REQUIRED)"
    else
        echo -e "${RED}✗${NC} $tool missing (REQUIRED)"
        ((ERRORS++))
    fi
done

for tool in "${OPTIONAL_TOOLS[@]}"; do
    if command -v $tool >/dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} $tool installed (optional)"
    else
        echo -e "${YELLOW}⚠${NC} $tool missing (optional - some features limited)"
        ((WARNINGS++))
    fi
done

# Check Python packages
echo ""
echo -e "${BLUE}Checking Python packages:${NC}"
if [ -d .venv ]; then
    source .venv/bin/activate 2>/dev/null
    
    PACKAGES=("flask" "textual" "psutil" "netifaces")
    for pkg in "${PACKAGES[@]}"; do
        if python -c "import $pkg" 2>/dev/null; then
            echo -e "${GREEN}✓${NC} $pkg installed"
        else
            echo -e "${RED}✗${NC} $pkg missing"
            ((ERRORS++))
        fi
    done
    
    deactivate 2>/dev/null
else
    echo -e "${RED}✗${NC} Cannot check packages - venv missing"
    ((ERRORS++))
fi

# Check directories
echo ""
echo -e "${BLUE}Checking directory structure:${NC}"
DIRS=("logs" "logs/eth" "data" "memory" "components" "templates")
for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓${NC} $dir/ exists"
    else
        echo -e "${YELLOW}⚠${NC} $dir/ missing (will be created on start)"
        ((WARNINGS++))
    fi
done

# Check HDMI detection script
if [ -f /usr/local/bin/check-hdmi.sh ]; then
    echo -e "${GREEN}✓${NC} HDMI detection script installed"
else
    echo -e "${YELLOW}⚠${NC} HDMI detection script not found (TUI will always start)"
    ((WARNINGS++))
fi

# Check network access
echo ""
echo -e "${BLUE}Checking network configuration:${NC}"
LOCAL_IP=$(hostname -I | awk '{print $1}')
if [ -n "$LOCAL_IP" ]; then
    echo -e "${GREEN}✓${NC} Local IP: $LOCAL_IP"
    echo -e "${BLUE}ℹ${NC} Web UI should be accessible at: http://$LOCAL_IP:5000"
else
    echo -e "${YELLOW}⚠${NC} No IP address assigned"
fi

# Summary
echo ""
echo -e "${BLUE}========================================${NC}"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ Verification PASSED${NC}"
    echo -e "${GREEN}  0 errors, $WARNINGS warnings${NC}"
    echo ""
    echo -e "${BLUE}Installation is complete and ready for use!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Reboot the system: sudo reboot"
    echo "2. Services will start automatically"
    echo "3. Access web UI at: http://$LOCAL_IP:5000"
    exit 0
else
    echo -e "${RED}✗ Verification FAILED${NC}"
    echo -e "${RED}  $ERRORS errors, $WARNINGS warnings${NC}"
    echo ""
    echo "Please fix the errors above before using the system"
    exit 1
fi
