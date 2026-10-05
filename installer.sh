#!/usr/bin/env bash
set -e

# === CONFIG ===
APP_NAME="wifi-killer"
APP_ID="wi-fi-enforcer"
INSTALL_DIR="/opt/$APP_ID"
ICON_PATH="/usr/share/icons/hicolor/64x64/apps/$APP_ID.png"
DESKTOP_ENTRY="/usr/share/applications/$APP_NAME.desktop"
LEGACY_DESKTOP_ENTRY="/usr/share/applications/$APP_ID.desktop"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

echo "[*] Installing $APP_NAME..."

# === STEP 1: Install runtime dependencies ===
if ! command -v apt-get >/dev/null 2>&1; then
    echo "[!] This installer currently supports Debian/Ubuntu systems only."
    exit 1
fi

sudo apt-get install -y \
    aircrack-ng figlet iw lolcat network-manager \
    python3-psutil python3-scapy python3-termcolor

# === STEP 2: Create Installation Directory ===
sudo mkdir -p "$INSTALL_DIR" "$(dirname "$ICON_PATH")"

# === STEP 3: Copy Core Scripts ===
sudo install -m 755 "$SCRIPT_DIR/enforcer.py" "$SCRIPT_DIR/background_deauth.py" "$INSTALL_DIR/"

# === STEP 4: Copy Icon ===
if [ -f "$SCRIPT_DIR/assets/enforcer.png" ]; then
    sudo install -m 644 "$SCRIPT_DIR/assets/enforcer.png" "$ICON_PATH"
else
    echo "[!] Icon not found at assets/enforcer.png. Using default icon."
    ICON_PATH="/usr/share/icons/hicolor/64x64/apps/network-wifi.png"
fi

# === STEP 5: Create Desktop Entry ===
echo "[*] Creating desktop launcher at $DESKTOP_ENTRY..."

# Remove the old launcher ID so GNOME cannot retain its previous command.
sudo rm -f "$LEGACY_DESKTOP_ENTRY"

cat <<EOF | sudo tee "$DESKTOP_ENTRY" > /dev/null
[Desktop Entry]
Version=1.0
Type=Application
Name=$APP_NAME
Comment=Aggressive Wi‑Fi deauthentication tool
Exec=pkexec /usr/bin/python3 $INSTALL_DIR/enforcer.py
Icon=$APP_ID
Terminal=true
Categories=Network;Security;
StartupNotify=true
EOF
sudo chmod 644 "$DESKTOP_ENTRY"

# === STEP 6: Refresh desktop and icon caches ===
sudo update-desktop-database /usr/share/applications 2>/dev/null || true
sudo gtk-update-icon-cache -f -t /usr/share/icons/hicolor/ 2>/dev/null || true

echo "[✓] $APP_NAME installed successfully!"
echo "➡️  You can now launch it from your Applications menu."
