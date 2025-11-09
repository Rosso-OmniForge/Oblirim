# OBLIRIM Network Detection - Quick Reference

## 🚀 Quick Start

### Current Status
- ✅ Network Orchestrator - Complete
- ✅ Net Test (Captive Portal Detection) - Complete  
- ✅ Wireless Tools (Wardriving) - Complete
- ⏳ WiFi Workflow - TODO
- ⏳ app.py Integration - TODO

---

## 📦 Components Overview

| Component | File | Purpose | Status |
|-----------|------|---------|--------|
| **Network Orchestrator** | `components/network_orchestrator.py` | Central coordinator for all interfaces | ✅ |
| **Net Test** | `components/net_test.py` | Captive portal & device detection | ✅ |
| **Wireless Tools** | `components/wireless_tools.py` | WiFi scanning & auto-connect | ✅ |
| **WiFi Workflow** | `components/wifi_workflow.py` | 4-phase WiFi pentesting | ⏳ |
| **Ethernet Workflow** | `components/eth_workflow.py` | 4-phase Ethernet pentesting | ✅ |

---

## 🔄 Decision Tree (How It Works)

```
┌─────────────────────────────────────────┐
│  Network Orchestrator monitors all     │
│  interfaces every 3 seconds            │
└───────────────┬─────────────────────────┘
                │
                ▼
        ┌───────────────┐
        │ eth0 has IP?  │
        └───┬───────┬───┘
            │       │
        YES │       │ NO
            │       │
            ▼       ▼
    ┌───────────┐   ┌───────────────┐
    │ Network   │   │ wlan0 has IP? │
    │ Tools     │   └───┬───────┬───┘
    │ (ETH)     │       │       │
    └───────────┘   YES │       │ NO
                        │       │
                        ▼       ▼
                ┌───────────┐   ┌───────────┐
                │ Net Test  │   │ Wireless  │
                │           │   │ Tools     │
                └─────┬─────┘   └───────────┘
                      │
              ┌───────┴────────┐
              ▼                ▼
      ┌──────────────┐   ┌──────────┐
      │ Devices      │   │ No       │
      │ Found?       │   │ Devices  │
      │ YES          │   │          │
      └───┬──────────┘   └──────────┘
          │
          ▼
    ┌───────────┐
    │ Network   │
    │ Tools     │
    │ (WiFi)    │
    └───────────┘
```

---

## 🎯 Priority Rules

**Priority 1**: Ethernet (eth0)  
- If eth0 has IP → Stop everything, run Network Tools (Ethernet)

**Priority 2**: WiFi (wlan0)  
- If wlan0 has IP → Run Net Test
  - If devices found → Run Network Tools (WiFi)
  - If no devices → Log as isolated network

**Priority 3**: No Connection  
- Run Wireless Tools (scan for open WiFi, auto-connect)

---

## 📝 Example Callbacks

### Register Callbacks in app.py

```python
from components.network_orchestrator import network_orchestrator
from components.eth_workflow import eth_workflow
from components.wifi_workflow import wifi_workflow  # TODO: Create this
from components.wireless_tools import wireless_tools
from components.net_test import net_test

def handle_eth_connected(network_info):
    """Ethernet connected - start eth workflow"""
    print(f"Ethernet connected: {network_info['ip']}")
    
    # Start ethernet workflow in thread
    def run():
        eth_workflow.run_workflow(network_info)
    
    threading.Thread(target=run, daemon=True).start()

def handle_wifi_connected(network_info):
    """WiFi connected - run Net Test first"""
    print(f"WiFi connected: {network_info['ip']} - SSID: {network_info['ssid']}")
    
    # Run Net Test
    results = net_test.run_full_test(interface='wlan0', network_info=network_info)
    
    # If devices found, run WiFi workflow
    if results['trigger_network_tools']:
        def run():
            wifi_workflow.run_workflow(network_info)  # TODO: Create wifi_workflow
        threading.Thread(target=run, daemon=True).start()
    else:
        print("No devices found - not running workflow")

def handle_no_connection():
    """No connection - start wireless tools"""
    print("No network connection - starting wireless tools")
    wireless_tools.start(mode='hunter')

def handle_tool_change(old_tool, new_tool):
    """Active tool changed"""
    print(f"Tool changed: {old_tool.value} → {new_tool.value}")
    
    # Stop old workflows
    if old_tool.value == 'wireless_tools':
        wireless_tools.stop()

# Register callbacks
network_orchestrator.register_callback('eth_connected', handle_eth_connected)
network_orchestrator.register_callback('wifi_connected', handle_wifi_connected)
network_orchestrator.register_callback('no_connection', handle_no_connection)
network_orchestrator.register_callback('tool_change', handle_tool_change)

# Start orchestrator
network_orchestrator.socketio = socketio
network_orchestrator.start()
```

---

## 🔧 API Endpoints (To Add)

```python
@app.route('/api/network/status')
def network_status():
    """Get overall network status"""
    return jsonify(network_orchestrator.get_status())

@app.route('/api/wireless/stats')
def wireless_stats():
    """Get wardriving statistics"""
    return jsonify(wireless_tools.get_wardrive_stats())

@app.route('/api/nettest/latest')
def nettest_latest():
    """Get latest Net Test results"""
    results = net_test.get_recent_results(count=1)
    return jsonify(results[0] if results else {})

@app.route('/api/wireless/scan', methods=['POST'])
def trigger_wireless_scan():
    """Manually trigger WiFi scan"""
    networks = wireless_tools.scan_wifi_networks()
    return jsonify({'networks': networks, 'count': len(networks)})
```

---

## 📊 SocketIO Events

### Events Emitted BY Components

| Event | Source | Data | Description |
|-------|--------|------|-------------|
| `network_status` | NetworkOrchestrator | Interface states, active tool | Every 3s status update |
| `active_tool_change` | NetworkOrchestrator | Old/new tool | When active tool changes |
| `orchestrator_log` | NetworkOrchestrator | Log message | Log entries |
| `wireless_scan_complete` | WirelessTools | Network count | WiFi scan finished |
| `open_networks_found` | WirelessTools | Network list | Open networks detected |
| `wireless_tools_log` | WirelessTools | Log message | Wireless tool logs |

### Events Listened TO (Dashboard → Backend)

| Event | Handler | Action |
|-------|---------|--------|
| `start_wireless_scan` | Manual trigger | Force WiFi scan |
| `connect_to_network` | Manual connect | Connect to specific SSID |
| `stop_wireless_tools` | Stop scanning | Stop wireless tools |

---

## 🗂️ Data Files

### Generated Automatically

```
data/
├── wardrive.json              # WiFi networks database
│   └── { networks: {...}, metadata: {...} }
│
├── captive_portals.json       # Detected portals
│   └── [ {timestamp, ssid, portal_url, ...}, ... ]
│
└── network_metrics.json       # Existing metrics
    └── { eth0: {...}, wlan0: {...} }

logs/
├── eth/                       # Ethernet logs
│   └── README.md
│
├── wifi/                      # WiFi workflow logs
│   └── nettest_*.json
│
└── wireless/                  # Wireless tools logs
    └── scan_*.log
```

---

## ⚙️ Configuration (TODO)

Create `config/network_detection.json`:

```json
{
  "wireless_tools": {
    "auto_connect": false,
    "scan_interval": 30,
    "blacklist": ["xfinitywifi", "attwifi", "optimumwifi"],
    "whitelist": [],
    "max_attempts_per_network": 1
  },
  "net_test": {
    "timeout": 10,
    "min_devices_for_workflow": 1,
    "test_urls": [
      "http://detectportal.firefox.com/success.txt",
      "http://captive.apple.com/hotspot-detect.html"
    ]
  },
  "orchestrator": {
    "check_interval": 3,
    "interfaces": ["eth0", "wlan0", "wlan1"]
  }
}
```

---

## 🧪 Testing Commands

### Test Individual Components

```bash
# Test Wireless Tools
cd /home/nero/dev/oblirim
python3 << EOF
from components.wireless_tools import wireless_tools
wireless_tools.auto_connect_enabled = False
networks = wireless_tools.scan_wifi_networks()
print(f"Found {len(networks)} networks")
for n in networks[:5]:
    print(f"  {n['ssid']} - {n['signal']}dBm - {'OPEN' if n['is_open'] else 'SECURED'}")
EOF

# Test Net Test
python3 << EOF
from components.net_test import net_test
results = net_test.run_full_test(interface='wlan0')
print(f"Internet: {results['internet_access']}")
print(f"Captive Portal: {results['captive_portal']}")
print(f"Devices: {results['devices_found']}")
print(f"Trigger Workflow: {results['trigger_network_tools']}")
EOF

# Test Network Orchestrator
python3 << EOF
from components.network_orchestrator import network_orchestrator
status = network_orchestrator.get_status()
print(f"Network State: {status['network_state']}")
print(f"Active Tool: {status['active_tool']}")
for iface, info in status['interfaces'].items():
    print(f"{iface}: {info['state']} - {info['ip']}")
EOF
```

---

## 🎬 Typical Execution Flow

### Scenario: Boot → Open WiFi → Ethernet Plugged

```
1. [00:00] System boots
2. [00:01] NetworkOrchestrator starts
3. [00:01] Detects: eth0 DOWN, wlan0 DOWN
4. [00:01] Activates: Wireless Tools (hunter mode)
5. [00:05] Wireless Tools finds open network "CoffeeShop_Guest"
6. [00:10] Connects successfully, IP assigned
7. [00:11] NetworkOrchestrator detects wlan0 UP
8. [00:11] Deactivates: Wireless Tools
9. [00:11] Activates: Net Test
10. [00:15] Net Test finds 8 devices, captive portal detected
11. [00:15] Deactivates: Net Test
12. [00:15] Activates: WiFi Workflow
13. [00:20] WiFi Workflow Phase 2 in progress
14. [00:25] USER PLUGS IN ETHERNET CABLE
15. [00:26] NetworkOrchestrator detects eth0 UP
16. [00:26] PRIORITY OVERRIDE: Deactivates WiFi Workflow
17. [00:26] Activates: Network Tools (Ethernet)
18. [00:30] Ethernet Workflow completes all 4 phases
19. [00:35] System idle, monitoring continues
```

---

## 🐛 Troubleshooting

### "nmcli command not found"
```bash
sudo apt install network-manager
```

### "No networks found"
```bash
# Check if wlan0 exists
ip link show wlan0

# Check if NetworkManager is running
sudo systemctl status NetworkManager

# Try manual scan
nmcli device wifi rescan
nmcli device wifi list
```

### "Can't connect to open network"
```bash
# Check permissions
sudo nmcli device wifi connect "NetworkName"

# Check logs
journalctl -u NetworkManager -f
```

### "Net Test shows no devices but I see them"
```bash
# nmap might need root for some scans
sudo nmap -sn 192.168.1.0/24

# Check ARP table
ip neigh show
```

---

## 📚 Key Files to Review

1. **`NETWORK_DETECTION_DESIGN.md`** - Complete architecture
2. **`IMPLEMENTATION_GUIDE.md`** - Detailed integration steps
3. **`components/network_orchestrator.py`** - Main coordinator
4. **`components/net_test.py`** - Captive portal detection
5. **`components/wireless_tools.py`** - WiFi scanning

---

## ✅ Integration Checklist

- [ ] Create `wifi_workflow.py` (clone eth_workflow.py)
- [ ] Update `app.py` with NetworkOrchestrator
- [ ] Add new API endpoints
- [ ] Update dashboard with WiFi/Wireless tabs
- [ ] Create config file
- [ ] Test state transitions
- [ ] Deploy to Raspberry Pi
- [ ] Field test in real environment

---

**Created**: November 9, 2025  
**For**: OBLIRIM v2.0 Enhanced Network Detection  
**Next**: WiFi Workflow implementation

