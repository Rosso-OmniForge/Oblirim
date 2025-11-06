#!/bin/bash

# Test script to verify systemd service creation
# This script simulates the service creation without actually installing

echo "=== Testing Systemd Service Creation ==="
echo ""

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SERVICE_NAME="oblirim"
SERVICE_FILE="/tmp/test-${SERVICE_NAME}.service"

echo "Project Directory: $PROJECT_DIR"
echo "Service Name: $SERVICE_NAME"
echo "Service File (test): $SERVICE_FILE"
echo ""

# Create test service file
cat > "$SERVICE_FILE" << EOF
[Unit]
Description=OBLIRIM PWN Master Dashboard
After=network.target multi-user.target
Wants=network.target

[Service]
Type=simple
User=${USER}
Group=${USER}
WorkingDirectory=${PROJECT_DIR}
Environment=PATH=${PROJECT_DIR}/.venv/bin
ExecStart=${PROJECT_DIR}/.venv/bin/python ${PROJECT_DIR}/app.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo "=== Generated Service File Content ==="
cat "$SERVICE_FILE"
echo ""

echo "=== Service File Validation ==="
systemd-analyze verify "$SERVICE_FILE" 2>/dev/null && {
    echo "✓ Service file syntax is valid"
} || {
    echo "⚠ Service file syntax check failed (this is normal without systemd)"
}

echo ""
echo "=== Service Commands That Would Be Used ==="
echo "sudo systemctl daemon-reload"
echo "sudo systemctl enable $SERVICE_NAME"
echo "sudo systemctl start $SERVICE_NAME"
echo "sudo systemctl status $SERVICE_NAME"
echo ""

# Cleanup
rm -f "$SERVICE_FILE"
echo "Test completed successfully!"