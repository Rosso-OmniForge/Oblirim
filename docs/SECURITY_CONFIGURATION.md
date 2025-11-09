# OBLIRIM Security Configuration

## Overview
This document describes the security configuration implemented to ensure:
1. TUI displays automatically on HDMI at boot (after server starts)
2. Web UI is only accessible via Bluetooth PAN network
3. Web UI is blocked from Ethernet and WiFi interfaces

## Changes Made

### 1. TUI Auto-Start Configuration (`install.sh`)

**File**: `oblirim-tui.service`

The TUI service now includes:
- `ExecStartPre` directive that waits for the main server to be ready
- Polls `http://localhost:5000` until it responds before starting TUI
- Ensures TUI only displays after the Flask server is fully operational

```systemd
[Unit]
After=oblirim.service
Requires=oblirim.service

[Service]
ExecStartPre=/bin/bash -c 'until curl -sf http://localhost:5000 > /dev/null; do sleep 1; done'
ExecStart=/path/to/.venv/bin/python /path/to/tui_app.py
```

### 2. Web UI Binding Configuration (`app.py`)

**Changed**: Flask server binding behavior

The server now:
- Checks for Bluetooth PAN interface (`bnep0`) availability
- Binds to `bnep0` IP address when Bluetooth is connected
- Falls back to `127.0.0.1` (localhost) when Bluetooth is not connected
- **Never binds to `0.0.0.0`** (all interfaces)

This ensures:
- TUI can always access the server via localhost
- Web UI is only accessible when Bluetooth PAN is active
- Ethernet/WiFi clients cannot access the dashboard

**Dependencies**: Added `netifaces==0.11.0` to `requirements.txt`

### 3. Firewall Configuration (`install.sh`)

**Added**: iptables rules for network security

Three firewall rules are configured:
```bash
# Allow localhost (for TUI)
iptables -I INPUT -i lo -p tcp --dport 5000 -j ACCEPT

# Allow Bluetooth PAN interface
iptables -I INPUT -i bnep0 -p tcp --dport 5000 -j ACCEPT

# Block all other interfaces
iptables -A INPUT -p tcp --dport 5000 -j DROP
```

Rules are persisted using:
- `iptables-persistent` package (automatically installed)
- `netfilter-persistent save` command

### 4. Bluetooth PAN Setup (`install.sh`)

**Added**: Bluetooth PAN network configuration

Features:
- Bluetooth service enabled and started
- Bluetooth class set to NAP (Network Access Point): `0x020300`
- Always discoverable mode enabled
- PAN setup script created at `/usr/local/bin/setup-bt-pan.sh`
- Bluetooth interface (`bnep0`) configured with static IP: `10.0.0.1`

### 5. Uninstall Script Updates (`uninstall.sh`)

**Enhanced**: Complete cleanup of all services and configurations

Now removes:
- `oblirim-tui.service` (new TUI service)
- `oblirim-kiosk.service` (legacy kiosk service)
- `oblirim.service` (main server service)
- All iptables rules for port 5000
- UFW rules (if present)
- Bluetooth PAN setup script

## Usage Instructions

### Installation
```bash
./install.sh
```

This will:
1. Install all dependencies including `netifaces`
2. Configure Bluetooth PAN network
3. Set up firewall rules
4. Create and enable TUI and server services
5. Configure auto-start on boot

### Accessing the Web UI

**Via Bluetooth PAN**:
1. Pair your device (phone/tablet/laptop) with the Raspberry Pi
2. Connect to the Bluetooth PAN network
3. Navigate to: `http://10.0.0.1:5000`

**Via TUI** (on HDMI display):
- TUI automatically displays on boot
- Shows real-time system stats and network monitoring
- No web browser required

### Security Notes

✅ **Secure**:
- Web UI only accessible via Bluetooth PAN (when connected)
- Ethernet and WiFi clients cannot access dashboard
- Localhost access preserved for TUI functionality

⚠️ **Important**:
- Bluetooth must be paired and connected for Web UI access
- Firewall rules block all non-Bluetooth/localhost access
- Server binds to localhost when Bluetooth is disconnected

### Troubleshooting

**TUI not starting**:
```bash
# Check TUI service status
sudo systemctl status oblirim-tui

# Check TUI logs
sudo journalctl -u oblirim-tui -f
```

**Web UI not accessible via Bluetooth**:
```bash
# Check Bluetooth service
sudo systemctl status bluetooth

# Check if bnep0 interface exists
ip addr show bnep0

# Verify firewall rules
sudo iptables -L INPUT -v -n | grep 5000

# Check server binding
sudo netstat -tlnp | grep 5000
```

**Server not starting**:
```bash
# Check main service
sudo systemctl status oblirim

# View server logs
sudo journalctl -u oblirim -f
```

### Manual Configuration

**Disable Bluetooth PAN restriction** (for testing):
```bash
# Temporarily bind to all interfaces (not recommended for production)
# Edit app.py and change:
bind_host = '0.0.0.0'  # Instead of netifaces logic
```

**Remove firewall rules temporarily**:
```bash
sudo iptables -F INPUT
sudo netfilter-persistent save
```

**Re-enable firewall**:
```bash
./install.sh  # Re-run install to restore security rules
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Raspberry Pi                          │
│                                                          │
│  ┌─────────────┐         ┌──────────────┐              │
│  │   HDMI      │         │  Bluetooth   │              │
│  │  Display    │         │     PAN      │              │
│  │             │         │   (bnep0)    │              │
│  └──────┬──────┘         └──────┬───────┘              │
│         │                       │                       │
│         │ TTY1                  │ 10.0.0.1             │
│         │                       │                       │
│  ┌──────▼───────────────────────▼───────┐              │
│  │         OBLIRIM Server               │              │
│  │    Flask + SocketIO (Port 5000)      │              │
│  │                                      │              │
│  │  Binds to:                          │              │
│  │  - 127.0.0.1 (no Bluetooth)         │              │
│  │  - 10.0.0.1 (Bluetooth connected)   │              │
│  └──────────────────────────────────────┘              │
│         ▲                                               │
│         │ Blocked by iptables                          │
│         │                                               │
│  ┌──────┴────────┐  ┌──────────────┐                  │
│  │   Ethernet    │  │   WiFi       │                  │
│  │    (eth0)     │  │  (wlan0/1)   │                  │
│  └───────────────┘  └──────────────┘                  │
│         ✗                  ✗                            │
└─────────────────────────────────────────────────────────┘
```

## Boot Sequence

1. **System Boot** → `multi-user.target` reached
2. **Network Services** → Ethernet, WiFi, Bluetooth start
3. **OBLIRIM Server** (`oblirim.service`) starts
   - Server binds to localhost or bnep0 IP
   - iptables rules applied
4. **TUI Display** (`oblirim-tui.service`) starts
   - Waits for server health check (port 5000 responds)
   - Displays on TTY1 (HDMI output)

## Files Modified

- `install.sh` - Enhanced with security configurations
- `uninstall.sh` - Enhanced cleanup procedures
- `app.py` - Dynamic binding based on Bluetooth PAN
- `requirements.txt` - Added `netifaces` dependency
- `docs/SECURITY_CONFIGURATION.md` - This document

## Future Enhancements

Potential improvements:
- HTTPS/TLS support for Web UI
- Bluetooth pairing PIN enforcement
- Web UI authentication/authorization
- Rate limiting for API endpoints
- Automated Bluetooth PAN setup on device pairing
