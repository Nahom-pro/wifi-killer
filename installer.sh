#!/usr/bin/env bash
set -e
# === CONFIG ===
APP_NAME="Wi‑Fi Enforcer"
APP_ID="wi-fi-enforcer"
INSTALL_DIR="/opt/$APP_ID"
ICON_PATH="/usr/share/icons/hicolor/64x64/apps/$APP_ID.png"
DESKTOP_ENTRY="/usr/share/applications/$APP_ID.desktop"

echo "[*] Installing $APP_NAME..."

# === STEP 1: Create Installation Directory ===
sudo mkdir -p "$INSTALL_DIR/assets"
# === STEP 2: Copy Core Scripts ===
sudo cp enforcer.py background_deauth.py "$INSTALL_DIR/"
sudo chmod +x "$INSTALL_DIR/enforcer.py" "$INSTALL_DIR/background_deauth.py"

# === STEP 3: Copy Icon ===
if [ -f assets/enforcer.png ]; then
    sudo cp assets/enforcer.png "$ICON_PATH"
else
    echo "[!] Icon not found at assets/enforcer.png. Using default icon."
    ICON_PATH="/usr/share/icons/hicolor/64x64/apps/network-wifi.png"
fi
