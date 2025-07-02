# 🛡️ ShadoWalker — >   Wi‑Fi Killer

```bash
   ____  _               _    __        __    _ _                _           
  / ___|| |__   __ _  __| | __\ \      / /_ _| | | _____ _ __   | |__  _   _ 
  \___ \| '_ \ / _` |/ _` |/ _ \ \ /\ / / _` | | |/ / _ \ '__|  | '_ \| | | |
   ___) | | | | (_| | (_| | (_) \ V  V / (_| | |   <  __/ |     | |_) | |_| |
  |____/|_| |_|\__,_|\__,_|\___/ \_/\_/ \__,_|_|_|\_\___|_|     |_.__/ \__, |
                                                                       |___/ 
                       _   _       _                     
                      | \ | | __ _| |__   ___  _ __ ___  
                      |  \| |/ _` | '_ \ / _ \| '_ ` _ \ 
                      | |\  | (_| | | | | (_) | | | | | |
                      |_| \_|\__,_|_| |_|\___/|_| |_| |_|

```

---

## 📌 Project Overview

**ShadoWalker** is a terminal-based, aggressive Wi‑Fi enforcement tool developed for **Kali Linux**.

This script protects your chosen Wi‑Fi network by continuously deauthenticating unknown or unauthorized devices. It is built for ethical hackers, red teamers, and wireless researchers who want fine control over their network security.

---

## ✨ Features

- ✅ Auto-detect wireless interfaces
- ✅ Automatically enable monitor mode
- ✅ Interactive Access Point selection via `airodump-ng`
- ✅ Background persistent deauthentication (via `scapy`)
- ✅ Whitelist MAC addresses to avoid deauthing trusted devices
- ✅ Real-time session logging and client tracking
- ✅ Safe shutdown, return to managed mode, and NetworkManager restart
- ✅ Decorative, user-friendly terminal UI with `figlet` + `lolcat`
- ✅ Desktop launcher for GNOME-based systems
- ✅ Installer script included

---

## 🔧 Installation

```bash
git clone https://github.com/nahom-pro/shadowalker.git
cd shadowalker
chmod +x installer.sh
sudo ./installer.sh
```

✅ You will find **Wi‑Fi Enforcer** in your Applications Menu after installation.

You can also launch it using:

```bash
sudo wifi-enforcer
```

---

## 🚀 Usage Guide

### ➤ Menu Options

```
[1] Start Deauth
[2] Stop Deauth
[3] View Status
[4] Exit
```

### ➤ Workflow

1. GNOME terminal opens with `airodump-ng` scanning.
2. Press `Ctrl+C` to stop scan.
3. Select AP to protect.
4. Persistent deauth starts in the background.

---

## 🔐 Whitelisting

To exclude devices from being deauthed:

Edit `whitelist[]` on backround_deauth.py:

```
whitelist[
'00:11:22:33:44:55',
'AA:BB:CC:DD:EE:FF'
]
```

---

## 🧾 Sample Log Output

```
[2025-06-30 03:36:22] Deauthed: CC:B1:82:88:38:E4 
[2025-06-30 03:37:01] Deauthed: 28:77:77:4D:15:32 
```

---

## 📦 Dependencies

```bash
sudo apt install aircrack-ng python3-scapy figlet lolcat gnome-terminal
```

---

## 🧠 How It Works

- Detect interface → Monitor mode
- AP scan (GNOME terminal)
- AP selection
- Background deauth
- Session logging
- Safe exit → restores managed mode

---

## ⚠️ Disclaimer

**This tool is for authorized testing only.**  
Unauthorized use is illegal and unethical.

---

## 📜 License

Licensed under the [MIT License](LICENSE)

---

## 👤 Author

**Nahom**  
Cyber Security Expert  
GitHub: [github.com/nahom-pro](https://github.com/nahom-pro)