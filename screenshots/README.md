# Screenshots

Documented proof for each stage of the project, in order.

## 1. Apple TV network info

Confirms the target device's real IP and MAC address, pulled directly from the Apple TV's own settings screen.

[image 1 here]

## 2. VM switched to Bridged networking

UTM's network mode changed from Shared (NAT) to Bridged (Advanced), required so the attacker VM sits on the same Layer 2 segment as the real Apple TV and router.

[image 2 here]

## 3. Reachability test

A direct Scapy ARP request confirms the VM can actually reach the real Apple TV over the network before attempting anything else.

[image 3 here]

## 4. Attack running, live tcpdump capture

The spoofing script running alongside a live tcpdump capture, showing forged ARP replies overriding the real device-to-MAC mappings in real time.

[image 4 here]

## 5. Detector catching the attack live

The detection script immediately flagging the spoofed ARP replies with timestamped alerts, while the attack is actively running.

[image 5 here]

## 6. Dashboard connected, before the attack

The live browser dashboard successfully connected to the detector feed, showing a normal, "nominal" network state before any attack begins.

[image 6 here]

## 7. Dashboard reacting to the attack live

The dashboard mid-attack: status flips to "compromised," the Apple TV and router rows flip to "spoofed," and a plain-english explanation appears in the live feed.

[image 7 here]
