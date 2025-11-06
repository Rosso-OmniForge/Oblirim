# OBLIRIM Auto-Start Configuration

## What the install.sh script does:

### 1. Creates Systemd Service
- **Service file**: `/etc/systemd/system/oblirim.service`
- **Service name**: `oblirim`
- **Auto-start**: Enabled on boot
- **Auto-restart**: Enabled with 10-second delay

### 2. Service Configuration
```ini
[Unit]
Description=OBLIRIM PWN Master Dashboard
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
User=YOUR_USER
Group=YOUR_USER
WorkingDirectory=/path/to/oblirim
Environment=PATH=/path/to/oblirim/.venv/bin
ExecStart=/path/to/oblirim/.venv/bin/python /path/to/oblirim/app.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### 3. Service Management Commands
```bash
# Service control
sudo systemctl start oblirim      # Start service
sudo systemctl stop oblirim       # Stop service
sudo systemctl restart oblirim    # Restart service
sudo systemctl status oblirim     # Check status
sudo systemctl enable oblirim     # Enable auto-start (done by installer)
sudo systemctl disable oblirim    # Disable auto-start

# Logs
sudo journalctl -u oblirim -f     # Follow logs
sudo journalctl -u oblirim -n 50  # Last 50 log entries
```

### 4. Utility Scripts Created
- `./start.sh` - Start the service
- `./stop.sh` - Stop the service  
- `./restart.sh` - Restart the service
- `./status.sh` - Check status and recent logs

### 5. What Happens on Boot
1. System boots up
2. Network comes online
3. `oblirim.service` starts automatically
4. Dashboard becomes available at `http://pi-ip:5000`
5. If service crashes, it automatically restarts after 10 seconds

### 6. Manual Service Creation (if needed)
If you need to manually create the service:

```bash
# 1. Create service file
sudo nano /etc/systemd/system/oblirim.service

# 2. Add the service configuration (see template above)

# 3. Reload systemd
sudo systemctl daemon-reload

# 4. Enable auto-start
sudo systemctl enable oblirim

# 5. Start service
sudo systemctl start oblirim
```

### 7. Troubleshooting
```bash
# Check if service is running
systemctl is-active oblirim

# Check service status
sudo systemctl status oblirim

# View recent logs
sudo journalctl -u oblirim --no-pager -n 20

# Restart if needed
sudo systemctl restart oblirim
```

The install script handles ALL of this automatically!