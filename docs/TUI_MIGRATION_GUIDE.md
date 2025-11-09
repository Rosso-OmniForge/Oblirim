# OBLIRIM TUI Mode - Migration Guide

## Overview

OBLIRIM has been updated to use a lightweight **Textual TUI (Text User Interface)** instead of Chromium kiosk mode for the Raspberry Pi display. This provides significant benefits:

### Benefits of TUI Mode

✅ **Much Lower Resource Usage**
- No X11 server required
- No Chromium browser overhead
- Runs directly on console (tty1)
- Minimal RAM and CPU usage

✅ **Better Stability**
- No browser crashes
- No display server issues
- More reliable on Pi hardware
- Faster boot times

✅ **Cleaner Installation**
- No Chromium installation needed
- No X11 dependencies
- Simpler systemd services
- Easier troubleshooting

## Architecture

OBLIRIM now consists of two main components:

1. **Flask Backend** (`app.py`)
   - Runs on port 5000
   - Handles all scanning logic
   - Serves web interface for remote access
   - Manages Ethernet detection and workflows

2. **Textual TUI** (`tui_app.py`)
   - Displays on Pi's HDMI output (tty1)
   - Real-time system stats
   - Ethernet connection status
   - Scan progress visualization
   - Log viewing

## Installation

### Fresh Installation

```bash
# Clone the repository
git clone <repo-url>
cd oblirim

# Run the installer
./install.sh

# The installer will:
# - Install Python dependencies (including Textual)
# - Set up systemd services for both backend and TUI
# - Configure auto-start on boot
```

### Updating Existing Installation

If you already have OBLIRIM installed with Chromium kiosk mode:

```bash
# Update the code
git pull

# Update Python dependencies
source .venv/bin/activate
pip install -r requirements.txt

# Disable old kiosk service
sudo systemctl stop oblirim-kiosk
sudo systemctl disable oblirim-kiosk

# Create new TUI service (run the relevant part of install.sh)
# Or manually create the service - see below
```

## Manual Service Setup

If you need to manually create the TUI service:

```bash
# Create service file
sudo nano /etc/systemd/system/oblirim-tui.service
```

Add this content:

```ini
[Unit]
Description=OBLIRIM TUI Display (Textual Interface on HDMI)
After=oblirim.service
Requires=oblirim.service

[Service]
Type=simple
User=YOUR_USERNAME
Group=YOUR_USERNAME
WorkingDirectory=/path/to/oblirim
Environment=PATH=/path/to/oblirim/.venv/bin
Environment=TERM=xterm-256color
StandardInput=tty
StandardOutput=tty
TTY=/dev/tty1
ExecStart=/path/to/oblirim/.venv/bin/python /path/to/oblirim/tui_app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable oblirim-tui
sudo systemctl start oblirim-tui
```

## Usage

### Starting the TUI Manually

```bash
# Start the TUI on current terminal
./launch-tui.sh
```

### TUI Controls

- `q` - Quit the TUI
- `r` - Refresh all data
- `s` - Start manual Ethernet scan
- `Ctrl+C` - Emergency exit

### System Service Commands

```bash
# Backend service (Flask)
sudo systemctl start oblirim       # Start backend
sudo systemctl stop oblirim        # Stop backend
sudo systemctl restart oblirim     # Restart backend
sudo systemctl status oblirim      # Check status
sudo journalctl -u oblirim -f      # View logs

# TUI service (Display)
sudo systemctl start oblirim-tui   # Start TUI on tty1
sudo systemctl stop oblirim-tui    # Stop TUI
sudo systemctl restart oblirim-tui # Restart TUI
sudo systemctl status oblirim-tui  # Check status
```

### Accessing from Other Devices

The web interface is still available for remote access:

```bash
# From any device on the network
http://<pi-ip-address>:5000
```

## Display Layout

The TUI shows three main sections:

### Top Left: System Stats
- Pi model
- IP address
- Network interfaces status (WiFi0, WiFi1, ETH)
- Temperature
- CPU usage
- RAM usage
- Disk usage

### Top Right: Ethernet Status
- Connection state
- Network information (IP, Gateway, Subnet)
- Current scan metrics (hosts, ports, vulnerabilities)
- Historical metrics
- Scan progress

### Bottom: Log Viewer
- Recent Ethernet logs
- Scrollable log output
- Auto-updates every 5 seconds

## Troubleshooting

### TUI Not Displaying on HDMI

```bash
# Check if TUI service is running
sudo systemctl status oblirim-tui

# Check if running on correct TTY
ps aux | grep tui_app

# Manually switch to tty1
sudo chvt 1
```

### Backend Not Running

```bash
# Check backend status
sudo systemctl status oblirim

# Check if port 5000 is in use
sudo netstat -tulpn | grep 5000

# View backend logs
sudo journalctl -u oblirim -f
```

### TUI Shows Errors

```bash
# Check Python dependencies
source .venv/bin/activate
pip install -r requirements.txt

# Check for missing packages
python -c "import textual; print('OK')"
```

### Console Access

If you need to access the console while TUI is running:

```bash
# SSH into the Pi, then:
# Switch to tty2-6
sudo chvt 2

# To return to TUI
sudo chvt 1

# Or stop the TUI service
sudo systemctl stop oblirim-tui
```

## Migration Checklist

- [ ] Update code: `git pull`
- [ ] Update dependencies: `pip install -r requirements.txt`
- [ ] Stop old kiosk service: `sudo systemctl stop oblirim-kiosk`
- [ ] Disable old kiosk service: `sudo systemctl disable oblirim-kiosk`
- [ ] Create TUI service (see above)
- [ ] Enable TUI service: `sudo systemctl enable oblirim-tui`
- [ ] Reboot: `sudo reboot`
- [ ] Verify TUI displays on HDMI
- [ ] Verify backend is accessible via web

## Performance Comparison

### Old (Chromium Kiosk)
- RAM usage: ~500-800 MB
- CPU usage: 15-30% idle
- Boot time: ~45-60 seconds
- Dependencies: X11, Chromium, window manager

### New (Textual TUI)
- RAM usage: ~100-150 MB
- CPU usage: 2-5% idle
- Boot time: ~20-30 seconds
- Dependencies: Python, Textual

## Additional Notes

- The web interface (`app.py`) continues to run and is accessible from other devices
- The TUI is purely for local display on the Pi's HDMI output
- All scanning functionality remains the same
- The TUI updates every 2 seconds for stats and 5 seconds for logs
- The TUI uses ANSI colors and works on any standard Linux console

## Support

For issues or questions:
- Check logs: `sudo journalctl -u oblirim-tui -f`
- Verify dependencies: `pip list | grep textual`
- Test manually: `./launch-tui.sh`
