#!/usr/bin/env python3
"""
Standalone TUI Test
Tests the TUI without requiring full backend or Ethernet connectivity
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print("OBLIRIM TUI - Standalone Test")
print("="*60)
print()
print("This test will launch the TUI in standalone mode.")
print("The TUI should display:")
print("  - System stats (CPU, RAM, Disk, etc.)")
print("  - Ethernet status (may show DISCONNECTED)")
print("  - Logs section")
print()
print("Controls:")
print("  q or Ctrl+C - Exit the TUI")
print("  r - Refresh display")
print("  s - Start scan (requires Ethernet)")
print()
print("Press Ctrl+C to exit at any time.")
print("="*60)
print()

# Import and run the TUI
try:
    from tui_app import OblirimTUI
    
    print("Starting TUI...")
    app = OblirimTUI()
    app.run()
    
    print("\n" + "="*60)
    print("TUI exited successfully!")
    print("="*60)
    
except KeyboardInterrupt:
    print("\n\nInterrupted by user - exiting cleanly")
    sys.exit(0)
except ImportError as e:
    print(f"\nERROR: Missing dependency - {e}")
    print("\nPlease ensure textual is installed:")
    print("  pip install textual")
    sys.exit(1)
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
