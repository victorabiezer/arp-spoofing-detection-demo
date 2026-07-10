#!/usr/bin/env python3
"""
CSCI4345 network application project :)
purpose: passively watches arp traffic and flags conflicting ip/mac pairs
this version also logs alerts to a file so a live dashboard can display them
"""

from scapy.all import sniff, ARP
from datetime import datetime
import json

# keeps track of which mac address belongs to which ip
# if an ip suddenly shows up with a different mac, that's our red flag
known_devices = {}

# where we write live alerts for the dashboard to pick up
LOG_FILE = "/home/ubuntu/arp_log.jsonl"

def write_log(entry_type, message):
    # adds one line to our log file, dashboard will be watching this file for new lines
    entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "type": entry_type,  # "info", "learned", or "alert"
        "message": message
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def log_alert(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[!] {timestamp} ALERT: {message}")
    write_log("alert", message)

def process_packet(packet):
    if packet.haslayer(ARP) and packet[ARP].op == 2:  # op=2 = arp reply
        sender_ip = packet[ARP].psrc
        sender_mac = packet[ARP].hwsrc

        if sender_ip in known_devices:
            if known_devices[sender_ip] != sender_mac:
                log_alert(
                    f"possible arp spoofing detected! "
                    f"{sender_ip} was {known_devices[sender_ip]}, now claims to be {sender_mac}"
                )
        else:
            known_devices[sender_ip] = sender_mac
            message = f"learned new device: {sender_ip} is at {sender_mac}"
            print(f"[*] {message}")
            write_log("learned", message)

def main():
    # clear out any old log data so each run starts fresh
    open(LOG_FILE, "w").close()
    print("[*] arp spoof detector running, watching for conflicting ip/mac pairs...")
    print("[*] press ctrl+c to stop.\n")
    sniff(filter="arp", prn=process_packet, store=False)

if __name__ == "__main__":
    main()
