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

## Session: 2025-11-07_00-09-57_10-0-5-70-24
- **Network:** 10.0.5.70/24
- **Started:** 2025-11-07 00:09:57

- **Tool Check:** Missing tools: sslscan, enum4linux, smb-vuln-*, snmp-check, onesixtyone - Install with install.sh (2025-11-07 00:09:57)
- **Command Output:** ip link show eth0: 2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 88:a2:9e:2d:53:b4 brd ff:ff:ff:ff:ff:ff
... (2025-11-07 00:09:57)
- **Phase 1:** Interface detected → eth0 details logged (2025-11-07 00:09:57)
- **Network Range:** 10.0.5.0/24 (2025-11-07 00:09:57)
- **Network Classification:** RFC1918 Private Network (2025-11-07 00:09:57)
- **Command Output:** nmap -sn 10.0.5.0/24: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:09 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.015s latency).
Nmap scan report for 10.0.5.20
Host is up (0.052s latency).
Nmap ... (2025-11-07 00:10:00)
- **Phase 2:** nmap -sn completed → 8 hosts found (2025-11-07 00:10:00)
- **ARP Scan:** Skipped (requires root privileges) (2025-11-07 00:10:00)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.1: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:10 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.0088s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT    STATE SERV... (2025-11-07 00:10:00)
- **Port Scan 10.0.5.1:** 3 ports open (2025-11-07 00:10:00)
## Session: 2025-11-07_00-10-10_10-0-5-70-24
- **Network:** 10.0.5.70/24
- **Started:** 2025-11-07 00:10:10

- **Tool Check:** Missing tools: sslscan, enum4linux, smb-vuln-*, snmp-check, onesixtyone - Install with install.sh (2025-11-07 00:10:10)
- **Command Output:** ip link show eth0: 2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 88:a2:9e:2d:53:b4 brd ff:ff:ff:ff:ff:ff
... (2025-11-07 00:10:10)
- **Phase 1:** Interface detected → eth0 details logged (2025-11-07 00:10:10)
- **Network Range:** 10.0.5.0/24 (2025-11-07 00:10:10)
- **Network Classification:** RFC1918 Private Network (2025-11-07 00:10:10)
- **Command Output:** nmap -sn 10.0.5.0/24: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:10 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.0096s latency).
Nmap scan report for 10.0.5.20
Host is up (0.011s latency).
Nmap... (2025-11-07 00:10:14)
- **Phase 2:** nmap -sn completed → 10 hosts found (2025-11-07 00:10:14)
- **ARP Scan:** Skipped (requires root privileges) (2025-11-07 00:10:14)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.1: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:10 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.0060s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT    STATE SERV... (2025-11-07 00:10:14)
- **Port Scan 10.0.5.1:** 3 ports open (2025-11-07 00:10:14)
## Session: 2025-11-07_00-10-41_10-0-5-70-24
- **Network:** 10.0.5.70/24
- **Started:** 2025-11-07 00:10:41

- **Tool Check:** Missing tools: sslscan, enum4linux, smb-vuln-*, snmp-check, onesixtyone - Install with install.sh (2025-11-07 00:10:41)
- **Command Output:** ip link show eth0: 2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 88:a2:9e:2d:53:b4 brd ff:ff:ff:ff:ff:ff
... (2025-11-07 00:10:41)
- **Phase 1:** Interface detected → eth0 details logged (2025-11-07 00:10:41)
- **Network Range:** 10.0.5.0/24 (2025-11-07 00:10:41)
- **Network Classification:** RFC1918 Private Network (2025-11-07 00:10:41)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.1: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:10 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.020s latency).
Not shown: 997 closed tcp ports (conn-refused)
PORT    STATE SERV... (2025-11-07 00:10:42)
- **Service Scan 10.0.5.1:** Version detection completed (2025-11-07 00:10:42)
- **UDP Scan 10.0.5.1:** Skipped (requires root) (2025-11-07 00:10:42)
- **Command Output:** nmap -sn 10.0.5.0/24: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:10 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.013s latency).
Nmap scan report for 10.0.5.20
Host is up (0.013s latency).
Nmap ... (2025-11-07 00:10:44)
- **Phase 2:** nmap -sn completed → 10 hosts found (2025-11-07 00:10:44)
- **ARP Scan:** Skipped (requires root privileges) (2025-11-07 00:10:44)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.1: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:10 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.018s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT    STATE SERVI... (2025-11-07 00:10:44)
- **Port Scan 10.0.5.1:** 3 ports open (2025-11-07 00:10:44)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.10: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:10 SAST
Nmap scan report for 10.0.5.10
Host is up (0.42s latency).
All 100 scanned ports on 10.0.5.10 are in ignored states.
Not shown: 70 filt... (2025-11-07 00:10:52)
- **Port Scan 10.0.5.10:** 0 ports open (2025-11-07 00:10:52)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.10: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:10 SAST
Nmap scan report for 10.0.5.10
Host is up (0.098s latency).
All 1000 scanned ports on 10.0.5.10 are in ignored states.
Not shown: 990 f... (2025-11-07 00:11:06)
- **Service Scan 10.0.5.10:** Version detection completed (2025-11-07 00:11:06)
- **UDP Scan 10.0.5.10:** Skipped (requires root) (2025-11-07 00:11:06)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.20: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:11 SAST
Nmap scan report for 10.0.5.20
Host is up (0.0068s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT     STATE SERVICE
22/tc... (2025-11-07 00:11:11)
- **Port Scan 10.0.5.20:** 3 ports open (2025-11-07 00:11:11)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.1: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:10 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.0071s latency).
Not shown: 997 closed tcp ports (conn-refused)
PORT    STATE SER... (2025-11-07 00:11:13)
- **Service Scan 10.0.5.1:** Version detection completed (2025-11-07 00:11:13)
- **UDP Scan 10.0.5.1:** Skipped (requires root) (2025-11-07 00:11:13)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.10: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:11 SAST
Nmap scan report for 10.0.5.10
Host is up (0.052s latency).
All 100 scanned ports on 10.0.5.10 are in ignored states.
Not shown: 90 fil... (2025-11-07 00:11:16)
- **Port Scan 10.0.5.10:** 0 ports open (2025-11-07 00:11:16)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.10: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:11 SAST
Nmap scan report for 10.0.5.10
Host is up (0.056s latency).
All 1000 scanned ports on 10.0.5.10 are in ignored states.
Not shown: 990 f... (2025-11-07 00:11:47)
- **Service Scan 10.0.5.10:** Version detection completed (2025-11-07 00:11:47)
- **UDP Scan 10.0.5.10:** Skipped (requires root) (2025-11-07 00:11:47)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.20: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:11 SAST
Nmap scan report for 10.0.5.20
Host is up (0.019s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT     STATE SERVICE
22/tcp... (2025-11-07 00:11:47)
- **Port Scan 10.0.5.20:** 3 ports open (2025-11-07 00:11:47)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.20: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:11 SAST
Nmap scan report for 10.0.5.20
Host is up (0.020s latency).
Not shown: 994 closed tcp ports (conn-refused)
PORT     STATE SERVICE    VE... (2025-11-07 00:12:35)
- **Service Scan 10.0.5.20:** Version detection completed (2025-11-07 00:12:35)
- **UDP Scan 10.0.5.20:** Skipped (requires root) (2025-11-07 00:12:35)
- **Command Output:** nikto -h 10.0.5.1 -Tuning 123 -maxtime 60: - Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          10.0.5.1
+ Target Hostname:    _gateway
+ Target Port:        80
+ Start Time:         ... (2025-11-07 00:12:44)
- **ERROR:** nikto -h 10.0.5.1 -Tuning 123 -maxtime 60: + ERROR: Host maximum execution time of 60 seconds reached
 (2025-11-07 00:12:44)
- **ERROR:** enum4linux -a 10.0.5.1: /bin/sh: 1: enum4linux: not found
 (2025-11-07 00:12:44)
- **SMB Enum 10.0.5.1:** Skipped (enum4linux not installed) (2025-11-07 00:12:44)
- **ERROR:** snmp-check 10.0.5.1: /bin/sh: 1: snmp-check: not found
 (2025-11-07 00:12:44)
- **SNMP Check 10.0.5.1:** Skipped (snmp-check not installed) (2025-11-07 00:12:44)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.20: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:11 SAST
Nmap scan report for 10.0.5.20
Host is up (0.014s latency).
Not shown: 994 closed tcp ports (conn-refused)
PORT     STATE SERVICE    VE... (2025-11-07 00:13:04)
- **Service Scan 10.0.5.20:** Version detection completed (2025-11-07 00:13:04)
- **UDP Scan 10.0.5.20:** Skipped (requires root) (2025-11-07 00:13:04)
- **Command Output:** nikto -h 10.0.5.1 -Tuning 123 -maxtime 60: - Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          10.0.5.1
+ Target Hostname:    _gateway
+ Target Port:        80
+ Start Time:         ... (2025-11-07 00:13:05)
- **ERROR:** nikto -h 10.0.5.1 -Tuning 123 -maxtime 60: + ERROR: Host maximum execution time of 60 seconds reached
 (2025-11-07 00:13:05)
- **ERROR:** enum4linux -a 10.0.5.1: /bin/sh: 1: enum4linux: not found
 (2025-11-07 00:13:05)
- **SMB Enum 10.0.5.1:** Skipped (enum4linux not installed) (2025-11-07 00:13:05)
- **ERROR:** snmp-check 10.0.5.1: /bin/sh: 1: snmp-check: not found
 (2025-11-07 00:13:05)
- **SNMP Check 10.0.5.1:** Skipped (snmp-check not installed) (2025-11-07 00:13:05)
- **Command Output:** nikto -h 10.0.5.10 -Tuning 123 -maxtime 60: - Nikto v2.1.5
---------------------------------------------------------------------------
+ No web server found on 10.0.5.10:80
-----------------------------------------------------------------------... (2025-11-07 00:13:09)
- **ERROR:** nikto -h 10.0.5.10 -Tuning 123 -maxtime 60: + ERROR: Host maximum execution time of 60 seconds reached
+ ERROR: Host maximum execution time of 60 seconds reached
+ ERROR: Host maximum execution time of 60 seconds reached
+ ERROR: Host maximum execution time of 60 seconds reached
 (2025-11-07 00:13:09)
- **ERROR:** enum4linux -a 10.0.5.10: /bin/sh: 1: enum4linux: not found
 (2025-11-07 00:13:09)
- **SMB Enum 10.0.5.10:** Skipped (enum4linux not installed) (2025-11-07 00:13:09)
- **ERROR:** snmp-check 10.0.5.10: /bin/sh: 1: snmp-check: not found
 (2025-11-07 00:13:09)
- **SNMP Check 10.0.5.10:** Skipped (snmp-check not installed) (2025-11-07 00:13:09)
- **Command Output:** nikto -h 10.0.5.10 -Tuning 123 -maxtime 60: - Nikto v2.1.5
---------------------------------------------------------------------------
+ No web server found on 10.0.5.10:80
-----------------------------------------------------------------------... (2025-11-07 00:13:30)
- **ERROR:** nikto -h 10.0.5.10 -Tuning 123 -maxtime 60: + ERROR: Host maximum execution time of 60 seconds reached
+ ERROR: Host maximum execution time of 60 seconds reached
+ ERROR: Host maximum execution time of 60 seconds reached
+ ERROR: Host maximum execution time of 60 seconds reached
 (2025-11-07 00:13:30)
- **ERROR:** enum4linux -a 10.0.5.10: /bin/sh: 1: enum4linux: not found
 (2025-11-07 00:13:30)
- **SMB Enum 10.0.5.10:** Skipped (enum4linux not installed) (2025-11-07 00:13:30)
- **ERROR:** snmp-check 10.0.5.10: /bin/sh: 1: snmp-check: not found
 (2025-11-07 00:13:30)
- **SNMP Check 10.0.5.10:** Skipped (snmp-check not installed) (2025-11-07 00:13:30)
- **Command Output:** nikto -h 10.0.5.20 -Tuning 123 -maxtime 60: - Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          10.0.5.20
+ Target Hostname:    10.0.5.20
+ Target Port:        80
+ Start Time:       ... (2025-11-07 00:14:18)
- **ERROR:** nikto -h 10.0.5.20 -Tuning 123 -maxtime 60: + ERROR: Host maximum execution time of 60 seconds reached
+ ERROR: Host maximum execution time of 60 seconds reached
 (2025-11-07 00:14:18)
- **ERROR:** enum4linux -a 10.0.5.20: /bin/sh: 1: enum4linux: not found
 (2025-11-07 00:14:18)
- **SMB Enum 10.0.5.20:** Skipped (enum4linux not installed) (2025-11-07 00:14:18)
- **ERROR:** snmp-check 10.0.5.20: /bin/sh: 1: snmp-check: not found
 (2025-11-07 00:14:18)
- **SNMP Check 10.0.5.20:** Skipped (snmp-check not installed) (2025-11-07 00:14:18)
- **Completed:** 2025-11-07 00:14:18
- **Summary:** Workflow completed: 6 hosts scanned

---

- **SMB Enum 10.0.5.20:** Skipped (enum4linux not installed) (2025-11-07 00:14:37)
- **SNMP Check 10.0.5.20:** Skipped (snmp-check not installed) (2025-11-07 00:14:37)
- **Completed:** 2025-11-07 00:14:37
- **Summary:** Workflow completed: 6 hosts scanned

---

## Session: 2025-11-07_00-24-56_10-0-5-70-24
- **Network:** 10.0.5.70/24
- **Started:** 2025-11-07 00:24:56

- **Tool Check:** Missing tools: enum4linux, smb-vuln-*, snmp-check - Install with install.sh (2025-11-07 00:24:56)
- **Command Output:** ip link show eth0: 2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 88:a2:9e:2d:53:b4 brd ff:ff:ff:ff:ff:ff
... (2025-11-07 00:24:56)
- **Phase 1:** Interface detected → eth0 details logged (2025-11-07 00:24:56)
- **Network Range:** 10.0.5.0/24 (2025-11-07 00:24:56)
- **Network Classification:** RFC1918 Private Network (2025-11-07 00:24:56)
- **Command Output:** nmap -sn 10.0.5.0/24: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:24 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.013s latency).
Nmap scan report for 10.0.5.20
Host is up (0.014s latency).
Nmap ... (2025-11-07 00:24:58)
- **Phase 2:** nmap -sn completed → 11 hosts found (2025-11-07 00:24:58)
- **ARP Scan:** Skipped (requires root privileges) (2025-11-07 00:24:58)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.1: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:24 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.012s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT    STATE SERVI... (2025-11-07 00:24:58)
- **Port Scan 10.0.5.1:** 3 ports open (2025-11-07 00:24:58)
## Session: 2025-11-07_00-25-13_10-0-5-70-24
- **Network:** 10.0.5.70/24
- **Started:** 2025-11-07 00:25:13

- **Tool Check:** Missing tools: enum4linux, smb-vuln-*, snmp-check - Install with install.sh (2025-11-07 00:25:13)
- **Command Output:** ip link show eth0: 2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 88:a2:9e:2d:53:b4 brd ff:ff:ff:ff:ff:ff
... (2025-11-07 00:25:13)
- **Phase 1:** Interface detected → eth0 details logged (2025-11-07 00:25:13)
- **Network Range:** 10.0.5.0/24 (2025-11-07 00:25:13)
- **Network Classification:** RFC1918 Private Network (2025-11-07 00:25:13)
- **Command Output:** nmap -sn 10.0.5.0/24: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:25 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.0055s latency).
Nmap scan report for 10.0.5.20
Host is up (0.0065s latency).
Nma... (2025-11-07 00:25:26)
- **Phase 2:** nmap -sn completed → 11 hosts found (2025-11-07 00:25:26)
- **ARP Scan:** Skipped (requires root privileges) (2025-11-07 00:25:26)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.1: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:25 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.028s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT    STATE SERVI... (2025-11-07 00:25:26)
- **Port Scan 10.0.5.1:** 3 ports open (2025-11-07 00:25:26)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.1: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:24 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.011s latency).
Not shown: 997 closed tcp ports (conn-refused)
PORT    STATE SERV... (2025-11-07 00:25:31)
- **Service Scan 10.0.5.1:** Version detection completed (2025-11-07 00:25:31)
- **UDP Scan 10.0.5.1:** Skipped (requires root) (2025-11-07 00:25:31)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.10: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:25 SAST
Nmap scan report for 10.0.5.10
Host is up (0.087s latency).
All 100 scanned ports on 10.0.5.10 are in ignored states.
Not shown: 90 fil... (2025-11-07 00:25:35)
- **Port Scan 10.0.5.10:** 0 ports open (2025-11-07 00:25:35)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.1: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:25 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.0055s latency).
Not shown: 997 closed tcp ports (conn-refused)
PORT    STATE SER... (2025-11-07 00:25:54)
- **Service Scan 10.0.5.1:** Version detection completed (2025-11-07 00:25:54)
- **UDP Scan 10.0.5.1:** Skipped (requires root) (2025-11-07 00:25:54)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.10: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:25 SAST
Nmap scan report for 10.0.5.10
Host is up.
All 100 scanned ports on 10.0.5.10 are in ignored states.
Not shown: 100 filtered tcp ports ... (2025-11-07 00:26:05)
- **Port Scan 10.0.5.10:** 0 ports open (2025-11-07 00:26:05)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.10: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:25 SAST
Nmap scan report for 10.0.5.10
Host is up (0.086s latency).
All 1000 scanned ports on 10.0.5.10 are in ignored states.
Not shown: 990 f... (2025-11-07 00:26:08)
- **Service Scan 10.0.5.10:** Version detection completed (2025-11-07 00:26:08)
- **UDP Scan 10.0.5.10:** Skipped (requires root) (2025-11-07 00:26:08)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.20: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:26 SAST
Nmap scan report for 10.0.5.20
Host is up (0.058s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT     STATE SERVICE
22/tcp... (2025-11-07 00:26:08)
- **Port Scan 10.0.5.20:** 3 ports open (2025-11-07 00:26:08)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.10: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:26 SAST
Nmap scan report for 10.0.5.10
Host is up (0.099s latency).
All 1000 scanned ports on 10.0.5.10 are in ignored states.
Not shown: 973 f... (2025-11-07 00:26:32)
- **Service Scan 10.0.5.10:** Version detection completed (2025-11-07 00:26:32)
- **UDP Scan 10.0.5.10:** Skipped (requires root) (2025-11-07 00:26:32)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.20: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:26 SAST
Nmap scan report for 10.0.5.20
Host is up (0.011s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT     STATE SERVICE
22/tcp... (2025-11-07 00:26:33)
- **Port Scan 10.0.5.20:** 3 ports open (2025-11-07 00:26:33)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.20: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:26 SAST
Nmap scan report for 10.0.5.20
Host is up (0.014s latency).
Not shown: 994 closed tcp ports (conn-refused)
PORT     STATE SERVICE    VE... (2025-11-07 00:27:36)
- **Service Scan 10.0.5.20:** Version detection completed (2025-11-07 00:27:36)
- **UDP Scan 10.0.5.20:** Skipped (requires root) (2025-11-07 00:27:36)
- **Command Output:** nikto -h 10.0.5.1 -Tuning 123 -maxtime 30: - Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          10.0.5.1
+ Target Hostname:    _gateway
+ Target Port:        80
+ Start Time:         ... (2025-11-07 00:27:40)
- **ERROR:** nikto -h 10.0.5.1 -Tuning 123 -maxtime 30: + ERROR: Host maximum execution time of 30 seconds reached
 (2025-11-07 00:27:40)
- **Phase 4:** nikto scan on 10.0.5.1 → 1 vulnerabilities found (2025-11-07 00:27:40)
- **Command Output:** onesixtyone -c /usr/share/doc/onesixtyone/dict.txt 10.0.5.1: Scanning 1 hosts, 50 communities
... (2025-11-07 00:27:46)
- **SNMP Check 10.0.5.1:** SNMP scan completed (2025-11-07 00:27:46)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.20: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:26 SAST
Nmap scan report for 10.0.5.20
Host is up (0.12s latency).
Not shown: 994 closed tcp ports (conn-refused)
PORT     STATE SERVICE    VER... (2025-11-07 00:28:04)
- **Service Scan 10.0.5.20:** Version detection completed (2025-11-07 00:28:04)
- **UDP Scan 10.0.5.20:** Skipped (requires root) (2025-11-07 00:28:04)
- **Command Output:** nikto -h 10.0.5.1 -Tuning 123 -maxtime 30: - Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          10.0.5.1
+ Target Hostname:    _gateway
+ Target Port:        80
+ Start Time:         ... (2025-11-07 00:28:07)
- **ERROR:** nikto -h 10.0.5.1 -Tuning 123 -maxtime 30: + ERROR: Host maximum execution time of 30 seconds reached
 (2025-11-07 00:28:07)
- **Phase 4:** nikto scan on 10.0.5.1 → 1 vulnerabilities found (2025-11-07 00:28:07)
- **Command Output:** nikto -h 10.0.5.10 -Tuning 123 -maxtime 30: - Nikto v2.1.5
---------------------------------------------------------------------------
+ No web server found on 10.0.5.10:80
-----------------------------------------------------------------------... (2025-11-07 00:28:11)
- **ERROR:** nikto -h 10.0.5.10 -Tuning 123 -maxtime 30: + ERROR: Host maximum execution time of 30 seconds reached
+ ERROR: Host maximum execution time of 30 seconds reached
+ ERROR: Host maximum execution time of 30 seconds reached
+ ERROR: Host maximum execution time of 30 seconds reached
 (2025-11-07 00:28:11)
- **Command Output:** onesixtyone -c /usr/share/doc/onesixtyone/dict.txt 10.0.5.1: Scanning 1 hosts, 50 communities
... (2025-11-07 00:28:12)
- **SNMP Check 10.0.5.1:** SNMP scan completed (2025-11-07 00:28:12)
- **Command Output:** onesixtyone -c /usr/share/doc/onesixtyone/dict.txt 10.0.5.10: Scanning 1 hosts, 50 communities
... (2025-11-07 00:28:16)
- **SNMP Check 10.0.5.10:** SNMP scan completed (2025-11-07 00:28:16)
- **Command Output:** nikto -h 10.0.5.10 -Tuning 123 -maxtime 30: - Nikto v2.1.5
---------------------------------------------------------------------------
+ No web server found on 10.0.5.10:80
-----------------------------------------------------------------------... (2025-11-07 00:28:35)
- **ERROR:** nikto -h 10.0.5.10 -Tuning 123 -maxtime 30: + ERROR: Host maximum execution time of 30 seconds reached
+ ERROR: Host maximum execution time of 30 seconds reached
+ ERROR: Host maximum execution time of 30 seconds reached
+ ERROR: Host maximum execution time of 30 seconds reached
 (2025-11-07 00:28:35)
- **Command Output:** onesixtyone -c /usr/share/doc/onesixtyone/dict.txt 10.0.5.10: Scanning 1 hosts, 50 communities
... (2025-11-07 00:28:41)
- **SNMP Check 10.0.5.10:** SNMP scan completed (2025-11-07 00:28:41)
- **Command Output:** nikto -h 10.0.5.20 -Tuning 123 -maxtime 30: - Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          10.0.5.20
+ Target Hostname:    10.0.5.20
+ Target Port:        80
+ Start Time:       ... (2025-11-07 00:28:59)
- **ERROR:** nikto -h 10.0.5.20 -Tuning 123 -maxtime 30: + ERROR: Host maximum execution time of 30 seconds reached
+ ERROR: Host maximum execution time of 30 seconds reached
+ ERROR: Host maximum execution time of 30 seconds reached
 (2025-11-07 00:28:59)
- **Command Output:** onesixtyone -c /usr/share/doc/onesixtyone/dict.txt 10.0.5.20: Scanning 1 hosts, 50 communities
... (2025-11-07 00:29:04)
- **SNMP Check 10.0.5.20:** SNMP scan completed (2025-11-07 00:29:04)
- **Completed:** 2025-11-07 00:29:04
- **Summary:** Workflow completed: 6 hosts scanned

---

- **SNMP Check 10.0.5.20:** SNMP scan completed (2025-11-07 00:29:29)
- **Completed:** 2025-11-07 00:29:29
- **Summary:** Workflow completed: 6 hosts scanned

---

## Session: 2025-11-07_00-29-57_10-0-5-70-24
- **Network:** 10.0.5.70/24
- **Started:** 2025-11-07 00:29:57

- **Tool Check:** Missing tools: enum4linux, smb-vuln-*, snmp-check - Install with install.sh (2025-11-07 00:29:57)
- **Command Output:** ip link show eth0: 2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 88:a2:9e:2d:53:b4 brd ff:ff:ff:ff:ff:ff
... (2025-11-07 00:29:57)
- **Phase 1:** Interface detected → eth0 details logged (2025-11-07 00:29:57)
- **Network Range:** 10.0.5.0/24 (2025-11-07 00:29:57)
- **Network Classification:** RFC1918 Private Network (2025-11-07 00:29:57)
- **Command Output:** nmap -sn 10.0.5.0/24: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:29 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.012s latency).
Nmap scan report for 10.0.5.20
Host is up (0.018s latency).
Nmap ... (2025-11-07 00:30:02)
- **Phase 2:** nmap -sn completed → 11 hosts found (2025-11-07 00:30:02)
- **ARP Scan:** Skipped (requires root privileges) (2025-11-07 00:30:02)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.1: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:30 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.015s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT    STATE SERVI... (2025-11-07 00:30:02)
- **Port Scan 10.0.5.1:** 3 ports open (2025-11-07 00:30:02)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.1: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:30 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.0041s latency).
Not shown: 997 closed tcp ports (conn-refused)
PORT    STATE SER... (2025-11-07 00:30:31)
- **Service Scan 10.0.5.1:** Version detection completed (2025-11-07 00:30:31)
- **UDP Scan 10.0.5.1:** Skipped (requires root) (2025-11-07 00:30:31)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.10: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:30 SAST
Nmap scan report for 10.0.5.10
Host is up (0.083s latency).
All 100 scanned ports on 10.0.5.10 are in ignored states.
Not shown: 90 fil... (2025-11-07 00:30:34)
- **Port Scan 10.0.5.10:** 0 ports open (2025-11-07 00:30:34)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.10: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:30 SAST
Nmap scan report for 10.0.5.10
Host is up (0.10s latency).
All 1000 scanned ports on 10.0.5.10 are in ignored states.
Not shown: 990 fi... (2025-11-07 00:31:12)
- **Service Scan 10.0.5.10:** Version detection completed (2025-11-07 00:31:12)
- **UDP Scan 10.0.5.10:** Skipped (requires root) (2025-11-07 00:31:12)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.20: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:31 SAST
Nmap scan report for 10.0.5.20
Host is up (0.014s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT     STATE SERVICE
22/tcp... (2025-11-07 00:31:12)
- **Port Scan 10.0.5.20:** 3 ports open (2025-11-07 00:31:12)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.20: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:31 SAST
Nmap scan report for 10.0.5.20
Host is up (0.0086s latency).
Not shown: 994 closed tcp ports (conn-refused)
PORT     STATE SERVICE    V... (2025-11-07 00:32:34)
- **Service Scan 10.0.5.20:** Version detection completed (2025-11-07 00:32:34)
- **UDP Scan 10.0.5.20:** Skipped (requires root) (2025-11-07 00:32:34)
## Session: 2025-11-07_00-55-19_10-0-5-70-24
- **Network:** 10.0.5.70/24
- **Started:** 2025-11-07 00:55:19

- **Tool Check:** Missing tools: enum4linux, smb-vuln-*, snmp-check - Install with install.sh (2025-11-07 00:55:19)
- **Command Output:** ip link show eth0: 2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 88:a2:9e:2d:53:b4 brd ff:ff:ff:ff:ff:ff
... (2025-11-07 00:55:19)
- **Phase 1:** Interface detected → eth0 details logged (2025-11-07 00:55:19)
- **Network Range:** 10.0.5.0/24 (2025-11-07 00:55:19)
- **Network Classification:** RFC1918 Private Network (2025-11-07 00:55:19)
- **Command Output:** nmap -sn 10.0.5.0/24: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:55 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.012s latency).
Nmap scan report for 10.0.5.20
Host is up (0.094s latency).
Nmap ... (2025-11-07 00:55:23)
- **Phase 2:** nmap -sn completed → 9 hosts found (2025-11-07 00:55:23)
- **ARP Scan:** Skipped (requires root privileges) (2025-11-07 00:55:23)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.1: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:55 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.015s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT    STATE SERVI... (2025-11-07 00:55:23)
- **Port Scan 10.0.5.1:** 3 ports open (2025-11-07 00:55:23)
## Session: 2025-11-07_00-55-33_10-0-5-70-24
- **Network:** 10.0.5.70/24
- **Started:** 2025-11-07 00:55:33

- **Tool Check:** Missing tools: enum4linux, smb-vuln-*, snmp-check - Install with install.sh (2025-11-07 00:55:33)
- **Command Output:** ip link show eth0: 2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 88:a2:9e:2d:53:b4 brd ff:ff:ff:ff:ff:ff
... (2025-11-07 00:55:33)
- **Phase 1:** Interface detected → eth0 details logged (2025-11-07 00:55:33)
- **Network Range:** 10.0.5.0/24 (2025-11-07 00:55:33)
- **Network Classification:** RFC1918 Private Network (2025-11-07 00:55:33)
- **Command Output:** nmap -sn 10.0.5.0/24: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:55 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.0068s latency).
Nmap scan report for 10.0.5.20
Host is up (0.033s latency).
Nmap... (2025-11-07 00:55:50)
- **Phase 2:** nmap -sn completed → 11 hosts found (2025-11-07 00:55:50)
- **ARP Scan:** Skipped (requires root privileges) (2025-11-07 00:55:50)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.1: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:55 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.016s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT    STATE SERVI... (2025-11-07 00:55:50)
- **Port Scan 10.0.5.1:** 3 ports open (2025-11-07 00:55:50)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.1: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:55 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.019s latency).
Not shown: 997 closed tcp ports (conn-refused)
PORT    STATE SERV... (2025-11-07 00:55:56)
- **Service Scan 10.0.5.1:** Version detection completed (2025-11-07 00:55:56)
- **UDP Scan 10.0.5.1:** Skipped (requires root) (2025-11-07 00:55:56)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.10: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:55 SAST
Nmap scan report for 10.0.5.10
Host is up (0.11s latency).
All 100 scanned ports on 10.0.5.10 are in ignored states.
Not shown: 90 filt... (2025-11-07 00:55:59)
- **Port Scan 10.0.5.10:** 0 ports open (2025-11-07 00:55:59)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.1: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:55 SAST
Nmap scan report for _gateway (10.0.5.1)
Host is up (0.014s latency).
Not shown: 997 closed tcp ports (conn-refused)
PORT    STATE SERV... (2025-11-07 00:56:19)
- **Service Scan 10.0.5.1:** Version detection completed (2025-11-07 00:56:19)
- **UDP Scan 10.0.5.1:** Skipped (requires root) (2025-11-07 00:56:19)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.10: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:56 SAST
Nmap scan report for 10.0.5.10
Host is up.
All 100 scanned ports on 10.0.5.10 are in ignored states.
Not shown: 100 filtered tcp ports ... (2025-11-07 00:56:30)
- **Port Scan 10.0.5.10:** 0 ports open (2025-11-07 00:56:30)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.10: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:55 SAST
Nmap scan report for 10.0.5.10
Host is up (0.054s latency).
All 1000 scanned ports on 10.0.5.10 are in ignored states.
Not shown: 990 f... (2025-11-07 00:56:30)
- **Service Scan 10.0.5.10:** Version detection completed (2025-11-07 00:56:30)
- **UDP Scan 10.0.5.10:** Skipped (requires root) (2025-11-07 00:56:30)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.20: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:56 SAST
Nmap scan report for 10.0.5.20
Host is up (0.0080s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT     STATE SERVICE
22/tc... (2025-11-07 00:56:31)
- **Port Scan 10.0.5.20:** 3 ports open (2025-11-07 00:56:31)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.10: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:56 SAST
Nmap scan report for 10.0.5.10
Host is up (0.084s latency).
All 1000 scanned ports on 10.0.5.10 are in ignored states.
Not shown: 990 f... (2025-11-07 00:56:43)
- **Service Scan 10.0.5.10:** Version detection completed (2025-11-07 00:56:43)
- **UDP Scan 10.0.5.10:** Skipped (requires root) (2025-11-07 00:56:43)
- **Command Output:** nmap -sT -T4 --top-ports 100 -Pn 10.0.5.20: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:56 SAST
Nmap scan report for 10.0.5.20
Host is up (0.025s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT     STATE SERVICE
22/tcp... (2025-11-07 00:56:43)
- **Port Scan 10.0.5.20:** 3 ports open (2025-11-07 00:56:43)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.20: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:56 SAST
Nmap scan report for 10.0.5.20
Host is up (0.024s latency).
Not shown: 994 closed tcp ports (conn-refused)
PORT     STATE SERVICE    VE... (2025-11-07 00:57:52)
- **Service Scan 10.0.5.20:** Version detection completed (2025-11-07 00:57:52)
- **UDP Scan 10.0.5.20:** Skipped (requires root) (2025-11-07 00:57:52)
- **Command Output:** nikto -h 10.0.5.1 -Tuning 123 -maxtime 30: - Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          10.0.5.1
+ Target Hostname:    _gateway
+ Target Port:        80
+ Start Time:         ... (2025-11-07 00:57:53)
- **ERROR:** nikto -h 10.0.5.1 -Tuning 123 -maxtime 30: + ERROR: Host maximum execution time of 30 seconds reached
 (2025-11-07 00:57:53)
- **Phase 4:** nikto scan on 10.0.5.1 → 1 vulnerabilities found (2025-11-07 00:57:53)
- **Command Output:** onesixtyone -c /usr/share/doc/onesixtyone/dict.txt 10.0.5.1: Scanning 1 hosts, 50 communities
... (2025-11-07 00:57:58)
- **SNMP Check 10.0.5.1:** SNMP scan completed (2025-11-07 00:57:58)
- **Command Output:** nmap -sV -sC -Pn 10.0.5.20: Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-07 00:56 SAST
Nmap scan report for 10.0.5.20
Host is up (0.014s latency).
Not shown: 994 closed tcp ports (conn-refused)
PORT     STATE SERVICE    VE... (2025-11-07 00:58:14)
- **Service Scan 10.0.5.20:** Version detection completed (2025-11-07 00:58:14)
- **UDP Scan 10.0.5.20:** Skipped (requires root) (2025-11-07 00:58:14)
- **Command Output:** nikto -h 10.0.5.1 -Tuning 123 -maxtime 30: - Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          10.0.5.1
+ Target Hostname:    _gateway
+ Target Port:        80
+ Start Time:         ... (2025-11-07 00:58:15)
- **ERROR:** nikto -h 10.0.5.1 -Tuning 123 -maxtime 30: + ERROR: Host maximum execution time of 30 seconds reached
 (2025-11-07 00:58:15)
- **Phase 4:** nikto scan on 10.0.5.1 → 1 vulnerabilities found (2025-11-07 00:58:15)
- **Command Output:** onesixtyone -c /usr/share/doc/onesixtyone/dict.txt 10.0.5.1: Scanning 1 hosts, 50 communities
... (2025-11-07 00:58:20)
- **SNMP Check 10.0.5.1:** SNMP scan completed (2025-11-07 00:58:20)
- **Command Output:** nikto -h 10.0.5.10 -Tuning 123 -maxtime 30: - Nikto v2.1.5
---------------------------------------------------------------------------
+ No web server found on 10.0.5.10:80
-----------------------------------------------------------------------... (2025-11-07 00:58:23)
- **ERROR:** nikto -h 10.0.5.10 -Tuning 123 -maxtime 30: + ERROR: Host maximum execution time of 30 seconds reached
+ ERROR: Host maximum execution time of 30 seconds reached
+ ERROR: Host maximum execution time of 30 seconds reached
+ ERROR: Host maximum execution time of 30 seconds reached
 (2025-11-07 00:58:23)
- **Command Output:** onesixtyone -c /usr/share/doc/onesixtyone/dict.txt 10.0.5.10: Scanning 1 hosts, 50 communities
... (2025-11-07 00:58:29)
- **SNMP Check 10.0.5.10:** SNMP scan completed (2025-11-07 00:58:29)
- **Command Output:** nikto -h 10.0.5.10 -Tuning 123 -maxtime 30: - Nikto v2.1.5
---------------------------------------------------------------------------
+ No web server found on 10.0.5.10:80
-----------------------------------------------------------------------... (2025-11-07 00:58:45)
- **ERROR:** nikto -h 10.0.5.10 -Tuning 123 -maxtime 30: + ERROR: Host maximum execution time of 30 seconds reached
+ ERROR: Host maximum execution time of 30 seconds reached
+ ERROR: Host maximum execution time of 30 seconds reached
+ ERROR: Host maximum execution time of 30 seconds reached
 (2025-11-07 00:58:45)
- **Command Output:** onesixtyone -c /usr/share/doc/onesixtyone/dict.txt 10.0.5.10: Scanning 1 hosts, 50 communities
... (2025-11-07 00:58:50)
- **SNMP Check 10.0.5.10:** SNMP scan completed (2025-11-07 00:58:50)
- **Command Output:** nikto -h 10.0.5.20 -Tuning 123 -maxtime 30: - Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          10.0.5.20
+ Target Hostname:    10.0.5.20
+ Target Port:        80
+ Start Time:       ... (2025-11-07 00:59:11)
- **ERROR:** nikto -h 10.0.5.20 -Tuning 123 -maxtime 30: + ERROR: Host maximum execution time of 30 seconds reached
+ ERROR: Host maximum execution time of 30 seconds reached
+ ERROR: Host maximum execution time of 30 seconds reached
 (2025-11-07 00:59:11)
- **Command Output:** onesixtyone -c /usr/share/doc/onesixtyone/dict.txt 10.0.5.20: Scanning 1 hosts, 50 communities
... (2025-11-07 00:59:17)
- **SNMP Check 10.0.5.20:** SNMP scan completed (2025-11-07 00:59:17)
- **Completed:** 2025-11-07 00:59:17
- **Summary:** Workflow completed: 6 hosts scanned

---

- **SNMP Check 10.0.5.20:** SNMP scan completed (2025-11-07 00:59:38)
- **Completed:** 2025-11-07 00:59:38
- **Summary:** Workflow completed: 6 hosts scanned

---

