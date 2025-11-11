#!/bin/bash

# OBLIRIM TUI - Post-Fix Testing Checklist
# Run this to verify all fixes are working correctly

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║     OBLIRIM TUI - Post-Fix Testing Checklist            ║"
echo "╔══════════════════════════════════════════════════════════╗"
echo -e "${NC}"
echo ""

PASS=0
FAIL=0

check_pass() {
    echo -e "${GREEN}✓ PASS${NC} - $1"
    ((PASS++))
}

check_fail() {
    echo -e "${RED}✗ FAIL${NC} - $1"
    ((FAIL++))
}

check_info() {
    echo -e "${CYAN}ℹ INFO${NC} - $1"
}

echo -e "${YELLOW}AUTOMATED CHECKS${NC}"
echo "────────────────────────────────────────────────────────"

# Check 1: File exists
if [ -f "tui_app.py" ]; then
    check_pass "tui_app.py exists"
else
    check_fail "tui_app.py not found"
fi

# Check 2: Syntax valid
if python3 -m py_compile tui_app.py 2>/dev/null; then
    check_pass "Python syntax valid"
else
    check_fail "Syntax errors detected"
fi

# Check 3: Dependencies
if [ -d ".venv" ]; then
    source .venv/bin/activate
    if python3 -c "import textual, psutil" 2>/dev/null; then
        check_pass "Dependencies installed (textual, psutil)"
    else
        check_fail "Missing dependencies"
    fi
else
    check_fail "Virtual environment not found"
fi

# Check 4: Import test
if python3 -c "from tui_app import OblirimTUI" 2>/dev/null; then
    check_pass "TUI imports successfully"
else
    check_fail "Import errors detected"
fi

# Check 5: Key code patterns
if grep -q "call_later(self.initial_update)" tui_app.py; then
    check_pass "Immediate update code present"
else
    check_fail "Missing immediate update code"
fi

if grep -q "ctrl+c.*quit" tui_app.py; then
    check_pass "Ctrl+C exit binding present"
else
    check_fail "Missing Ctrl+C binding"
fi

if grep -q "def on_unmount" tui_app.py; then
    check_pass "Cleanup handler present"
else
    check_fail "Missing cleanup handler"
fi

if grep -q "Loading system stats" tui_app.py; then
    check_pass "Loading placeholders present"
else
    check_fail "Missing loading placeholders"
fi

echo ""
echo -e "${YELLOW}MANUAL VERIFICATION REQUIRED${NC}"
echo "────────────────────────────────────────────────────────"
echo ""
echo "Please test these manually by running: ./test-tui-simple.sh"
echo ""
echo -e "${CYAN}□${NC} 1. Data displays immediately on startup (within 1 second)"
echo -e "${CYAN}□${NC} 2. System stats show: Model, IP, interfaces, CPU, RAM, Disk"
echo -e "${CYAN}□${NC} 3. Ethernet status shows: Connection state, metrics"
echo -e "${CYAN}□${NC} 4. Logs section shows helpful message or actual logs"
echo -e "${CYAN}□${NC} 5. Press 'q' - TUI exits cleanly"
echo -e "${CYAN}□${NC} 6. Press Ctrl+C - TUI exits cleanly"
echo -e "${CYAN}□${NC} 7. Terminal shows 'OBLIRIM TUI exited cleanly' on exit"
echo -e "${CYAN}□${NC} 8. Press 'r' - Display refreshes immediately"
echo ""

echo "────────────────────────────────────────────────────────"
echo -e "${YELLOW}AUTOMATED CHECK RESULTS${NC}"
echo "────────────────────────────────────────────────────────"
echo -e "${GREEN}Passed: $PASS${NC}"
if [ $FAIL -gt 0 ]; then
    echo -e "${RED}Failed: $FAIL${NC}"
else
    echo -e "Failed: $FAIL"
fi
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗"
    echo "║   All automated checks passed!                          ║"
    echo "║   Ready for manual testing.                             ║"
    echo "╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}Next steps:${NC}"
    echo "  1. Run: ./test-tui-simple.sh"
    echo "  2. Verify the 8 manual checks above"
    echo "  3. Check docs/TUI_VISUAL_REFERENCE_FIXED.md for what to expect"
    echo ""
    exit 0
else
    echo -e "${RED}╔══════════════════════════════════════════════════════════╗"
    echo "║   Some checks failed!                                   ║"
    echo "║   Please review errors above.                           ║"
    echo "╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}Troubleshooting:${NC}"
    echo "  - Run: pip install -r requirements.txt"
    echo "  - Check: python3 tui_app.py (for detailed errors)"
    echo "  - See: docs/TUI_FIXES.md for technical details"
    echo ""
    exit 1
fi
