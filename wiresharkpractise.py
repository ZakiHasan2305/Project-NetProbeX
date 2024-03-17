import pyshark
from constants import wireshark_file_path

def get_source_ip(pcap_file):
    # Open the pcap file
    cap = pyshark.FileCapture(pcap_file)

    # Iterate over each packet in the pcap file
    for packet in cap:
        # Check if the packet has an IP layer
        if 'IP' in packet:
            # Extract and return the source IP address
            return packet.ip.src

    # If no IP address is found, return None
    return None

# Replace 'your_pcap_file.pcap' with the path to your pcap file
pcap_file = wireshark_file_path
source_ip = get_source_ip(pcap_file)

if source_ip:
    print("Source IP address:", source_ip)
else:
    print("No source IP address found in the pcap file.")
