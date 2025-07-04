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