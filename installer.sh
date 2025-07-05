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

# === STEP 4: Create Desktop Entry with Root Prompt ===
echo "[*] Creating desktop launcher at $DESKTOP_ENTRY..."

cat <<EOF | sudo tee "$DESKTOP_ENTRY" > /dev/null
[DesktopEntry]
Version=1.0
Type=Application
Name=$APP_NAME
Comment=Aggressive Wi‑Fi deauthentication tool
Exec=pkexec env DISPLAY=\$DISPLAY XAUTHORITY=\$XAUTHORITY gnome-terminal -- bash -c 'python3 $INSTALL_DIR/enforcer.py; exec bash'
Icon=$APP_ID
Terminal=false
Categories=Network;Security;
StartupNotify=true
EOF

# === STEP 5: Update Icon Cache (optional) ===
sudo gtk-update-icon-cache /usr/share/icons/hicolor/ 2>/dev/null || true

echo "[✓] $APP_NAME installed successfully!"
echo "➡️  You can now launch it from your Applications menu."
