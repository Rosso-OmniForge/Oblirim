# OBLIRIM Network Detection System - Design Document

**Version**: 2.0  
**Date**: November 9, 2025  
**Status**: In Development

---

## 🎯 Overview

This document outlines the enhanced network detection and workflow system for OBLIRIM. The new design introduces **intelligent multi-interface detection** that automatically launches appropriate tools based on connection type and network characteristics.

---

## 🏗️ Architecture Components

### 1. **Network Orchestrator** (`network_orchestrator.py`)
**Purpose**: Central coordinator that monitors all network interfaces and triggers appropriate workflows

**Responsibilities**:
- Monitor `eth0`, `wlan0`, `wlan1` interface states
- Detect connection changes (UP/DOWN, IP assignment)
- Coordinate workflow execution based on connection type
- Prevent conflicting tools from running simultaneously
- Emit real-time status updates via SocketIO

**Key Methods**:
```python
- get_active_interfaces() -> dict
- get_interface_info(interface_name) -> dict
- start_monitoring()
- stop_monitoring()
- handle_state_change(interface, old_state, new_state)
```

---

### 2. **Net Test** (`net_test.py`)
**Purpose**: Network connectivity and captive portal detection tool

**When It Runs**:
- Automatically when `wlan0` gets an IP address
- Manually triggered for testing

**What It Does**:
1. **Internet Connectivity Test**
   - Ping well-known DNS servers (8.8.8.8, 1.1.1.1)
   - HTTP GET to detectportal.firefox.com
   - Check for HTTP 302 redirects (captive portal signature)

2. **Captive Portal Detection**
   - Parse redirect URLs
   - Detect common portal types (WISPr, hotel, coffee shop)
   - Log portal authentication pages

3. **Network Device Discovery**
   - Quick ARP scan to find other devices
   - If devices found → trigger **Network Tools** (WiFi Workflow)
   - If no devices → log as isolated network

**Output**:
```json
{
  "internet_access": true/false,
  "captive_portal": true/false,
  "portal_type": "WISPr|Generic|None",
  "portal_url": "http://...",
  "devices_found": 5,
  "trigger_network_tools": true/false
}
```

---

### 3. **Wireless Tools** (`wireless_tools.py`)
**Purpose**: Wardriving-style WiFi reconnaissance and packet capture

**When It Runs**:
- When **NO Ethernet** AND **NO WiFi connection**
- When `wlan1` is available for monitoring (while `wlan0` can connect)

**Operating Modes**:

#### **Mode A: Open Network Hunter**
**Goal**: Find and auto-connect to open WiFi networks

**Process**:
1. Scan for WiFi networks using `nmcli` or `iwlist`
2. Filter for **OPEN** networks (no encryption)
3. Sort by signal strength (strongest first)
4. Auto-connect to strongest open network
5. Run **Net Test** on successful connection
6. If Net Test passes → run **WiFi Workflow**
7. Disconnect and try next network if no devices found

**Logging**:
```markdown
## Open Network Scan - 2025-11-09 14:22:10
- **SSID**: "FreePublicWiFi"
- **BSSID**: 00:11:22:33:44:55
- **Signal**: -45 dBm (Excellent)
- **Encryption**: OPEN
- **Action**: Auto-connected
- **Net Test**: PASS (15 devices found)
- **Workflow**: Network Tools triggered
```

#### **Mode B: Passive Wardriving**
**Goal**: Log all WiFi networks without connecting

**Process**:
1. Put `wlan1` (if available) or `wlan0` into monitor mode
2. Capture beacon frames with `tcpdump` or `airodump-ng`
3. Log all SSIDs, BSSIDs, encryption types, channels
4. Generate wardrive database (JSON/SQLite)

**Logging**:
```json
{
  "timestamp": "2025-11-09T14:22:10Z",
  "ssid": "HomeNetwork_5G",
  "bssid": "AA:BB:CC:DD:EE:FF",
  "channel": 36,
  "signal": -65,
  "encryption": "WPA2-PSK",
  "vendor": "Cisco Systems"
}
```

#### **Mode C: Bettercap/Pwnagotchi Style Capture**
**Goal**: Passive packet capture for WPA handshakes

**Process**:
1. Use `wlan1` in monitor mode
2. Run Bettercap with WiFi deauth module (passive listening)
3. Capture EAPOL handshakes to `.pcap` files
4. Log captured handshakes for offline cracking
5. Optional: Auto-upload to cloud/server for distributed cracking

**When Active**:
- No open networks found after scan
- `wlan1` available for monitoring
- User enables "Aggressive Mode"

---

### 4. **WiFi Workflow** (`wifi_workflow.py`)
**Purpose**: 4-phase penetration testing workflow adapted for WiFi networks

**When It Runs**:
- When connected to WiFi (`wlan0`) AND **Net Test passes** (devices found)

**Workflow Structure** (mirrors `eth_workflow.py`):

**Phase 1: WiFi Network Detection**
- Get SSID, BSSID, encryption type
- Identify router IP (gateway)
- Classify network (home, enterprise, public)

**Phase 2: Host Discovery**
- `nmap -sn` scan on WiFi subnet
- ARP scan for active hosts
- MAC vendor lookup

**Phase 3: Service Enumeration**
- TCP port scan on discovered hosts
- Service version detection
- HTTP/HTTPS banner grabbing

**Phase 4: Vulnerability Assessment**
- Nikto on web servers
- SMB enumeration
- SNMP checks

**Key Differences from Ethernet Workflow**:
- Add SSID/BSSID logging
- Detect WiFi-specific vulnerabilities (WPS, WEP)
- Check for rogue AP indicators

---

## 🔀 State Machine & Decision Tree

### **Network State Machine**

```
┌─────────────────────────────────────────────────────────────┐
│                     SYSTEM BOOT                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────┐
              │  NO CONNECTION   │◄──────────────┐
              └────────┬─────────┘               │
                       │                         │
        ┌──────────────┼──────────────┐         │
        │              │              │          │
        ▼              ▼              ▼          │
┌────────────┐  ┌────────────┐  ┌──────────┐   │
│ eth0 UP    │  │ wlan0 UP   │  │ wlan1 UP │   │
│ + IP       │  │ + IP       │  │          │   │
└─────┬──────┘  └─────┬──────┘  └────┬─────┘   │
      │               │              │          │
      ▼               ▼              ▼          │
┌────────────┐  ┌────────────┐  ┌──────────┐   │
│ Network    │  │ Net Test   │  │ Wireless │   │
│ Tools      │  │            │  │ Tools    │   │
│ (ETH)      │  └─────┬──────┘  │ (Monitor)│   │
└────────────┘        │         └──────────┘   │
                      │                         │
              ┌───────┴───────┐                │
              ▼               ▼                 │
      ┌──────────────┐  ┌──────────┐          │
      │ Devices?     │  │ Captive  │          │
      │ YES          │  │ Portal?  │          │
      └───┬──────────┘  └──────────┘          │
          │                                     │
          ▼                                     │
    ┌────────────┐                             │
    │ Network    │                             │
    │ Tools      │                             │
    │ (WiFi)     │                             │
    └────────────┘                             │
          │                                     │
          └─────────────────────────────────────┘
```

### **Decision Logic**

```python
def determine_active_tool():
    """
    Decision tree for which tool to activate
    """
    # Priority 1: Ethernet (most reliable for pentesting)
    if eth0_has_ip():
        stop_all_other_tools()
        start_network_tools(interface='eth0')
        return 'NETWORK_TOOLS_ETH'
    
    # Priority 2: WiFi with active connection
    elif wlan0_has_ip():
        stop_wireless_tools()  # Stop scanning if running
        result = run_net_test(interface='wlan0')
        
        if result['devices_found'] > 0:
            start_network_tools(interface='wlan0')
            return 'NETWORK_TOOLS_WIFI'
        elif result['captive_portal']:
            log_captive_portal(result['portal_url'])
            return 'CAPTIVE_PORTAL_DETECTED'
        else:
            return 'ISOLATED_NETWORK'
    
    # Priority 3: No active connection - start wireless reconnaissance
    else:
        start_wireless_tools()
        return 'WIRELESS_TOOLS'
```

---

## 📊 Tool Activation Matrix

| Scenario | eth0 | wlan0 | Active Tool | Behavior |
|----------|------|-------|-------------|----------|
| Ethernet connected | UP + IP | DOWN | **Network Tools (ETH)** | Full 4-phase scan on eth0 |
| WiFi connected (devices found) | DOWN | UP + IP | **Net Test** → **Network Tools (WiFi)** | Test network → 4-phase scan on wlan0 |
| WiFi connected (no devices) | DOWN | UP + IP | **Net Test** | Log as isolated, monitor for changes |
| WiFi captive portal | DOWN | UP + IP | **Net Test** | Detect portal, log URL, attempt bypass |
| No connection | DOWN | DOWN | **Wireless Tools** | Scan for open WiFi, wardriving mode |
| Ethernet connects mid-WiFi scan | UP + IP | UP + IP | **Network Tools (ETH)** | STOP WiFi tools, START eth0 workflow |
| WiFi connects mid-wireless scan | DOWN | UP + IP | **Net Test** | STOP wireless tools, test network |

---

## 🔄 Transition Handling

### **Scenario: Ethernet connects while WiFi scan is running**

1. Network Orchestrator detects `eth0` state change
2. Immediately stop **WiFi Workflow** or **Wireless Tools**
3. Emit SocketIO event: `workflow_interrupted`
4. Start **Network Tools (ETH)**
5. Log transition: `"WiFi workflow stopped - Ethernet priority"`

### **Scenario: WiFi disconnects during scan**

1. Network Orchestrator detects `wlan0` down
2. Stop **WiFi Workflow**
3. Start **Wireless Tools** (begin scanning again)
4. Log: `"WiFi lost - Reverting to wireless reconnaissance"`

### **Scenario: Open WiFi found and connected**

1. **Wireless Tools** finds open network "FreeWiFi"
2. Auto-connect using `nmcli device wifi connect "FreeWiFi"`
3. Wait for IP assignment (max 10 seconds)
4. Run **Net Test**
5. If devices found → Start **WiFi Workflow**
6. If no devices → Disconnect and try next network

---

## 🛠️ Implementation Details

### **Required Tools**

| Tool | Purpose | Install |
|------|---------|---------|
| `nmcli` | WiFi scanning & connection | `apt install network-manager` |
| `iw` / `iwconfig` | Interface control | `apt install wireless-tools iw` |
| `airodump-ng` | Wardriving captures | `apt install aircrack-ng` |
| `bettercap` | Advanced WiFi attacks | `apt install bettercap` |
| `tcpdump` | Packet capture | `apt install tcpdump` |
| `curl` | Captive portal detection | `apt install curl` |

### **Configuration Files**

**`config/network_detection.json`**
```json
{
  "interfaces": {
    "eth0": {"priority": 1, "auto_scan": true},
    "wlan0": {"priority": 2, "auto_scan": true, "auto_connect_open": true},
    "wlan1": {"priority": 3, "monitor_mode": true}
  },
  "net_test": {
    "timeout": 10,
    "test_urls": [
      "http://detectportal.firefox.com/success.txt",
      "http://captive.apple.com/hotspot-detect.html"
    ],
    "dns_servers": ["8.8.8.8", "1.1.1.1"]
  },
  "wireless_tools": {
    "open_network_whitelist": [],
    "open_network_blacklist": ["xfinitywifi", "attwifi"],
    "max_connection_attempts": 3,
    "enable_handshake_capture": false,
    "wardrive_log_path": "/home/nero/dev/oblirim/data/wardrive.json"
  }
}
```

---

## 📁 File Structure

```
/home/nero/dev/oblirim/
├── components/
│   ├── network_orchestrator.py       [NEW] Central coordinator
│   ├── net_test.py                    [NEW] Captive portal detection
│   ├── wireless_tools.py              [NEW] Wardriving & WiFi recon
│   ├── wifi_workflow.py               [NEW] 4-phase WiFi workflow
│   ├── eth_detector.py                [DEPRECATE] Merge into orchestrator
│   ├── eth_workflow.py                [KEEP] Ethernet-specific workflow
│   └── network_metrics.py             [UPDATE] Add WiFi metrics
├── config/
│   └── network_detection.json         [NEW] Configuration
├── data/
│   ├── wardrive.json                  [NEW] Wardriving database
│   ├── captive_portals.json           [NEW] Portal detection logs
│   └── network_metrics.json           [EXISTING]
└── logs/
    ├── eth/                           [EXISTING]
    ├── wifi/                          [NEW]
    └── wireless/                      [NEW]
```

---

## 🚀 Implementation Plan

### **Phase 1: Core Detection (Week 1)**
- [ ] Build `network_orchestrator.py` with multi-interface monitoring
- [ ] Build `net_test.py` for captive portal detection
- [ ] Test state transitions (eth0 → wlan0 → no connection)

### **Phase 2: WiFi Workflow (Week 2)**
- [ ] Build `wifi_workflow.py` (clone of eth_workflow with WiFi adaptations)
- [ ] Integrate Net Test results into workflow decisions
- [ ] Add WiFi-specific logging to `tab_logger.py`

### **Phase 3: Wireless Tools (Week 3)**
- [ ] Build `wireless_tools.py` with open network scanning
- [ ] Implement auto-connect logic
- [ ] Add wardriving database and logging

### **Phase 4: Advanced Features (Week 4)**
- [ ] Bettercap/Pwnagotchi integration
- [ ] Handshake capture mode
- [ ] Captive portal bypass attempts (generic credentials)

### **Phase 5: UI & Testing (Week 5)**
- [ ] Update dashboard with WiFi tab
- [ ] Add real-time wireless scan results display
- [ ] End-to-end testing on Pi

---

## 🔐 Security & Ethics

**Important**:
- All tools are for **authorized testing only**
- Auto-connect to open networks only when explicitly enabled
- No aggressive deauth attacks without user confirmation
- Log all actions for audit trail
- Respect blacklists for known public WiFi (Xfinity, AT&T, etc.)

---

## 📝 Example Log Outputs

### **Ethernet Connected**
```markdown
## Session: 2025-11-09_14:22_192.168.1.0/24
- **Trigger**: eth0 connected
- **Interface**: eth0
- **IP**: 192.168.1.100
- **Gateway**: 192.168.1.1
- **Tool**: Network Tools (Ethernet)
- **Phase 1**: Network Detection ✓
- **Phase 2**: 12 hosts discovered
- **Phase 3**: 45 ports found
- **Phase 4**: 3 vulnerabilities detected
```

### **WiFi with Net Test**
```markdown
## Session: 2025-11-09_15:30_CoffeeShopWiFi
- **Trigger**: wlan0 connected
- **SSID**: "CoffeeShop_Guest"
- **BSSID**: AA:BB:CC:DD:EE:FF
- **IP**: 10.0.50.123
- **Net Test**: PASS
  - Internet: YES
  - Captive Portal: YES (WISPr)
  - Portal URL: http://portal.coffeeshop.com/login
  - Devices: 8 found
- **Tool**: Network Tools (WiFi)
- **Workflow**: Started
```

### **Wireless Tools Scanning**
```markdown
## Wireless Scan: 2025-11-09_16:00
- **Mode**: Open Network Hunter
- **Networks Found**: 15
  - "FreeWiFi" (OPEN, -45dBm) → Connected
  - "GuestNetwork" (OPEN, -62dBm)
  - "HomeRouter_2G" (WPA2, -55dBm)
- **Auto-Connect**: "FreeWiFi"
- **Net Test**: PASS (2 devices)
- **Action**: Network Tools triggered
```

---

## 🎯 Success Criteria

1. **Zero-touch operation**: Device boots → auto-detects → launches correct tools
2. **Seamless transitions**: Ethernet plugged in → immediately stops WiFi tools
3. **Smart WiFi handling**: Auto-connects to open networks → tests → scans if viable
4. **Complete logging**: Every action logged with timestamps and context
5. **Dashboard visibility**: Real-time updates show which tool is active and why

---

**Next Steps**: Begin implementation of `network_orchestrator.py` ✅
