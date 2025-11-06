#!/bin/bash
set -e

# -------------------------------------------------
# Universal Chrome Kiosk Installer (Raspberry Pi 3 – Bookworm)
# Run as your normal user (e.g. nero). One-time only.
# -------------------------------------------------

USER=$(whoami)
if [ "$USER" = "root" ]; then
  echo "ERROR: Do not run as root. Run as your user."
  exit 1
fi

echo "Setting up Chrome kiosk for user: $USER"
echo "Target: http://localhost:3000 on HDMI"
echo

# 1. Install required packages
sudo apt update
sudo apt install -y chromium xinit openbox unclutter xserver-xorg

# 2. Force X11 (disable Wayland)
sudo raspi-config nonint do_wayland 0

# 3. Add user to required groups
sudo usermod -aG video,tty,adm,sudo "$USER"

# 4. Create .xinitrc – launches Chromium in kiosk mode
cat > "/home/$USER/.xinitrc" <<'EOF'
#!/bin/sh
# Hide cursor
unclutter -idle 0 -root &

# Disable screen blanking
xset s off
xset s noblank
xset -dpms

# Minimal window manager
openbox-session &

# Launch Chromium in true kiosk mode
exec chromium \
  --kiosk \
  --no-first-run \
  --noerrdialogs \
  --disable-infobars \
  --incognito \
  --disable-restore-session-state \
  --start-maximized \
  "http://localhost:3000"
EOF
chmod +x "/home/$USER/.xinitrc"

# 5. Boot to console + auto-login on tty1
sudo systemctl set-default multi-user.target
sudo mkdir -p /etc/systemd/system/getty@tty1.service.d
sudo tee /etc/systemd/system/getty@tty1.service.d/autologin.conf > /dev/null <<EOF
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin $USER --noclear %I \$TERM
EOF

# 6. Auto-start X after login
grep -q "startx" "/home/$USER/.bash_profile" 2>/dev/null || cat >> "/home/$USER/.bash_profile" <<'EOF'

# Auto-start X on tty1
if [[ -z "$DISPLAY" ]] && [[ $(tty) = /dev/tty1 ]]; then
  exec startx
fi
EOF

# 7. Disable screen blanking globally
sudo mkdir -p /etc/X11/xorg.conf.d
sudo tee /etc/X11/xorg.conf.d/10-disable-blanking.conf > /dev/null <<'EOF'
Section "ServerFlags"
    Option "BlankTime"  "0"
    Option "StandbyTime" "0"
    Option "SuspendTime" "0"
    Option "OffTime"     "0"
EndSection
Section "Monitor"
    Identifier "HDMI-1"
    Option "DPMS" "false"
EndSection
EOF

# 8. Optional: Hide boot splash (clean black screen)
sudo raspi-config nonint do_boot_splash 1

# -------------------------------------------------
echo
echo "INSTALL COMPLETE"
echo "------------------------------------------------"
echo "Next: Reboot the Pi"
echo "   sudo reboot"
echo
echo "After reboot:"
echo "  → HDMI screen boots directly into Chrome kiosk"
echo "  → http://localhost:3000 in full-screen"
echo "  → No cursor, no address bar, no exit"
echo
echo "Recovery:"
echo "  Press Ctrl+Alt+F3 → login as $USER"
echo "  Run: sudo systemctl restart getty@tty1"
echo "------------------------------------------------"
# -------------------------------------------------