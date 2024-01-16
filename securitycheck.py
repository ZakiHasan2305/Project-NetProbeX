import pyshark
from math import log2
from collections import Counter

def calculate_entropy(data):
    if not data:
        return 0
    data_size = len(data)
    probabilities = [count / data_size for count in Counter(data).values()]
    entropy = -sum(p * log2(p) for p in probabilities)
    return entropy

def analyze_pcap(pcap_file):
    cap = pyshark.FileCapture(pcap_file)
    for packet in cap:
        try:
            if 'TCP' in packet and 'payload' in packet.tcp.field_names:
                payload = packet.tcp.payload.hex()  # Get payload for TCP packets
                entropy = calculate_entropy(payload)
                print(f"Packet {packet.number}: Entropy = {entropy}")
        except AttributeError:
            # Handle non-TCP packets
            pass

if __name__ == "__main__":
    pcap_file_path = "links.pcapng"
    analyze_pcap(pcap_file_path)
