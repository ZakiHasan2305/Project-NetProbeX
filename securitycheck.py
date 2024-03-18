from scapy.all import *
from scapy.layers.inet import IP  # Add this line to import the IP class
import math
from constants import get_wireshark_file_path
wireshark_file_path = get_wireshark_file_path()

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

def get_packets_and_entropy(file_path):
    analyzed_packets = []
    entropy_levels = []

    packets = rdpcap(file_path)
    for packet in packets:
        if IP in packet:
            payload = packet[IP].payload

            if hasattr(payload, "load"):
                data = payload.load
                entropy = calculate_entropy(data)

                # Adjust the condition as needed for your specific case
                if entropy < 3.0:
                    analyzed_packets.append(str(packet))
                    entropy_levels.append(entropy)

    return analyzed_packets, entropy_levels

if __name__ == "__main__":
    pcap_file = wireshark_file_path
    packets, entropy_levels = get_packets_and_entropy(pcap_file)
    # analyze_pcap(pcap_file)

    # Now you can use 'packets' and 'entropy_levels' in your PyQt frontend
    print("Analyzed Packets:", packets)
    print("Entropy Levels:", entropy_levels)

