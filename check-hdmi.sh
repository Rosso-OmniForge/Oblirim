#!/bin/bash
# HDMI Detection Script for OBLIRIM
# Checks if an HDMI display is connected before starting TUI
# Returns 0 if display found, 1 if not

# Method 1: Check DRM status (most reliable on modern systems)
for connector in /sys/class/drm/card*/status; do
    if [ -f "$connector" ]; then
        STATUS=$(cat "$connector" 2>/dev/null)
        if [ "$STATUS" = "connected" ]; then
            echo "HDMI display detected via DRM"
            exit 0
        fi
    fi
done

# Method 2: Check specific HDMI connector
if [ -e /sys/class/drm/card1-HDMI-A-1/status ]; then
    STATUS=$(cat /sys/class/drm/card1-HDMI-A-1/status 2>/dev/null)
    if [ "$STATUS" = "connected" ]; then
        echo "HDMI display detected on card1-HDMI-A-1"
        exit 0
    fi
fi

# Method 3: Use tvservice (Raspberry Pi specific)
if command -v tvservice >/dev/null 2>&1; then
    DISPLAY_INFO=$(tvservice -s 2>/dev/null)
    if echo "$DISPLAY_INFO" | grep -qiE "HDMI|DVI"; then
        echo "HDMI display detected via tvservice"
        exit 0
    fi
fi

# Method 4: Check vcgencmd (Raspberry Pi specific)
if command -v vcgencmd >/dev/null 2>&1; then
    DISPLAY_INFO=$(vcgencmd get_lcd_info 2>/dev/null)
    if [ -n "$DISPLAY_INFO" ]; then
        echo "Display detected via vcgencmd"
        exit 0
    fi
fi

# Method 5: Check if framebuffer device exists and has resolution
if [ -c /dev/fb0 ]; then
    if command -v fbset >/dev/null 2>&1; then
        FB_INFO=$(fbset -fb /dev/fb0 2>/dev/null)
        if echo "$FB_INFO" | grep -q "geometry"; then
            echo "Display detected via framebuffer"
            exit 0
        fi
    fi
fi

echo "No HDMI display detected"
exit 1
