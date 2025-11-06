# OBLIRIM - Ethernet Penetration Testing Interface

**⚠️ FOR TESTING ONLY - NOT A FUCKING TOY ⚠️**

A high-performance, always-running Ethernet penetration testing web interface designed for Raspberry Pi. Features automatic network detection, structured logging, comprehensive 4-phase vulnerability assessment workflow, and real-time progress tracking with historical metrics.

## 🚀 Key Features

### 🔍 **Auto-Detection & Auto-Scan**
- **Automatic Ethernet monitoring** via background daemon
- **Auto-trigger scans** immediately when eth0 gets IP address
- **Real-time progress display** visible on dashboard without interaction
- **Network-specific metrics** with Current/Historical tracking (CPT/HPT format)
- **Persistent data** across reconnections to same network

### 📊 **Live Dashboard** 
- **50/50 Split Layout**: System Stats | Ethernet Status
- **Real-time Metrics**: Hosts, Ports, Vulnerabilities (Current vs Historical)
- **Live Progress Bar**: Shows scan progress even when page loads mid-scan
- **Phase Indicators**: Visual 4-phase progress with active animations
- **Network Blocking Detection**: Alerts when network filtering detected

### 🎯 **4-Phase Penetration Testing Workflow**

#### **Phase 1: Network Detection & Initialization** (10% - 20%)
- Interface detection (`ip link show eth0`)
- IP acquisition and subnet calculation
- Gateway and DNS enumeration
- RFC1918 classification
- Network metrics initialization

#### **Phase 2: Host Discovery** (20% - 40%)
- `nmap -sn` ping sweep across subnet
- Live host identification  
- Host count tracking and metrics update

#### **Phase 3: Service Enumeration** (40% - 70%)
- TCP connect scans (`nmap -sT -T4 --top-ports 100 -Pn`)
- Service version detection (`nmap -sV -sC -Pn`)
- Port discovery and cataloging
- Per-host metrics tracking

#### **Phase 4: Vulnerability Assessment** (70% - 100%)
- Web vulnerability scanning (`nikto -maxtime 30`)
- SMB enumeration (`enum4linux` if available)
- SNMP discovery (`onesixtyone`)
- SSL/TLS assessment (`sslscan`)
- Vulnerability counting and historical tracking
- TCP SYN scan (`nmap -sS -T4`)
- Service version detection (`nmap -sV -sC`)
- UDP top ports scan (`nmap -sU`)
- Protocol-specific enumeration

#### **Phase 4: Vulnerability Scanning**
- **HTTP/HTTPS**: nikto, dirb, sslscan
- **SSH**: nmap SSH scripts
- **SMB**: enum4linux, smb-vuln-*
- **SNMP**: snmp-check, onesixtyone
- **FTP**: Anonymous access checks
- Results parsed and logged to README

### 📊 **Tab-Specific Logging**
- **Markdown-formatted logs** in `/logs/eth/README.md`
- **Session IDs**: `YYYY-MM-DD_HH:MM_[network]`
- **Phase tracking** with timestamps
- **Vulnerability summaries** with severity ratings
- **Full scan output** preservation

### 🖥️ **Real-Time Dashboard**
- **Live progress bars** for scan phases
- **Connection status** with IP/gateway info
- **Device counters**: hosts, ports, vulnerabilities
- **Console log streaming** via WebSocket
- **Expandable host cards** (planned)

### 🎨 **Optimized Design**
- **Lightweight hacker theme** (green/cyan terminal aesthetic)
- **Portrait-optimized** for 1080x1920 touchscreen displays
- **Raspberry Pi 3+ compatible** with performance optimizations
- **Mobile-responsive** interface

## 📦 Installation

### **Quick Install (Recommended)**
```bash
# Clone the repository
git clone https://github.com/Rosso-OmniForge/Oblirim.git
cd Oblirim

# Run installation script
chmod +x install.sh
./install.sh

# Reboot after installation
sudo reboot
```

### **What Gets Installed**
1. ✅ System dependencies (Python 3, pip, git, etc.)
2. ✅ Python virtual environment
3. ✅ Flask + SocketIO web framework
4. ✅ **Penetration testing tools** (nmap, nikto, sslscan, etc.)
5. ✅ Systemd service for auto-start
6. ✅ Configures autostart on boot
7. ✅ **Ready after reboot!**

### **Penetration Testing Tools Installed**
- `nmap` - Network scanner ⭐ **REQUIRED**
- `nikto` - Web vulnerability scanner ⭐ **REQUIRED**
- `sslscan` - SSL/TLS configuration analyzer
- `onesixtyone` - SNMP scanner
- `nbtscan` - NetBIOS scanner
- `snmp` - SNMP tools
- `dirb` - Web content scanner
- `masscan` - Ultra-fast port scanner
- _(enum4linux and snmp-check unavailable in default repos)_

### **Manual Tool Installation**
If tools are missing after install:
```bash
sudo apt-get update
sudo apt-get install -y nmap nikto sslscan onesixtyone nbtscan snmp
```

## 🎯 System Requirements

### **Minimum Requirements**
- **Raspberry Pi 3B+** or newer (Pi 4/5 recommended)
- **Raspberry Pi OS Bookworm** (Debian 12)
- **2GB RAM** (4GB+ recommended for heavy scans)
- **16GB SD card** (32GB+ recommended)
- **Python 3.9+**
- **Ethernet connection** (eth0)

### **Tested Systems**
- ✅ Raspberry Pi 5 (8GB) - Bookworm
- ✅ Raspberry Pi 4B (4GB) - Bookworm  
- ✅ Raspberry Pi 3B+ (1GB) - Bookworm
- ✅ Generic Linux x86_64 - Ubuntu/Debian

### **Network Requirements**
- **Ethernet (eth0)** for target network scanning
- **Port 5000** open for web access
- **WebSocket support** in browser
- **Authorized testing environment ONLY**

## 🖥️ Usage

### **Automatic Operation (HDMI Display)**
The system is designed for **hands-free operation**:

1. **Power on Raspberry Pi** with HDMI display connected
2. **Wait ~30 seconds** for boot and service start
3. **Connect Ethernet cable** to target network (eth0)
4. **Dashboard auto-opens** in Chromium (kiosk mode)
5. **Scan auto-starts** when IP is assigned
6. **Progress visible** immediately on dashboard
7. **Metrics update** in real-time (CPT/HPT format)

### **Manual Access**
- **Local**: http://localhost:5000
- **Network**: http://YOUR_PI_IP:5000  
- **Android/Mobile**: Connect via network and browse to Pi IP

### **Understanding the Dashboard**

**Left Panel - System Stats:**
- Pi Model, IP Address, CPU, Memory, Disk
- Network interface statuses (eth0, wlan0, wlan1, BT)
- Temperature monitoring

**Right Panel - Ethernet Status:**
- Connection state and network info
- **Current scan progress** with phase indicators
- **Metrics in CPT/HPT format:**
  - `Hosts: 10/45` = Current 10, Historical Total 45
  - `Ports: 23/187` = Current 23, Historical Total 187
  - `Vulns: 3/28` = Current 3, Historical Total 28
- Network blocking detection alerts

### **Control Scripts**
```bash
./launch.sh     # Start the dashboard (manual mode)
./stop.sh       # Stop all services
./restart.sh    # Restart the dashboard
```

### **ETH Tab Features**
- Full scan progress with 4-phase breakdown
- Detailed metrics with historical comparison
- Real-time log viewer (auto-scrolling)
- Per-network session tracking

### **Dashboard Tabs**
- **DASH** - System statistics and connection status
- **ETH** - Ethernet scanning tools and results
- **WLAN** - Wireless network tools (coming soon)
- **BLT** - Bluetooth tools (coming soon)
- **CONFIG** - Configuration management

### **Ethernet Tab Features**
1. **Connection Status** - Real-time eth0 state monitoring
2. **Network Info** - IP, gateway, networks scanned counter
3. **Manual Scan** - Start penetration testing workflow on-demand
4. **Progress Tracking** - Live progress bar for scan phases
5. **Log Viewer** - Recent scan results and session logs
6. **Device Statistics** - Hosts found, open ports, vulnerabilities

## 🔧 Manual Installation

If you prefer to install manually:

### **1. System Preparation**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv git \
  nmap arp-scan nikto dirb sslscan enum4linux -y
```

### **2. Clone Repository**
```bash
git clone https://github.com/Rosso-OmniForge/Oblirim.git
cd Oblirim
```

### **3. Setup Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **4. Test Installation**
```bash
python app.py
# Access http://localhost:5000
```

### **5. Configure Auto-Start (Optional)**
```bash
# Use the install.sh script for full auto-start setup
./install.sh
```

## 📁 Project Structure

```
oblirim/
├── app.py                      # Flask application & SocketIO server
├── components/
│   ├── eth_detector.py         # Ethernet detection daemon
│   ├── eth_workflow.py         # 4-phase workflow engine
│   ├── tab_logger.py           # Tab-specific README logger
│   └── system_specs_component.py
├── templates/
│   └── index.html              # Main dashboard UI
├── static/                     # CSS/JS assets (if any)
├── logs/
│   └── eth/
│       └── README.md           # Ethernet scan logs
├── data/
│   └── network_tally.json      # Network counter
├── tools/                      # Tool output directory
├── install.sh                  # Automated installer
├── start.sh / stop.sh          # Control scripts
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔧 Configuration

### **Data Directory**
The `data/` folder contains:
- `network_tally.json` - Persistent network counter

### **Logs Directory**
The `logs/eth/` folder contains:
- `README.md` - Structured session logs with scan results

### **Session Log Format**
```markdown
## Session: 2025-11-06_22:45_192-168-1-0
- **Network:** 192.168.1.0/24
- **Started:** 2025-11-06 22:45:12
- **Interface:** eth0 (up)
- **IP:** 192.168.1.100/24
- **Gateway:** 192.168.1.1
- **Phase 1:** Network detected and classified
- **Phase 2:** nmap -sn → 8 hosts
- **Phase 3:** Full port scan completed
- **Phase 4:** nikto found 3 vulns on 192.168.1.15
- **Completed:** 2025-11-06 23:10:05
- **Summary:** 8 hosts scanned, 23 open ports, 12 vulnerabilities

---
```

### **Service Management**
```bash
# System service control
sudo systemctl start oblirim
sudo systemctl stop oblirim
sudo systemctl restart oblirim
sudo systemctl status oblirim

# View real-time logs
sudo journalctl -u oblirim -f
```

## 🚨 Troubleshooting

### **Installation Issues**
```bash
# Permission errors
sudo chown -R $USER:$USER ~/Oblirim

# Python issues  
sudo apt install python3-dev python3-pip python3-venv

# Missing dependencies
./install.sh  # Re-run installer
```

### **Runtime Issues**
```bash
# Check service status
./status.sh

# View detailed logs
sudo journalctl -u oblirim --no-pager -n 50

# Test manual startup
source venv/bin/activate && python app.py
```

### **Network Access Issues**
```bash
# Check firewall
sudo ufw status
sudo ufw allow 5000

# Check IP address
hostname -I

# Test local access
curl http://localhost:5000
```

### **Ethernet Detection Issues**
```bash
# Check eth0 status
ip link show eth0
cat /sys/class/net/eth0/carrier

# Verify permissions
ls -la /sys/class/net/eth0/

# Check daemon logs
grep "Ethernet" ~/Oblirim/logs/*.log
```

### **Tool Installation Issues**
```bash
# Verify tools are installed
which nmap arp-scan nikto

# Manually install missing tools
sudo apt install nmap arp-scan nikto dirb sslscan enum4linux

# Test tool execution
nmap --version
```

### **Performance Issues**
- **For Pi 3**: Some scans may be slower, adjust timeout values
- **High CPU**: Large scans can spike CPU to 80%+, this is normal
- **Memory issues**: Restart the service: `./restart.sh`
- **Scan timeouts**: Check network connectivity to target

## ⚖️ Legal & Ethical Use

### **⚠️ IMPORTANT DISCLAIMER**

This tool is designed for **authorized security testing ONLY**. Use of this software for:
- Unauthorized network scanning
- Attacking systems you don't own or have permission to test
- Any illegal activity

...is **STRICTLY PROHIBITED** and may violate laws including:
- Computer Fraud and Abuse Act (USA)
- Computer Misuse Act (UK)
- Similar laws in your jurisdiction

### **Proper Usage**
✅ **Authorized penetration testing** on your own networks  
✅ **Security audits** with written permission  
✅ **Educational purposes** in controlled lab environments  
✅ **Bug bounty programs** within their scope  

❌ **Scanning networks without permission**  
❌ **Attacking production systems**  
❌ **Port scanning public IPs without authorization**  

**The developers assume NO responsibility for misuse of this software.**

## 🔄 Updates

### **Update Application**
```bash
cd ~/Oblirim
git pull
source venv/bin/activate
pip install -r requirements.txt --upgrade
./restart.sh
```

### **Update System**
```bash
sudo apt update && sudo apt upgrade -y
sudo reboot
```

## 🗑️ Uninstallation

```bash
./uninstall.sh
```

This will:
- Stop and remove the systemd service
- Optionally remove project files
- Clean up system configuration
- Preserve logs (optional)

## 🤝 Contributing

### **Development Setup**
```bash
git clone https://github.com/Rosso-OmniForge/Oblirim.git
cd Oblirim
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### **Adding Features**
1. Create components in `components/`
2. Add routes in `app.py`
3. Update templates in `templates/`
4. Test on Pi 3/4/5 hardware
5. Update logs in `/logs/[tab]/README.md`

### **Workflow Engine Extension**
To add new scan phases:
1. Edit `components/eth_workflow.py`
2. Add phase function: `phase_N_description()`
3. Call in `run_workflow()` method
4. Update progress callbacks
5. Add logging via `tab_logger`

## 📝 Technical Details

### **Ethernet Detection Mechanism**
- Polls `/sys/class/net/eth0/carrier` every 3 seconds
- Non-blocking threading implementation
- State change triggers workflow callbacks
- Persistent session tracking

### **Workflow Architecture**
- **Modular phases** for easy extension
- **Async execution** via threading
- **Progress callbacks** for real-time UI updates
- **Structured logging** to Markdown files
- **Tool verification** on startup

### **Security Considerations**
- All scans run with user permissions (no root)
- Tools installed system-wide for stability
- Timeout protection on all subprocess calls
- Rate limiting to prevent Pi overload
- Logs preserved for audit trails

## 📚 Resources

### **Documentation**
- [NMAP Documentation](https://nmap.org/book/man.html)
- [Nikto User Guide](https://cirt.net/Nikto2)
- [Raspberry Pi Setup](https://www.raspberrypi.com/documentation/)

### **Related Projects**
- Kali Linux - Penetration testing distribution
- OpenVAS - Vulnerability scanner
- Metasploit Framework - Exploitation framework

## 📜 License

This project is provided for educational and authorized security testing purposes only.

**MIT License** - See LICENSE file for details.

## 🆘 Support

- **Issues**: Report bugs via [GitHub Issues](https://github.com/Rosso-OmniForge/Oblirim/issues)
- **Documentation**: Check this README
- **Logs**: Use `./status.sh` for diagnostics

## 🙏 Credits

Built with:
- Flask & SocketIO for real-time web interface
- Python 3 for backend logic
- Bootstrap-inspired CSS for UI
- NMAP, Nikto, and other open-source security tools

---

**OBLIRIM** - Ethernet Penetration Testing Interface  
🔐 For authorized security testing on Raspberry Pi  
⚠️ **Use responsibly. Test only authorized networks.**