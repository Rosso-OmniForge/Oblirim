# Ethernet Penetration Testing Logs

## Session: 2025-11-06_22-58_1762462737

- **Connected:** 2025-11-06 22:58:57

- **Interface:** eth0 (up)

- **IP:** 10.0.5.70/24

- **Gateway:** 10.0.5.1

## Session: 2025-11-06_22-58-57_10-0-5-70-24
- **Network:** 10.0.5.70/24
- **Started:** 2025-11-06 22:58:57

## Session: 2025-11-06_22-59-46_10-0-5-70-24
- **Network:** 10.0.5.70/24
- **Started:** 2025-11-06 22:59:46

## Session: 2025-11-06_23-06_1762463211

- **Connected:** 2025-11-06 23:06:51

- **Interface:** eth0 (up)

- **IP:** 10.0.5.70/24

- **Gateway:** 10.0.5.1

## Session: 2025-11-06_23-06-51_10-0-5-70-24
- **Network:** 10.0.5.70/24
- **Started:** 2025-11-06 23:06:51

## Session: 2025-11-06_23-08-10_10-0-5-70-24
- **Network:** 10.0.5.70/24
- **Started:** 2025-11-06 23:08:10

## Session: 2025-11-06_23-21-44_10-0-5-70-24
- **Network:** 10.0.5.70/24
- **Started:** 2025-11-06 23:21:44

## Session: 2025-11-06_23-21-59_10-0-5-70-24
- **Network:** 10.0.5.70/24
- **Started:** 2025-11-06 23:21:59

## Session: 2025-11-06_23-22-30_10-0-5-70-24
- **Network:** 10.0.5.70/24
- **Started:** 2025-11-06 23:22:30

## Session: 2025-11-06_23-43-05_10-0-5-70-24
- **Network:** 10.0.5.70/24
- **Started:** 2025-11-06 23:43:05

- **Tool Check:** Missing tools: sslscan, enum4linux, smb-vuln-*, snmp-check, onesixtyone - Install with install.sh (2025-11-06 23:43:05)
- **Command Output:** ip link show eth0: 2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 88:a2:9e:2d:53:b4 brd ff:ff:ff:ff:ff:ff
... (2025-11-06 23:43:05)
- **Phase 1:** Interface detected → eth0 details logged (2025-11-06 23:43:05)
- **Network Range:** 10.0.5.0/24 (2025-11-06 23:43:05)
- **Network Classification:** RFC1918 Private Network (2025-11-06 23:43:05)
- **Command Output:** nmap -sn 10.0.5.0/24: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-06 23:43 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.015s latency).
Nmap scan report for 10.0.5.20
Host is up (0.036s latency).
Nmap ... (2025-11-06 23:43:08)
- **Phase 2:** nmap -sn completed → 9 hosts found (2025-11-06 23:43:08)
- **ERROR:** arp-scan --localnet: pcap_activate: eth0: You don't have permission to perform this capture on that device
(socket: Operation not permitted)
 (2025-11-06 23:43:08)
- **ERROR:** nmap -sS -T4 --top-ports 1000 192.168.1.1: You requested a scan type which requires root privileges.
QUITTING!
 (2025-11-06 23:43:08)
- **Command Output:** nmap -sV -sC 192.168.1.1: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-06 23:43 SAST
Note: Host seems down. If it is really up, but blocking our ping probes, try -Pn
Nmap done: 1 IP address (0 hosts up) scanned in 3.43 s... (2025-11-06 23:43:12)
- **Service Scan 192.168.1.1:** Version detection completed (2025-11-06 23:43:12)
- **ERROR:** nmap -sU --top-ports 100 192.168.1.1: You requested a scan type which requires root privileges.
QUITTING!
 (2025-11-06 23:43:12)
- **ERROR:** nmap -sS -T4 --top-ports 1000 192.168.1.100: You requested a scan type which requires root privileges.
QUITTING!
 (2025-11-06 23:43:12)
- **Command Output:** nmap -sV -sC 192.168.1.100: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-06 23:43 SAST
Note: Host seems down. If it is really up, but blocking our ping probes, try -Pn
Nmap done: 1 IP address (0 hosts up) scanned in 3.38 s... (2025-11-06 23:43:15)
- **Service Scan 192.168.1.100:** Version detection completed (2025-11-06 23:43:15)
- **ERROR:** nmap -sU --top-ports 100 192.168.1.100: You requested a scan type which requires root privileges.
QUITTING!
 (2025-11-06 23:43:15)
- **ERROR:** nmap -sS -T4 --top-ports 1000 192.168.1.254: You requested a scan type which requires root privileges.
QUITTING!
 (2025-11-06 23:43:15)
- **Command Output:** nmap -sV -sC 192.168.1.254: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-06 23:43 SAST
Note: Host seems down. If it is really up, but blocking our ping probes, try -Pn
Nmap done: 1 IP address (0 hosts up) scanned in 3.37 s... (2025-11-06 23:43:18)
- **Service Scan 192.168.1.254:** Version detection completed (2025-11-06 23:43:18)
- **ERROR:** nmap -sU --top-ports 100 192.168.1.254: You requested a scan type which requires root privileges.
QUITTING!
 (2025-11-06 23:43:18)
- **ERROR:** Command timed out: nikto -h 192.168.1.1 -Tuning 123 (2025-11-06 23:43:48)
- **ERROR:** enum4linux -a 192.168.1.1: /bin/sh: 1: enum4linux: not found
 (2025-11-06 23:43:48)
- **ERROR:** snmp-check 192.168.1.1: /bin/sh: 1: snmp-check: not found
 (2025-11-06 23:43:48)
- **ERROR:** Command timed out: nikto -h 192.168.1.100 -Tuning 123 (2025-11-06 23:44:18)
- **ERROR:** enum4linux -a 192.168.1.100: /bin/sh: 1: enum4linux: not found
 (2025-11-06 23:44:18)
- **ERROR:** snmp-check 192.168.1.100: /bin/sh: 1: snmp-check: not found
 (2025-11-06 23:44:18)
- **ERROR:** Command timed out: nikto -h 192.168.1.254 -Tuning 123 (2025-11-06 23:44:48)
- **ERROR:** enum4linux -a 192.168.1.254: /bin/sh: 1: enum4linux: not found
 (2025-11-06 23:44:48)
- **ERROR:** snmp-check 192.168.1.254: /bin/sh: 1: snmp-check: not found
 (2025-11-06 23:44:48)
- **Completed:** 2025-11-06 23:44:48
- **Summary:** Workflow completed: 3 hosts scanned

---

## Session: 2025-11-06_23-46-45_10-0-5-70-24
- **Network:** 10.0.5.70/24
- **Started:** 2025-11-06 23:46:45

- **Tool Check:** Missing tools: sslscan, enum4linux, smb-vuln-*, snmp-check, onesixtyone - Install with install.sh (2025-11-06 23:46:45)
- **Command Output:** ip link show eth0: 2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 88:a2:9e:2d:53:b4 brd ff:ff:ff:ff:ff:ff
... (2025-11-06 23:46:45)
- **Phase 1:** Interface detected → eth0 details logged (2025-11-06 23:46:45)
- **Network Range:** 10.0.5.0/24 (2025-11-06 23:46:45)
- **Network Classification:** RFC1918 Private Network (2025-11-06 23:46:45)
- **Command Output:** nmap -sn 10.0.5.0/24: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-06 23:46 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.0039s latency).
Nmap scan report for 10.0.5.20
Host is up (0.010s latency).
Nmap... (2025-11-06 23:46:55)
- **Phase 2:** nmap -sn completed → 10 hosts found (2025-11-06 23:46:55)
- **ERROR:** arp-scan --localnet: pcap_activate: eth0: You don't have permission to perform this capture on that device
(socket: Operation not permitted)
 (2025-11-06 23:46:55)
- **ERROR:** nmap -sS -T4 --top-ports 1000 192.168.1.1: You requested a scan type which requires root privileges.
QUITTING!
 (2025-11-06 23:46:55)
- **Command Output:** nmap -sV -sC 192.168.1.1: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-06 23:46 SAST
Note: Host seems down. If it is really up, but blocking our ping probes, try -Pn
Nmap done: 1 IP address (0 hosts up) scanned in 3.39 s... (2025-11-06 23:46:58)
- **Service Scan 192.168.1.1:** Version detection completed (2025-11-06 23:46:58)
- **ERROR:** nmap -sU --top-ports 100 192.168.1.1: You requested a scan type which requires root privileges.
QUITTING!
 (2025-11-06 23:46:58)
- **ERROR:** nmap -sS -T4 --top-ports 1000 192.168.1.100: You requested a scan type which requires root privileges.
QUITTING!
 (2025-11-06 23:46:58)
- **Command Output:** nmap -sV -sC 192.168.1.100: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-06 23:46 SAST
Note: Host seems down. If it is really up, but blocking our ping probes, try -Pn
Nmap done: 1 IP address (0 hosts up) scanned in 3.38 s... (2025-11-06 23:47:02)
- **Service Scan 192.168.1.100:** Version detection completed (2025-11-06 23:47:02)
- **ERROR:** nmap -sU --top-ports 100 192.168.1.100: You requested a scan type which requires root privileges.
QUITTING!
 (2025-11-06 23:47:02)
- **ERROR:** nmap -sS -T4 --top-ports 1000 192.168.1.254: You requested a scan type which requires root privileges.
QUITTING!
 (2025-11-06 23:47:02)
- **Command Output:** nmap -sV -sC 192.168.1.254: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-06 23:47 SAST
Note: Host seems down. If it is really up, but blocking our ping probes, try -Pn
Nmap done: 1 IP address (0 hosts up) scanned in 3.37 s... (2025-11-06 23:47:05)
- **Service Scan 192.168.1.254:** Version detection completed (2025-11-06 23:47:05)
- **ERROR:** nmap -sU --top-ports 100 192.168.1.254: You requested a scan type which requires root privileges.
QUITTING!
 (2025-11-06 23:47:05)
- **ERROR:** Command timed out: nikto -h 192.168.1.1 -Tuning 123 (2025-11-06 23:47:35)
- **ERROR:** enum4linux -a 192.168.1.1: /bin/sh: 1: enum4linux: not found
 (2025-11-06 23:47:35)
- **ERROR:** snmp-check 192.168.1.1: /bin/sh: 1: snmp-check: not found
 (2025-11-06 23:47:35)
- **ERROR:** Command timed out: nikto -h 192.168.1.100 -Tuning 123 (2025-11-06 23:48:05)
- **ERROR:** enum4linux -a 192.168.1.100: /bin/sh: 1: enum4linux: not found
 (2025-11-06 23:48:05)
- **ERROR:** snmp-check 192.168.1.100: /bin/sh: 1: snmp-check: not found
 (2025-11-06 23:48:05)
- **ERROR:** Command timed out: nikto -h 192.168.1.254 -Tuning 123 (2025-11-06 23:48:35)
- **ERROR:** enum4linux -a 192.168.1.254: /bin/sh: 1: enum4linux: not found
 (2025-11-06 23:48:35)
- **ERROR:** snmp-check 192.168.1.254: /bin/sh: 1: snmp-check: not found
 (2025-11-06 23:48:35)
- **Completed:** 2025-11-06 23:48:35
- **Summary:** Workflow completed: 3 hosts scanned

---

## Session: 2025-11-06_23-52-41_10-0-5-70-24
- **Network:** 10.0.5.70/24
- **Started:** 2025-11-06 23:52:41

- **Tool Check:** Missing tools: sslscan, enum4linux, smb-vuln-*, snmp-check, onesixtyone - Install with install.sh (2025-11-06 23:52:41)
- **Command Output:** ip link show eth0: 2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 88:a2:9e:2d:53:b4 brd ff:ff:ff:ff:ff:ff
... (2025-11-06 23:52:41)
- **Phase 1:** Interface detected → eth0 details logged (2025-11-06 23:52:41)
- **Network Range:** 10.0.5.0/24 (2025-11-06 23:52:41)
- **Network Classification:** RFC1918 Private Network (2025-11-06 23:52:41)
- **Command Output:** nmap -sn 10.0.5.0/24: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-06 23:52 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.020s latency).
Nmap scan report for 10.0.5.20
Host is up (0.011s latency).
Nmap ... (2025-11-06 23:52:44)
- **Phase 2:** nmap -sn completed → 10 hosts found (2025-11-06 23:52:44)
- **ARP Scan:** Skipped (requires root privileges) (2025-11-06 23:52:44)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.1: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-06 23:52 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.020s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT    STATE SERVI... (2025-11-06 23:52:45)
- **Port Scan 10.0.5.1:** 3 ports open (2025-11-06 23:52:45)
## Session: 2025-11-06_23-52-59_10-0-5-70-24
- **Network:** 10.0.5.70/24
- **Started:** 2025-11-06 23:52:59

- **Tool Check:** Missing tools: sslscan, enum4linux, smb-vuln-*, snmp-check, onesixtyone - Install with install.sh (2025-11-06 23:52:59)
- **Command Output:** ip link show eth0: 2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 88:a2:9e:2d:53:b4 brd ff:ff:ff:ff:ff:ff
... (2025-11-06 23:52:59)
- **Phase 1:** Interface detected → eth0 details logged (2025-11-06 23:52:59)
- **Network Range:** 10.0.5.0/24 (2025-11-06 23:52:59)
- **Network Classification:** RFC1918 Private Network (2025-11-06 23:52:59)
- **Command Output:** nmap -sn 10.0.5.0/24: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-06 23:52 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.0048s latency).
Nmap scan report for 10.0.5.20
Host is up (0.058s latency).
Nmap... (2025-11-06 23:53:12)
- **Phase 2:** nmap -sn completed → 10 hosts found (2025-11-06 23:53:12)
- **ARP Scan:** Skipped (requires root privileges) (2025-11-06 23:53:12)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.1: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-06 23:53 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.011s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT    STATE SERVI... (2025-11-06 23:53:12)
- **Port Scan 10.0.5.1:** 3 ports open (2025-11-06 23:53:12)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.1: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-06 23:52 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.022s latency).
Not shown: 997 closed tcp ports (conn-refused)
PORT    STATE SERV... (2025-11-06 23:53:18)
- **Service Scan 10.0.5.1:** Version detection completed (2025-11-06 23:53:18)
- **UDP Scan 10.0.5.1:** Skipped (requires root) (2025-11-06 23:53:18)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.10: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-06 23:53 SAST
Nmap scan report for 10.0.5.10
Host is up (0.082s latency).
All 100 scanned ports on 10.0.5.10 are in ignored states.
Not shown: 90 fil... (2025-11-06 23:53:21)
- **Port Scan 10.0.5.10:** 0 ports open (2025-11-06 23:53:21)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.1: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-06 23:53 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.0051s latency).
Not shown: 997 closed tcp ports (conn-refused)
PORT    STATE SER... (2025-11-06 23:53:41)
- **Service Scan 10.0.5.1:** Version detection completed (2025-11-06 23:53:41)
- **UDP Scan 10.0.5.1:** Skipped (requires root) (2025-11-06 23:53:41)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.10: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-06 23:53 SAST
Nmap scan report for 10.0.5.10
Host is up.
All 100 scanned ports on 10.0.5.10 are in ignored states.
Not shown: 100 filtered tcp ports ... (2025-11-06 23:53:52)
- **Port Scan 10.0.5.10:** 0 ports open (2025-11-06 23:53:52)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.10: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-06 23:53 SAST
Nmap scan report for 10.0.5.10
Host is up (0.047s latency).
All 1000 scanned ports on 10.0.5.10 are in ignored states.
Not shown: 990 f... (2025-11-06 23:53:52)
- **Service Scan 10.0.5.10:** Version detection completed (2025-11-06 23:53:52)
- **UDP Scan 10.0.5.10:** Skipped (requires root) (2025-11-06 23:53:52)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.20: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-06 23:53 SAST
Nmap scan report for 10.0.5.20
Host is up (0.012s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT     STATE SERVICE
22/tcp... (2025-11-06 23:53:52)
- **Port Scan 10.0.5.20:** 3 ports open (2025-11-06 23:53:52)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.10: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-06 23:53 SAST
Nmap scan report for 10.0.5.10
Host is up (2.4s latency).
All 1000 scanned ports on 10.0.5.10 are in ignored states.
Not shown: 858 fil... (2025-11-06 23:55:11)
- **Service Scan 10.0.5.10:** Version detection completed (2025-11-06 23:55:11)
- **UDP Scan 10.0.5.10:** Skipped (requires root) (2025-11-06 23:55:11)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.20: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-06 23:55 SAST
Nmap scan report for 10.0.5.20
Host is up (0.012s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT     STATE SERVICE
22/tcp... (2025-11-06 23:55:11)
- **Port Scan 10.0.5.20:** 3 ports open (2025-11-06 23:55:11)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.20: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-06 23:53 SAST
Nmap scan report for 10.0.5.20
Host is up (0.0083s latency).
Not shown: 994 closed tcp ports (conn-refused)
PORT     STATE SERVICE    V... (2025-11-06 23:55:13)
- **Service Scan 10.0.5.20:** Version detection completed (2025-11-06 23:55:13)
- **UDP Scan 10.0.5.20:** Skipped (requires root) (2025-11-06 23:55:13)
- **Command Output:** nikto -h 10.0.5.1 -Tuning 123 -maxtime 60: - Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          10.0.5.1
+ Target Hostname:    _gateway
+ Target Port:        80
+ Start Time:         ... (2025-11-06 23:55:15)
- **ERROR:** nikto -h 10.0.5.1 -Tuning 123 -maxtime 60: + ERROR: Host maximum execution time of 60 seconds reached
 (2025-11-06 23:55:15)
- **ERROR:** enum4linux -a 10.0.5.1: /bin/sh: 1: enum4linux: not found
 (2025-11-06 23:55:15)
- **SMB Enum 10.0.5.1:** Skipped (enum4linux not installed) (2025-11-06 23:55:15)
- **ERROR:** snmp-check 10.0.5.1: /bin/sh: 1: snmp-check: not found
 (2025-11-06 23:55:15)
- **SNMP Check 10.0.5.1:** Skipped (snmp-check not installed) (2025-11-06 23:55:15)
- **Command Output:** nikto -h 10.0.5.10 -Tuning 123 -maxtime 60: - Nikto v2.1.5
---------------------------------------------------------------------------
+ No web server found on 10.0.5.10:80
-----------------------------------------------------------------------... (2025-11-06 23:55:40)
- **ERROR:** nikto -h 10.0.5.10 -Tuning 123 -maxtime 60: + ERROR: Host maximum execution time of 60 seconds reached
+ ERROR: Host maximum execution time of 60 seconds reached
+ ERROR: Host maximum execution time of 60 seconds reached
+ ERROR: Host maximum execution time of 60 seconds reached
 (2025-11-06 23:55:40)
- **ERROR:** enum4linux -a 10.0.5.10: /bin/sh: 1: enum4linux: not found
 (2025-11-06 23:55:40)
- **SMB Enum 10.0.5.10:** Skipped (enum4linux not installed) (2025-11-06 23:55:40)
- **ERROR:** snmp-check 10.0.5.10: /bin/sh: 1: snmp-check: not found
 (2025-11-06 23:55:40)
- **SNMP Check 10.0.5.10:** Skipped (snmp-check not installed) (2025-11-06 23:55:40)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.20: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-06 23:55 SAST
Nmap scan report for 10.0.5.20
Host is up (0.013s latency).
Not shown: 994 closed tcp ports (conn-refused)
PORT     STATE SERVICE    VE... (2025-11-06 23:56:31)
- **Service Scan 10.0.5.20:** Version detection completed (2025-11-06 23:56:31)
- **UDP Scan 10.0.5.20:** Skipped (requires root) (2025-11-06 23:56:31)
- **Command Output:** nikto -h 10.0.5.1 -Tuning 123 -maxtime 60: - Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          10.0.5.1
+ Target Hostname:    _gateway
+ Target Port:        80
+ Start Time:         ... (2025-11-06 23:56:32)
- **ERROR:** nikto -h 10.0.5.1 -Tuning 123 -maxtime 60: + ERROR: Host maximum execution time of 60 seconds reached
 (2025-11-06 23:56:32)
- **ERROR:** enum4linux -a 10.0.5.1: /bin/sh: 1: enum4linux: not found
 (2025-11-06 23:56:32)
- **SMB Enum 10.0.5.1:** Skipped (enum4linux not installed) (2025-11-06 23:56:32)
- **ERROR:** snmp-check 10.0.5.1: /bin/sh: 1: snmp-check: not found
 (2025-11-06 23:56:32)
- **SNMP Check 10.0.5.1:** Skipped (snmp-check not installed) (2025-11-06 23:56:32)
- **Command Output:** nikto -h 10.0.5.20 -Tuning 123 -maxtime 60: - Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          10.0.5.20
+ Target Hostname:    10.0.5.20
+ Target Port:        80
+ Start Time:       ... (2025-11-06 23:56:47)
- **ERROR:** nikto -h 10.0.5.20 -Tuning 123 -maxtime 60: + ERROR: Host maximum execution time of 60 seconds reached
+ ERROR: Host maximum execution time of 60 seconds reached
 (2025-11-06 23:56:47)
- **ERROR:** enum4linux -a 10.0.5.20: /bin/sh: 1: enum4linux: not found
 (2025-11-06 23:56:47)
- **SMB Enum 10.0.5.20:** Skipped (enum4linux not installed) (2025-11-06 23:56:47)
- **ERROR:** snmp-check 10.0.5.20: /bin/sh: 1: snmp-check: not found
 (2025-11-06 23:56:47)
- **SNMP Check 10.0.5.20:** Skipped (snmp-check not installed) (2025-11-06 23:56:47)
- **Completed:** 2025-11-06 23:56:47
- **Summary:** Workflow completed: 6 hosts scanned

---

- **SMB Enum 10.0.5.10:** Skipped (enum4linux not installed) (2025-11-06 23:56:57)
- **SNMP Check 10.0.5.10:** Skipped (snmp-check not installed) (2025-11-06 23:56:57)
- **SMB Enum 10.0.5.20:** Skipped (enum4linux not installed) (2025-11-06 23:58:07)
- **SNMP Check 10.0.5.20:** Skipped (snmp-check not installed) (2025-11-06 23:58:07)
- **Completed:** 2025-11-06 23:58:07
- **Summary:** Workflow completed: 6 hosts scanned

---

