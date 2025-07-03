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