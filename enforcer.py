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

def parse_csv():
    aps = []
    try:
        with open(TMP_CSV, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if re.match(r"(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}", line):
                    parts = [x.strip() for x in line.split(",")]
                    if len(parts) > 13:
                        aps.append({
                            "BSSID": parts[0],
                            "Channel": parts[3],
                            "ESSID": parts[13]
                        })
    except FileNotFoundError:
        error("Scan result not found.")
    return aps

def choose_ap(aps):
    print(colored("\n📡 Available Access Points:", "magenta", attrs=["bold"]))
    for i, ap in enumerate(aps):
        essid = ap["ESSID"] if ap["ESSID"] else "[Hidden]"
        print(colored(f"{i}) {essid:20} {ap['BSSID']}  Ch:{ap['Channel']}", "white"))
    try:
        idx = int(input(colored("\nSelect AP number to protect: ", "green")))
        return aps[idx]
    except:
        error("Invalid selection.")
        stop_monitor()
        sys.exit(1)

# === DEAUTH MANAGEMENT ===
def start_deauth(bssid, channel):
    os.makedirs(SESSION_DIR, exist_ok=True)
    # Create empty client log file if it doesn't exist
    open(CLIENT_LOG, 'a').close()
    
    log_file = os.path.join(SESSION_DIR, "deauth.log")
    cmd = f"nohup python3 background_deauth.py {MONITOR_IFACE} {bssid} {channel} {CLIENT_LOG} > {log_file} 2>&1 & echo $! > {PID_FILE}"
    os.system(cmd)
    success("Deauth started in background.")
    status(f"BSSID: {bssid} | Channel: {channel}")
    status(f"Session log: {log_file}")
    status(f"Clients: {CLIENT_LOG}")
    print(colored("\n[✓] You can close this terminal. Attack will continue.\n", "green"))

def stop_deauth():
    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r") as f:
            pid = f.read().strip()
            try:
                process = psutil.Process(int(pid))
                process.terminate()
                success("Deauth process stopped.")
            except psutil.NoSuchProcess:
                error("No active deauth process found.")
        os.remove(PID_FILE)
        stop_monitor()
    else:
        error("No active deauth session.")

def view_status():
    print(colored("\n[📋] Active Deauthed Clients Log:", "yellow"))
    if os.path.exists(CLIENT_LOG):
        try:
            with open(CLIENT_LOG, "r") as f:
                lines = f.readlines()
                if lines:
                    print("".join(lines[-10:]))
                else:
                    print(colored("No clients deauthed yet.\n", "blue"))
        except:
            print(colored("Log file is empty.\n", "blue"))
    else:
        print(colored("No log file found.\n", "red"))


# === MAIN MENU ===
def main():
    banner()
    detect_iface()
    start_monitor()
    while True:
        line()
        print(colored("[1] Start Deauth   [2] Stop Deauth   [3] View Status   [4] Exit", "cyan"))
        choice = input(colored("Choice: ", "green"))
        if choice == "1":
            os.system(f"rm -f {TMP_PREFIX}-*")
            scan_aps()
            aps = parse_csv()
            if not aps:
                error("No APs found.")
                continue
            ap = choose_ap(aps)
            start_deauth(ap["BSSID"], ap["Channel"])
            
        elif choice == "2":
            stop_deauth()
        elif choice == "3":
            view_status()
        elif choice == "4":
            stop_monitor()
            print(colored("\n[✓] Exiting... Goodbye!\n", "green"))
            break
        else:
            error("Invalid option.")
