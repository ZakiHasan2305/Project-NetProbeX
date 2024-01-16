import pyshark


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
pcap_file = "data.pcapng"

ip_addresses = extract_ip_addresses(pcap_file)
print("Extracted IP Addresses:", ip_addresses)




