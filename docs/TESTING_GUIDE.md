# OBLIRIM Testing Guide

## Quick Testing (No Installation Required)

You can test OBLIRIM without doing a full system installation:

### 🚀 Super Quick Start
```bash
./quick-test.sh
```
This gives you a menu of testing options.

### 📋 Testing Options

#### 1. **Full Test Suite**
Tests everything without modifying your system:
```bash
./test-dev.sh --full
```

#### 2. **Interactive Development Server**
Start a test server on port 5001:
```bash
./test-dev.sh --server
```
Then visit: http://127.0.0.1:5001

#### 3. **TUI Test (Automatic)**
Test TUI with auto-starting backend:
```bash
./test-tui.sh
```
This automatically starts a test backend on port 5001 if needed, then launches the TUI.

#### 4. **TUI Only** (requires backend running)
```bash
# Option A: Start backend first
./launch.sh  # In one terminal

# Option B: Use TUI launcher with options
./launch-tui.sh  # In another terminal - offers to start backend

# Option C: Manual setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py  # In one terminal
python3 tui_app.py  # In another terminal
```

#### 5. **Web Server Only** (development)
```bash
./launch.sh
```
Then visit: http://localhost:5000

### 🔍 What Gets Tested

- ✅ **Python Environment** - Virtual env creation, dependencies
- ✅ **Flask Server** - Web interface, API endpoints  
- ✅ **TUI Application** - Terminal interface syntax/instantiation
- ✅ **Network Configuration** - Interface detection, binding logic
- ✅ **Security Rules** - Firewall simulation (no actual changes)
- ✅ **Project Structure** - Files, directories, imports

### 🛡️ Security Testing

The test suite simulates the security configuration without making any system changes:

- **Firewall Rules** - Shows what iptables rules would be applied
- **Network Binding** - Tests localhost/Bluetooth PAN binding logic  
- **Interface Detection** - Tests network interface discovery

### 💻 Development Workflow

```bash
# 1. Quick validation
./quick-test.sh

# 2. Test TUI specifically (auto-starts backend)
./test-tui.sh

# 3. Development server (with hot reload)
./launch.sh

# 4. TUI testing (manual)
./launch-tui.sh

# 5. Full test before deployment
./test-dev.sh --full

# 6. Production installation
./install.sh
```

### 🐛 Troubleshooting

**Virtual Environment Issues:**
```bash
# Remove and recreate
rm -rf .venv .test_venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Port Conflicts:**
```bash
# Check what's using port 5000/5001
sudo netstat -tlpn | grep :5000
sudo netstat -tlpn | grep :5001

# Kill processes if needed
pkill -f "python.*app.py"
```

**TUI Issues:**
```bash
# Check terminal compatibility
echo $TERM
python3 -c "import textual; print('Textual OK')"
```

**Permission Issues:**
```bash
# Make scripts executable
chmod +x *.sh
```

### 📁 Test Files

- `test-dev.sh` - Comprehensive test suite (syntax checks, no TUI launch)
- `test-tui.sh` - **TUI-specific test with auto-backend** ⭐ NEW
- `quick-test.sh` - Quick test launcher menu
- `launch-tui.sh` - TUI launcher with backend options
- `launch.sh` - Web server launcher  
- `test-installation.sh` - Installation verification
- `test-service.sh` - Systemd service testing

### 🔧 Advanced Testing

**Custom Test Server:**
```bash
# Run with specific host/port
FLASK_ENV=development python3 -c "
from app import app, socketio
socketio.run(app, host='127.0.0.1', port=5555, debug=True)
"
```

**Component Testing:**
```bash
# Test specific components
python3 -c "from components.eth_detector import eth_detector; print('OK')"
python3 -c "from components.network_metrics import network_metrics; print('OK')"
```

**Mock Bluetooth Interface:**
```bash
# Simulate Bluetooth PAN
sudo ip link add bnep0 type dummy
sudo ip addr add 10.0.0.1/24 dev bnep0
sudo ip link set bnep0 up

# Test, then cleanup
sudo ip link del bnep0
```

---

**Next Steps:**
- ✅ Test everything with `./test-dev.sh --full`
- ✅ Develop with `./launch.sh` and `./launch-tui.sh`  
- ✅ Deploy with `./install.sh` when ready