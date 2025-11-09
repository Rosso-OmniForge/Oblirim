# OBLIRIM Network Detection - Visual Reference

## System Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                         OBLIRIM v2.0                                  │
│              Enhanced Multi-Interface Network Detection               │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                      NETWORK ORCHESTRATOR                             │
│                   (Central Coordinator)                               │
│                                                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │
│  │   Monitor   │  │   Monitor   │  │   Monitor   │                  │
│  │    eth0     │  │   wlan0     │  │   wlan1     │                  │
│  │  (Priority  │  │  (Priority  │  │  (Priority  │                  │
│  │      1)     │  │      2)     │  │      3)     │                  │
│  └─────┬───────┘  └─────┬───────┘  └─────┬───────┘                  │
│        │                │                │                           │
│        └────────────────┴────────────────┘                           │
│                         │                                             │
│                    Check Every                                        │
│                     3 Seconds                                         │
│                         │                                             │
│         ┌───────────────┴───────────────┐                            │
│         ▼                               ▼                             │
│  ┌─────────────┐                 ┌─────────────┐                     │
│  │ State       │                 │ Determine   │                     │
│  │ Changed?    │──────YES───────>│ Active Tool │                     │
│  └─────────────┘                 └──────┬──────┘                     │
│         │                               │                             │
│         NO                              │                             │
│         │                               │                             │
│         └───────────────────────────────┘                             │
└───────────────────────────────────────┬─────────────────────────────┘
                                        │
                                        ▼
                          ┌─────────────────────────┐
                          │  TOOL ACTIVATION LOGIC  │
                          │  (Priority-Based)       │
                          └────────────┬────────────┘
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        │                              │                              │
        ▼                              ▼                              ▼
┌───────────────┐            ┌───────────────┐            ┌───────────────┐
│   PRIORITY 1  │            │   PRIORITY 2  │            │   PRIORITY 3  │
│   eth0 = UP   │            │  wlan0 = UP   │            │ NO CONNECTION │
│   + HAS IP    │            │   + HAS IP    │            │               │
└───────┬───────┘            └───────┬───────┘            └───────┬───────┘
        │                            │                            │
        ▼                            ▼                            ▼
┌───────────────┐            ┌───────────────┐            ┌───────────────┐
│ NETWORK TOOLS │            │   NET TEST    │            │ WIRELESS TOOLS│
│  (ETHERNET)   │            │               │            │               │
│               │            │ • DNS Test    │            │ • Scan WiFi   │
│ • Phase 1:    │            │ • HTTP Test   │            │ • Find OPEN   │
│   Detection   │            │ • Captive     │            │ • Auto-Connect│
│ • Phase 2:    │            │   Portal      │            │ • Wardrive DB │
│   Host Disc.  │            │ • Device Scan │            │               │
│ • Phase 3:    │            │               │            │ MODES:        │
│   Service     │            └───────┬───────┘            │ • Hunter      │
│   Enum.       │                    │                    │ • Passive     │
│ • Phase 4:    │            ┌───────┴────────┐           │               │
│   Vuln Scan   │            │                │           └───────────────┘
│               │            ▼                ▼
└───────────────┘    ┌──────────────┐  ┌────────────┐
                     │ Devices      │  │ No Devices │
                     │ Found?       │  │ or Captive │
                     │              │  │ Portal     │
                     └──────┬───────┘  └────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ NETWORK TOOLS │
                    │   (WIFI)      │
                    │               │
                    │ • Phase 1:    │
                    │   WiFi Info   │
                    │   (SSID,BSSID)│
                    │ • Phase 2-4:  │
                    │   Same as ETH │
                    │               │
                    └───────────────┘
```

---

## State Transition Diagram

```
                         ┌─────────────────┐
                         │   SYSTEM BOOT   │
                         └────────┬────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │  NETWORK ORCHESTRATOR   │
                    │       RUNNING           │
                    └────────┬────────────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
    ┌──────────┐      ┌──────────┐      ┌──────────┐
    │  eth0    │      │  wlan0   │      │  wlan1   │
    │  DOWN    │      │  DOWN    │      │  DOWN    │
    └──────────┘      └──────────┘      └──────────┘
          │                  │                  │
          └──────────────────┴──────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ NO CONNECTION   │
                    │ STATE           │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ WIRELESS TOOLS  │
                    │   ACTIVATED     │
                    └────────┬────────┘
                             │
                    (Scanning for WiFi...)
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
    ┌──────────┐      ┌──────────┐      ┌──────────┐
    │ Open Net │      │ No Open  │      │ Ethernet │
    │ Found &  │      │ Networks │      │ Plugged  │
    │ Connected│      │          │      │   In!    │
    └────┬─────┘      └────┬─────┘      └────┬─────┘
         │                 │                  │
         │                 │                  │
         ▼                 │                  ▼
    ┌──────────┐           │           ┌──────────┐
    │ wlan0 UP │           │           │ eth0 UP  │
    │ + HAS IP │           │           │ + HAS IP │
    └────┬─────┘           │           └────┬─────┘
         │                 │                │
         │    STOP    ◄────┘                │
         │   WIRELESS                       │
         │    TOOLS                    STOP ALL
         │                              WORKFLOWS
         ▼                                  │
    ┌──────────┐                           │
    │ NET TEST │                           │
    │  RUNS    │                           │
    └────┬─────┘                           │
         │                                  │
    ┌────┴─────┐                           │
    │          │                           │
    ▼          ▼                           ▼
┌──────┐  ┌──────┐                  ┌──────────┐
│Device│  │ No   │                  │ NETWORK  │
│Found │  │Device│                  │  TOOLS   │
└──┬───┘  └──────┘                  │ (ETH)    │
   │                                 │          │
   ▼                                 │ HIGHEST  │
┌──────────┐                         │ PRIORITY │
│ NETWORK  │◄────────────────────────┤ ALWAYS!  │
│  TOOLS   │    (If eth0 connects)   │          │
│ (WiFi)   │                         └──────────┘
└──────────┘
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         DATA SOURCES                             │
└─────────────────────────────────────────────────────────────────┘
         │                    │                    │
         │                    │                    │
         ▼                    ▼                    ▼
    ┌────────┐          ┌────────┐          ┌────────┐
    │ /sys/  │          │  ip    │          │ nmcli  │
    │ class/ │          │ addr   │          │  dev   │
    │ net/   │          │ show   │          │  wifi  │
    └───┬────┘          └───┬────┘          └───┬────┘
        │                   │                   │
        └───────────────────┴───────────────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │  NETWORK ORCHESTRATOR │
                │   (State Detection)   │
                └──────────┬────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  eth_workflow │  │  net_test     │  │wireless_tools │
│               │  │               │  │               │
│ • nmap        │  │ • ping DNS    │  │ • nmcli scan  │
│ • nikto       │  │ • HTTP test   │  │ • auto-connect│
│ • enum4linux  │  │ • nmap scan   │  │               │
│               │  │               │  │               │
└───────┬───────┘  └───────┬───────┘  └───────┬───────┘
        │                  │                  │
        │                  │                  │
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ logs/eth/     │  │ logs/wifi/    │  │ data/         │
│ README.md     │  │ nettest_*.json│  │ wardrive.json │
└───────────────┘  └───────────────┘  └───────────────┘
        │                  │                  │
        └──────────────────┴──────────────────┘
                           │
                           ▼
                ┌───────────────────────┐
                │    DASHBOARD          │
                │   (SocketIO Events)   │
                └───────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ network_status│  │ eth_progress  │  │wireless_scan  │
│               │  │               │  │ _complete     │
└───────────────┘  └───────────────┘  └───────────────┘
```

---

## Component Interaction Map

```
┌─────────────────────────────────────────────────────────────────┐
│                           app.py                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Flask + SocketIO                       │   │
│  └──────────────────────────────────────────────────────────┘   │
│         │                                                         │
│         │ Initializes & Registers Callbacks                     │
│         │                                                         │
│         ▼                                                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │            network_orchestrator.start()                   │   │
│  │  • register_callback('eth_connected', handler)           │   │
│  │  • register_callback('wifi_connected', handler)          │   │
│  │  • register_callback('no_connection', handler)           │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ Callbacks
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ eth_connected │   │wifi_connected │   │ no_connection │
│   handler     │   │   handler     │   │   handler     │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ eth_workflow  │   │  net_test     │   │wireless_tools │
│ .run_workflow │   │ .run_full_test│   │    .start()   │
│   (network_   │   │               │   │               │
│     info)     │   │     ↓         │   │               │
│               │   │  ┌─────────┐  │   │               │
│               │   │  │Devices? │  │   │               │
│               │   │  └────┬────┘  │   │               │
│               │   │       │       │   │               │
│               │   │    YES│       │   │               │
│               │   │       ▼       │   │               │
│               │   │wifi_workflow  │   │               │
│               │   │.run_workflow  │   │               │
│               │   │ (network_info)│   │               │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│   Emit        │   │   Emit        │   │   Emit        │
│ eth_progress  │   │nettest_result │   │wireless_scan  │
│               │   │               │   │  _complete    │
│   to          │   │   to          │   │   to          │
│ SocketIO      │   │ SocketIO      │   │ SocketIO      │
└───────────────┘   └───────────────┘   └───────────────┘
        │                   │                   │
        └───────────────────┴───────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   DASHBOARD   │
                    │  (JavaScript) │
                    └───────────────┘
```

---

## File Dependency Graph

```
app.py
  ├─ components/network_orchestrator.py
  │    ├─ components/eth_workflow.py
  │    │    ├─ components/tab_logger.py
  │    │    └─ components/network_metrics.py
  │    │
  │    ├─ components/wifi_workflow.py (TODO)
  │    │    ├─ components/tab_logger.py
  │    │    └─ components/network_metrics.py
  │    │
  │    ├─ components/net_test.py
  │    │    └─ (uses requests library)
  │    │
  │    └─ components/wireless_tools.py
  │         └─ (uses nmcli/iwlist)
  │
  ├─ components/system_specs_component.py
  │
  ├─ templates/index.html
  │
  └─ static/
       └─ (CSS, JS files)
```

---

## Timeline View (Typical Execution)

```
Time    Event                       Active Tool           State
──────  ──────────────────────      ────────────────      ──────────────
00:00   System Boot                 None                  Initializing
00:01   Orchestrator Start          None → Wireless       NO_CONNECTION
00:05   WiFi Scan Complete          Wireless Tools        Scanning
00:10   Open Network Found          Wireless Tools        Connecting
00:15   wlan0 Gets IP               Wireless → Net Test   WIFI_CONNECTED
00:20   Net Test Complete           Net Test → WiFi Flow  Testing
00:25   WiFi Workflow Phase 1       WiFi Workflow         Scanning
00:30   WiFi Workflow Phase 2       WiFi Workflow         Scanning
00:35   !! Ethernet Plugged In !!   WiFi → ETH Flow       BOTH_CONNECTED
00:36   Ethernet Workflow Phase 1   ETH Workflow          ETH_CONNECTED
00:40   Ethernet Workflow Phase 2   ETH Workflow          Scanning
00:45   Ethernet Workflow Phase 3   ETH Workflow          Scanning
00:50   Ethernet Workflow Phase 4   ETH Workflow          Scanning
00:55   Workflow Complete           ETH Workflow (Idle)   Monitoring
```

---

## Error Handling Flow

```
┌───────────────────────────────────────────────────────────┐
│                   Error Scenarios                          │
└───────────────────────────────────────────────────────────┘

1. Network Tools Fails Mid-Scan
   ┌─────────────┐
   │ Phase 2     │ ──Error──> Log Error
   │ Fails       │            Continue to Phase 3
   └─────────────┘            (Graceful Degradation)

2. Net Test Timeout
   ┌─────────────┐
   │ DNS Test    │ ──Timeout──> Try HTTP Test
   │ Timeout     │              If all fail → Log & Exit
   └─────────────┘              Don't trigger workflow

3. WiFi Connection Fails
   ┌─────────────┐
   │ nmcli       │ ──Fails──> Try next network
   │ connect     │            If all fail → Continue scanning
   │ fails       │            (Mark network as attempted)
   └─────────────┘

4. Ethernet Disconnects During Scan
   ┌─────────────┐
   │ eth0 DOWN   │ ──Detected──> Stop ETH Workflow
   │             │               Check wlan0
   └─────────────┘               If up → Start WiFi flow
                                 If down → Start Wireless Tools

5. Tool Crash
   ┌─────────────┐
   │ Component   │ ──Exception──> Log Error
   │ Raises      │                Set state to IDLE
   │ Exception   │                Continue monitoring
   └─────────────┘                (System keeps running)
```

---

## Configuration Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│              Configuration Precedence                        │
└─────────────────────────────────────────────────────────────┘

1. Default Values (In Code)
   ├─ network_orchestrator.py → check_interval = 3
   ├─ wireless_tools.py → scan_interval = 30
   └─ net_test.py → timeout = 10

2. Config File (If Exists)
   └─ config/network_detection.json
      ├─ Overrides defaults
      └─ Loaded at startup

3. Runtime Modification (Future)
   └─ Dashboard settings panel
      └─ Temporarily override config
```

---

**Created**: November 9, 2025  
**Purpose**: Visual reference for OBLIRIM Network Detection v2.0  
**Use**: Print this out or keep it handy during integration!

