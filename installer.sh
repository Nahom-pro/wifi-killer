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