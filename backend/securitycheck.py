from scapy.all import *
from scapy.layers.inet import IP  # Add this line to import the IP class
import math

def calculate_entropy(data):
    if not data:
        return 0

    prob = [float(data.count(c)) / len(data) for c in set(data)]
    entropy = - sum(p * math.log(p) / math.log(2.0) for p in prob)
    return entropy

def analyze_packet(packet):
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        payload = packet[IP].payload

        if hasattr(payload, "load"):
            data = payload.load

            # Adjust the condition as needed for your specific case
            if calculate_entropy(data) < 4.0:
                print(f"Low entropy detected in packet from {ip_src} to {ip_dst} which is {calculate_entropy(data)}")

def analyze_pcap(file_path):
    packets = rdpcap(file_path)
    for packet in packets:
        analyze_packet(packet)

if __name__ == "__main__":
    pcap_file = "Project-NetProbeX/links.pcapng"
    analyze_pcap(pcap_file)
