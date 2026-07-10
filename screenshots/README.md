# Screenshots

Documented proof for each stage of the project, in order.

## 1. Apple TV network info

Confirms the target device's real IP and MAC address, pulled directly from the Apple TV's own settings screen.

<img width="1920" height="1080" alt="01_apple_tv_network_info" src="https://github.com/user-attachments/assets/a777d428-f8a8-47f0-a277-fbf0b84dbeba" />

## 2. VM switched to Bridged networking

UTM's network mode changed from Shared (NAT) to Bridged (Advanced), required so the attacker VM sits on the same Layer 2 segment as the real Apple TV and router.

<img width="1920" height="1080" alt="02_vm_bridged_mode" src="https://github.com/user-attachments/assets/3c4cdefd-745c-403a-a010-e7c2fb27fd13" />

## 3. Reachability test

A direct Scapy ARP request confirms the VM can actually reach the real Apple TV over the network before attempting anything else.

<img width="1920" height="1080" alt="03_scapy_arp_test" src="https://github.com/user-attachments/assets/90fcc234-0b98-46fe-aae0-a1d72b00f817" />

## 4. Attack running, live tcpdump capture

The spoofing script running alongside a live tcpdump capture, showing forged ARP replies overriding the real device-to-MAC mappings in real time.

<img width="1920" height="1080" alt="04_attack_live_tcpdump" src="https://github.com/user-attachments/assets/4748656d-8c5a-4c2b-b814-c61ff1423ec4" />

## 5. Detector catching the attack live

The detection script immediately flagging the spoofed ARP replies with timestamped alerts, while the attack is actively running.

<img width="1920" height="1080" alt="05_detector_catching_attack" src="https://github.com/user-attachments/assets/a5528eb6-b880-4789-a264-4a0ecaa565ce" />

## 6. Dashboard connected, before the attack

The live browser dashboard successfully connected to the detector feed, showing a normal, "nominal" network state before any attack begins.

<img width="1920" height="1080" alt="06_dashboard_connected" src="https://github.com/user-attachments/assets/e41a2cd0-abd6-4607-b873-2cf5f4d9f6ec" />

## 7. Dashboard reacting to the attack live

The dashboard mid-attack: status flips to "compromised," the Apple TV and router rows flip to "spoofed," and a plain-english explanation appears in the live feed.
<img width="1920" height="1080" alt="07_pre_dashboard_compromised" src="https://github.com/user-attachments/assets/083d35ee-8c95-4132-9373-b86251a18b2b" />

<img width="1920" height="1080" alt="07_dashboard_compromised" src="https://github.com/user-attachments/assets/355f19dd-50e7-407c-9b53-f5f89ea70444" />
