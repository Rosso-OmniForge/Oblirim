# OBLIRIM - Quick Reference Guide

## 📦 Installation

```bash
git clone https://github.com/Rosso-OmniForge/Oblirim.git
cd Oblirim
./install.sh
./verify-install.sh  # Check installation
sudo reboot
```

---

## 🎮 Control Commands

### Backend Server (Web UI)
```bash
./launch.sh          # Start backend
./stop.sh            # Stop backend
./restart.sh         # Restart backend
sudo journalctl -u oblirim -f  # View logs
```

### TUI Display (HDMI)
```bash
sudo systemctl start oblirim-tui     # Start TUI
sudo systemctl stop oblirim-tui      # Stop TUI
sudo systemctl restart oblirim-tui   # Restart TUI
sudo journalctl -u oblirim-tui -f    # View logs
```

### Both Services
```bash
sudo systemctl status oblirim oblirim-tui  # Check status
```

---

## 🌐 Access

- **Local:** http://localhost:5000
- **Network:** http://YOUR_PI_IP:5000
- **TUI:** Automatically on HDMI display (tty1)

---

## 🔧 Service Management

### Enable/Disable Auto-Start
```bash
sudo systemctl enable oblirim       # Enable backend
sudo systemctl disable oblirim      # Disable backend
sudo systemctl enable oblirim-tui   # Enable TUI
sudo systemctl disable oblirim-tui  # Disable TUI
```

### Check Service Status
```bash
systemctl is-enabled oblirim
systemctl is-active oblirim
```

---

## 🧪 Testing

```bash
cd testing/
./test-tui-simple.sh        # Test TUI
./verify-tui-fixes.sh       # Verify TUI fixes
./START_HERE.sh             # TUI quick start guide
```

---

## 🗑️ Uninstallation

```bash
./uninstall.sh
```

**This will:**
- Stop all services
- Remove systemd service files
- Optionally remove packages
- Optionally remove project files
- Reset system to base OS

---

## 📁 File Organization

### Root Directory (Core Scripts Only)
- `install.sh` - Installation script (ONLY ONE)
- `uninstall.sh` - Complete removal
- `verify-install.sh` - Installation verification
- `check-hdmi.sh` - HDMI detection
- `launch.sh` - Backend control
- `stop.sh` - Backend control
- `restart.sh` - Backend control
- `launch-tui.sh` - Manual TUI launcher

### Testing Directory
- All test scripts in `testing/`
- Symlinks in root for convenience

### Deprecated
- `server_install.sh.deprecated` - Don't use

---

## 🔍 Troubleshooting

### Service Won't Start
```bash
sudo systemctl status oblirim
sudo journalctl -u oblirim -n 50
./verify-install.sh
```

### TUI Not Showing
```bash
# Check HDMI detection
/usr/local/bin/check-hdmi.sh
echo $?  # Should be 0 if HDMI detected

# Check service
sudo systemctl status oblirim-tui

# Check logs
sudo journalctl -u oblirim-tui -n 50
```

### Network Access Issues
```bash
# Check IP
hostname -I

# Test local
curl http://localhost:5000

# Test network
curl http://YOUR_PI_IP:5000

# Check firewall
sudo ufw status
```

### Ethernet Not Detecting
```bash
# Check interface
ip link show eth0

# Check logs
sudo journalctl -u oblirim -f | grep -i eth

# Manual test
cd testing/
./test-installation.sh
```

---

## 📊 Verification

After installation:
```bash
./verify-install.sh
```

Should show:
- ✓ Virtual environment exists
- ✓ Main service enabled
- ✓ TUI service enabled
- ✓ nmap installed
- ✓ nikto installed
- ✓ Python packages installed
- ✓ Directories exist

---

## 🚀 Production Checklist

Before deploying:
- [ ] Fresh OS installation tested
- [ ] `./verify-install.sh` passes
- [ ] Reboot test successful
- [ ] Services auto-start
- [ ] TUI displays correctly
- [ ] Web UI accessible from network
- [ ] Ethernet auto-scan works
- [ ] Logs are being created

---

## 📞 Support

- **Issues:** GitHub Issues
- **Documentation:** `docs/` folder
- **Audit Report:** `PROJECT_AUDIT_REPORT.md`
- **Fixes Log:** `FIXES_IMPLEMENTED.md`

---

## ⚠️ Important Notes

1. **launch.sh, stop.sh, restart.sh** control BACKEND ONLY (not TUI)
2. TUI is controlled via `systemctl` commands
3. TUI only starts if HDMI display is connected
4. Backend binds to `0.0.0.0` (network accessible)
5. Services auto-start on boot (if enabled)
6. Virtual environment must exist before services start
7. TTY permissions granted via `tty` group membership

---

## 🎯 Key Differences From Before

**OLD:**
- Two installation scripts (confusing)
- launch/stop/restart affected everything
- No HDMI detection (waste resources)
- Backend failed to bind (bnep0 issue)
- Services could fail silently
- No verification script

**NEW:**
- ONE installation script
- Clear separation: Backend vs TUI control
- HDMI detection (smart resource usage)
- Reliable backend binding (0.0.0.0)
- Services verified before reboot
- Comprehensive verification script

---

**Last Updated:** November 11, 2025
