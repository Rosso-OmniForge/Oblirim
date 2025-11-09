#!/bin/bash
set -e

# -------------------------------------------------
# DEPRECATED - This script is no longer used
# -------------------------------------------------
# OBLIRIM now uses a lightweight Textual TUI instead
# of Chromium kiosk mode for better performance on Pi.
#
# The TUI runs directly on the console (tty1) and
# displays on HDMI without requiring X11 or Chromium.
#
# To install OBLIRIM with TUI, use: ./install.sh
# -------------------------------------------------

echo "================================================"
echo "  DEPRECATED: Chromium Kiosk Mode"
echo "================================================"
echo ""
echo "This script is no longer used. OBLIRIM now uses"
echo "a lightweight Textual-based TUI that runs on"
echo "the console instead of requiring Chromium."
echo ""
echo "Benefits of the new TUI:"
echo "  • Much lower resource usage (no X11/Chromium)"
echo "  • More stable on Raspberry Pi"
echo "  • Faster boot times"
echo "  • No browser overhead"
echo ""
echo "To install OBLIRIM with the new TUI:"
echo "  ./install.sh"
echo ""
echo "To manually start the TUI:"
echo "  sudo systemctl start oblirim-tui"
echo ""
echo "================================================"
exit 1