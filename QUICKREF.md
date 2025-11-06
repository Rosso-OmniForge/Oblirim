# OBLIRIM - Quick Reference Guide

## 🚀 Quick Start Commands

```bash
# Start the application
./start.sh

# Stop the application  
./stop.sh

# Restart the application
./restart.sh

# Check status and logs
./status.sh

# Test installation
./test-installation.sh
```

## 🌐 Access URLs

- **Local**: http://localhost:5000
- **Network**: http://YOUR_PI_IP:5000
- **Default Port**: 5000

## 📊 Dashboard Tabs

| Tab | Purpose |
|-----|---------|
| **DASH** | System statistics, network status |
| **ETH** | Ethernet penetration testing |
| **WLAN** | Wireless network tools (coming soon) |
| **BLT** | Bluetooth tools (coming soon) |
| **CONFIG** | Configuration management |

## 🔍 Ethernet Tab Features

1. **Connection Status** - Real-time eth0 monitoring
2. **Network Info** - IP, gateway, networks scanned
3. **Start ETH Scan** - Manual workflow trigger
4. **Progress Bar** - Live scan progress
5. **Log Viewer** - Session results

## 📁 Important Paths

```
~/Oblirim/
├── logs/eth/README.md    # Scan logs
├── data/network_tally.json  # Network counter
├── venv/                 # Virtual environment
└── app.py                # Main application
```

## 🛠️ Troubleshooting Commands

```bash
# Check if service is running
sudo systemctl status oblirim

# View real-time logs
sudo journalctl -u oblirim -f

# Restart service
sudo systemctl restart oblirim

# Check network interfaces
ip link show eth0
cat /sys/class/net/eth0/carrier

# Test tools installation
nmap --version
arp-scan --version
nikto --version

# Check Python environment
source venv/bin/activate
pip list | grep -i flask
```

## 🔧 Tool Verification

```bash
# Verify all tools are installed
which nmap arp-scan nikto dirb sslscan enum4linux

# Test nmap
nmap --version

# Test network access
ping -c 1 8.8.8.8

# Check eth0 status
ip addr show eth0
```

## 📝 Log Locations

- **Application logs**: `/var/log/syslog` or `journalctl -u oblirim`
- **Scan logs**: `~/Oblirim/logs/eth/README.md`
- **Network tally**: `~/Oblirim/data/network_tally.json`

## ⚙️ Configuration

### Service Configuration
```bash
# Service file location
/etc/systemd/system/oblirim.service

# Reload service after changes
sudo systemctl daemon-reload
sudo systemctl restart oblirim
```

### Network Configuration
```bash
# Open firewall port
sudo ufw allow 5000/tcp

# Check firewall status
sudo ufw status
```

## 🐛 Common Issues & Solutions

### Issue: "Permission denied" on /sys/class/net
```bash
# Check permissions
ls -la /sys/class/net/eth0/

# This is normal - read access is sufficient
```

### Issue: Tools not found
```bash
# Install missing tools
sudo apt update
sudo apt install nmap arp-scan nikto dirb sslscan enum4linux
```

### Issue: Virtual environment not activated
```bash
# Activate venv
source venv/bin/activate

# Verify
which python
# Should show: ~/Oblirim/venv/bin/python
```

### Issue: Port 5000 already in use
```bash
# Find process using port 5000
sudo lsof -i :5000

# Kill the process
sudo kill -9 [PID]

# Or change port in app.py
```

## 📊 Scan Workflow Phases

1. **Phase 1: Network Detection** - Interface detection, IP acquisition
2. **Phase 2: Host Discovery** - nmap, arp-scan
3. **Phase 3: Service Enumeration** - Port scanning, service detection
4. **Phase 4: Vulnerability Scanning** - nikto, enum4linux, etc.

## 🔐 Security Best Practices

- ✅ Only scan authorized networks
- ✅ Keep logs for audit trails
- ✅ Use strong passwords if exposing to network
- ✅ Monitor system resources during scans
- ❌ Never scan public IPs without permission
- ❌ Don't expose port 5000 to the internet without authentication

## 📞 Getting Help

```bash
# Check application status
./status.sh

# View recent logs (last 50 lines)
sudo journalctl -u oblirim -n 50

# Test installation
./test-installation.sh

# Manual startup for debugging
source venv/bin/activate
python app.py
```

## 🔄 Update Process

```bash
# Pull latest changes
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Restart application
./restart.sh
```

---

**For full documentation, see README.md**
