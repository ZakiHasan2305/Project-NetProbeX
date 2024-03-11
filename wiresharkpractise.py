import pyshark
import socket
from constants import wireshark_file_path

def get_local_ip_address():
    # Get the local IP address of the device
    return socket.gethostbyname(socket.gethostname())

def extract_ip_addresses(pcap_file):
    capture = pyshark.FileCapture(pcap_file)
    ip_addresses = set()

    for packet in capture:
        try:
            # Extract source and destination IP addresses
            src_ip = packet.ip.src
            dst_ip = packet.ip.dst
            ip_addresses.add(src_ip)
            ip_addresses.add(dst_ip)
        except AttributeError:
            # If the packet does not have IP layer, skip it
            continue

    return ip_addresses

# Replace with your Wireshark capture file path
pcap_file = wireshark_file_path

local_ip_address = get_local_ip_address()
print("Local IP Address:", local_ip_address)

ip_addresses = extract_ip_addresses(pcap_file)
# Print IP addresses, excluding the local IP address
print("Extracted IP Addresses (excluding local IP):", ip_addresses - {local_ip_address})






