<img width="1536" height="1024" alt="hotel_scenario" src="https://github.com/user-attachments/assets/07d63f3c-167b-4106-8b62-0d1dc4c88926" /># ARP Spoofing Demo + Live Detection Dashboard

CSCI4345 Network Application Project, Summer I 2026 UTRGV

## what this is

this project demonstrates an ARP spoofing (man-in-the-middle) attack against a real device on my home network, then builds a detector that catches the attack live, and finally a browser dashboard that shows the whole thing happening in real time in plain english.

the target device is my Apple TV. the "victim" and "attacker" are both real, this isn't three VMs pretending to be different computers, it's an actual attack against an actual device on my own network, using a VM as the attacker.

## why this matters

the Link Layer (where ARP lives) trusts everyone by default. any device on a local network can claim to be any other device, and nothing stops it. this is exactly how man-in-the-middle attacks work on public wifi, in offices, in hotels, anywhere a network doesn't segment or verify who's who at Layer 2.

this project shows the vulnerability, then shows a real, working defense against it.

## the scenario

<img width="1536" height="1024" alt="hotel_scenario" src="https://github.com/user-attachments/assets/d34c57b7-e79d-4a9b-9863-ac02a05023b7" />

imagine a small hotel lobby with a shared wifi network for guests and staff (a common real-world mistake). the lobby has a smart TV (the Apple TV) for guest use. a "guest" sitting in the lobby with a laptop performs an ARP spoofing attack, positioning themselves between the TV and the router, and can now see its traffic. this is why hotels, cafes, and offices should never mix guest and internal networks without protection. the "IT consultant" then patches the vulnerability with a live detection tool.

## project structure

```
arp_spoof_public.py     # the attack script (MAC addresses masked for public repo)
arp_detector.py         # passively watches for ARP spoofing and logs alerts
dashboard_server.py     # small Flask server that streams detector alerts live
dashboard.html          # browser dashboard, connects to the server and visualizes attacks in real time
screenshots/            # proof of each stage working
```

note: the MAC addresses in `arp_spoof_public.py` and `dashboard.html` are partially masked for privacy. real values were used during actual testing, shown in the screenshots and demo video.

## how it works

**the attack (`arp_spoof_public.py`)**
sends forged ARP replies to two targets at once. tells the Apple TV "I am the router," and tells the router "I am the Apple TV." both sides start routing their traffic through the attacker machine instead of directly to each other. IP forwarding is enabled on the attacker so traffic still flows through normally, meaning the target doesn't lose internet and the attack stays quiet.

**the detector (`arp_detector.py`)**
passively sniffs ARP traffic and remembers which MAC address belongs to which IP. if an IP that was already seen suddenly claims a different MAC, that's the red flag, it's exactly what the spoofing script does. every alert gets timestamped, printed to the terminal, and also logged to a file for the dashboard to pick up.

**the dashboard (`dashboard_server.py` + `dashboard.html`)**
the server watches the detector's log file and streams new lines out to the browser the moment they happen (using server-sent events). the dashboard itself is styled to look like a structured terminal view, it's not replacing the real terminal output, it's a second, more readable way to watch the same real data live. when an alert comes through, the affected devices flip from "normal" to "spoofed" and a plain-english explanation shows up under the alert.

## how to run it

1. get the real MAC addresses for your target device and gateway (see "finding MAC addresses" below)
2. fill those into `arp_spoof_public.py` in place of the masked values
3. start the dashboard server: `sudo python3 dashboard_server.py`
4. start the detector: `sudo python3 arp_detector.py`
5. open `dashboard.html` in a browser on a machine that can reach the server's IP
6. run the attack: `sudo python3 arp_spoof_public.py`
7. watch the dashboard update live, then `ctrl+c` the attack script to stop and restore ARP tables

## finding MAC addresses

send an ARP request directly to the target's IP and read the reply:

```python
from scapy.all import ARP, Ether, srp
arp = ARP(pdst='TARGET_IP')
ether = Ether(dst='ff:ff:ff:ff:ff:ff')
result = srp(ether/arp, timeout=2, verbose=True)[0]
for sent, received in result:
    print(received.psrc, received.hwsrc)
```

## troubleshooting / things that went wrong along the way

**router-level ARP defense**
my home network uses a Calix GigaSpire BLAST (an ISP-provided fiber gateway), which has ARP spoofing protection baked in on some models. the catch: this router doesn't expose that setting anywhere I could reach it, not through the CommandIQ app, not through a normal admin panel. I couldn't disable it ahead of time, so I just ran the attack and let the result speak for itself. if your router blocks the attack outright, that's not a failure, that's the router doing its job, and it's worth documenting either way.

**VM networking mode**
UTM defaults new VMs to Shared Network (NAT) mode, which puts the VM behind an extra layer and prevents it from seeing real traffic on the home LAN. ARP spoofing needs the attacker and victim on the same physical Layer 2 segment, so the VM has to be switched to Bridged (Advanced) mode first, or none of this works.

**pip and --break-system-packages**
newer pip versions require `--break-system-packages` to install system-wide on Ubuntu 22.04. this VM's pip (22.0.2) doesn't recognize that flag at all, so I used `sudo pip3 install <package>` instead. works fine on a dedicated lab VM, not a practice I'd recommend on a real production system.

**CORS blocking the dashboard**
the first version of the dashboard couldn't connect to the Flask server, it kept saying "connection lost" even though the server logs showed it was responding fine. this turned out to be the browser blocking cross-origin requests, since the dashboard was opened as a local file (`file://`) rather than served from a real domain. fixed by adding `flask-cors` to the server and enabling `CORS(app)`.

**terminal mixups**
running three scripts across three terminal windows at once got confusing more than once, at one point a command got typed into a terminal that was already running a different script and just sat there queued up doing nothing. worth double-checking which window is idle before typing a new command if you're juggling multiple terminals like this.

## tools and technologies

- UTM (Ubuntu 22.04 ARM64 VM on macOS, used since UTRGV's official platform, Azure, wasn't accessible from this machine)
- Python 3.10, Scapy 2.7.0
- Flask + flask-cors
- tcpdump
- a real Apple TV as the target device

## citations

- Kurose, J.F. & Ross, K.W. *Computer Networking: A Top-Down Approach* (9th ed.), 2026. Section 6.4, Switched Local Area Networks (Addressing, ARP, Ethernet, VLANs). Section 6.1, Introduction to the Link Layer.
- Scapy documentation, used for ARP packet crafting and sniffing: https://scapy.readthedocs.io
