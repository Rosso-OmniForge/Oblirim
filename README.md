# OBLIRIM PWN Master Dashboard

A high-performance, hacker-aesthetic web dashboard for Raspberry Pi system monitoring with dynamic ASCII face emotions and real-time system statistics.

## 🚀 Features

### 🎭 **Dynamic Emotions System**
- **Adaptive ASCII face** that changes based on system performance
- **Real-time emotional states**: Happy, Neutral, Concerned, Stressed, Overloaded
- **Smart monitoring** of CPU usage, temperature, and memory

### 📊 **System Monitoring**
- **Real-time system specs** for Raspberry Pi 3, 4, and 5
- **Network interface status** (WiFi, Ethernet, Bluetooth)
- **Performance metrics** (CPU, Memory, Disk usage)
- **Temperature monitoring** with multiple sensor support
- **Live updates** via WebSocket connection

### 🎨 **Optimized Design**
- **Portrait-optimized layout** (1080x1920) for touchscreen displays
- **Lightweight CSS** optimized for Raspberry Pi 3 performance
- **Hacker aesthetic** with green/cyan terminal styling
- **Modular components** for easy customization

### 🔧 **Additional Tools**
- **Script runner** for automated tasks
- **Log viewer** for system monitoring
- **Network tools** for diagnostics
- **Configuration management**

## 📦 Quick Installation

### **One-Command Install**
```bash
# Download and run the installer
curl -sSL https://your-repo-url/install.sh | bash
# OR clone and install locally:
git clone <repository-url>
cd oblirim
./install.sh
```

### **What the installer does:**
1. ✅ Updates system packages
2. ✅ Installs Python 3, pip, and dependencies
3. ✅ Creates virtual environment
4. ✅ Installs Python packages
5. ✅ Configures system services (Bluetooth, SSH)
6. ✅ Creates systemd service for auto-start
7. ✅ Sets up firewall rules
8. ✅ Creates utility scripts
9. ✅ **Ready after reboot!**

## 🎯 System Requirements

### **Minimum Requirements**
- **Raspberry Pi 3B+** or newer (Pi 4/5 recommended)
- **Raspberry Pi OS Bookworm** (Debian 12)
- **1GB RAM** (2GB+ recommended)
- **8GB SD card** (16GB+ recommended)
- **Python 3.9+**

### **Tested Systems**
- ✅ Raspberry Pi 5 (8GB) - Bookworm
- ✅ Raspberry Pi 4B (4GB) - Bookworm  
- ✅ Raspberry Pi 3B+ (1GB) - Bookworm
- ✅ Generic Linux x86_64 - Ubuntu/Debian

### **Network Requirements**
- **WiFi or Ethernet** connection
- **Port 5000** open for web access
- **WebSocket support** in browser

## 🖥️ Usage

### **Access the Dashboard**
After installation and reboot:
- **Local access**: http://localhost:5000
- **Network access**: http://YOUR_PI_IP:5000
- **Mobile friendly**: Optimized for 1080x1920 displays

### **Control Scripts**
```bash
./start.sh      # Start the dashboard
./stop.sh       # Stop the dashboard  
./restart.sh    # Restart the dashboard
./status.sh     # Check status and logs
```

### **Navigation**
- **DASH** - Main dashboard with face and system specs
- **SCRIPTS** - Run automated scripts and tools
- **LOGS** - View system and application logs  
- **TOOLS** - Network diagnostics and utilities
- **CONFIG** - Configuration management

## 🔧 Manual Installation

If you prefer to install manually:

### **1. System Preparation**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv git -y
```

### **2. Clone Repository**
```bash
git clone <repository-url>
cd oblirim
```

### **3. Setup Environment**
```bash
python3 -m venv .venv
source .venv/bin/activate
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

## 🎭 Emotions System

The dashboard features an intelligent emotions system that monitors your Pi's health:

### **Emotion States**
| State | Trigger | Face | Description |
|-------|---------|------|-------------|
| **😊 Happy** | CPU < 30%, Temp < 50°C | Smiling | System running smoothly |
| **😐 Neutral** | Normal operation | Standard | Balanced performance |
| **😟 Concerned** | CPU > 70% OR Temp > 65°C | Worried | Performance degrading |
| **😰 Stressed** | CPU > 85% OR Temp > 75°C | Anxious | System under heavy load |
| **🤯 Overloaded** | CPU > 95% OR Temp > 80°C | Distressed | Critical performance issues |

### **Customization**
Edit `components/emotions.py` to:
- Add new emotional states
- Modify trigger thresholds  
- Create custom ASCII faces
- Add new monitoring parameters

## 🔧 Configuration

### **Memory Directory**
The `memory/` folder contains:
- `config.json` - Application settings
- `system_info.json` - Cached system data
- `install_progress.log` - Installation logs
- `user_settings.json` - User preferences

### **Component Structure**
```
components/
├── face.py          # ASCII face renderer
├── system_specs.py  # System information
├── emotions.py      # Emotion engine
└── css/
    ├── face.css     # Face styling
    └── specs.css    # System specs styling
```

### **Service Management**
```bash
# System service control
sudo systemctl start oblirim-dashboard
sudo systemctl stop oblirim-dashboard
sudo systemctl restart oblirim-dashboard
sudo systemctl status oblirim-dashboard

# View logs
sudo journalctl -u oblirim-dashboard -f
```

## 🚨 Troubleshooting

### **Installation Issues**
```bash
# Permission errors
sudo chown -R $USER:$USER /path/to/oblirim

# Python issues  
sudo apt install python3-dev python3-pip

# Missing dependencies
./install.sh  # Re-run installer
```

### **Runtime Issues**
```bash
# Check service status
./status.sh

# View detailed logs
sudo journalctl -u oblirim-dashboard --no-pager

# Test manual startup
source .venv/bin/activate && python app.py
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

### **Performance Issues**
- **For Pi 3**: Ensure you're using the optimized lightweight theme
- **High CPU**: Check for background processes
- **Memory issues**: Restart the service: `./restart.sh`

## 🔄 Updates

### **Update Application**
```bash
git pull
source .venv/bin/activate
pip install -r requirements.txt
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

## 🤝 Contributing

### **Development Setup**
```bash
git clone <repository-url>
cd oblirim
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

### **Adding Features**
1. Create components in `components/`
2. Add routes in `app.py`
3. Update templates in `templates/`
4. Test on Pi 3/4/5 hardware

## 📝 License

[Add your license here]

## 🆘 Support

- **Issues**: Report bugs via GitHub Issues
- **Documentation**: Check this README
- **Logs**: Use `./status.sh` for diagnostics

---

**OBLIRIM PWN Master** - Built for hackers, optimized for Pi 🥧🐍