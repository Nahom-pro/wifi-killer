#!/usr/bin/env python3

import subprocess, os, sys, time, re, psutil
from datetime import datetime
from termcolor import colored

# === CONFIG ===
BASE_LOG_DIR = "logs"
SESSION_DIR = os.path.join(BASE_LOG_DIR, f"session_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
TMP_PREFIX = "/tmp/airodump_output"
TMP_CSV = TMP_PREFIX + "-01.csv"
PID_FILE = os.path.join(SESSION_DIR, "deauth.pid")
CLIENT_LOG = os.path.join(SESSION_DIR, "clients.log")
IFACE = ""
MONITOR_IFACE = ""

# === VISUALS ===
def banner():
    os.system("clear")
    print("\n")
    os.system("figlet -c 'ShadoWalker  by  Nahom' | /usr/games/lolcat -a -d 2")
    print(colored("═" * 50, "cyan"))
    print(colored("  Aggressively Deauth Unauthorized Clients", "cyan"))
    print(colored("═" * 50 + "\n", "cyan"))

def status(msg, symbol="[*]", color="cyan"): print(colored(f"{symbol} {msg}", color))
def success(msg): status(msg, "[✓]", "green")
def error(msg): status(msg, "[✗]", "red")
def line(): print(colored("─" * 50, "blue"))

# === INTERFACE DETECTION ===
def detect_iface():
    global IFACE
    result = subprocess.getoutput("iw dev")
    match = re.search(r"Interface\s+(\w+)", result)
    IFACE = match.group(1) if match else "wlan0"
    success(f"Interface selected: {IFACE}")

def start_monitor():
    global MONITOR_IFACE
    subprocess.run(["airmon-ng", "start", IFACE], stdout=subprocess.DEVNULL)
    MONITOR_IFACE = IFACE + "mon"
    success(f"Monitor mode enabled on {MONITOR_IFACE}")

def stop_monitor():
    subprocess.run(["airmon-ng", "stop", MONITOR_IFACE], stdout=subprocess.DEVNULL)
    subprocess.run(["systemctl", "start", "NetworkManager"], stdout=subprocess.DEVNULL)
    success("Restored managed mode & restarted NetworkManager.")

# === AIRODUMP ===
def scan_aps():
    status("Opening GNOME terminal to scan nearby APs...")
    cmd = f"sudo airodump-ng -w {TMP_PREFIX} --output-format csv {MONITOR_IFACE}"
    gnome_cmd = f"sudo -u \"$(logname)\" gnome-terminal -- bash -c \"{cmd}; exec bash\""
    os.system(gnome_cmd)
    input(colored("\n[Enter] when ready to continue: ", "green"))

