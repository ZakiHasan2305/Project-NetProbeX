import pyshark


def analyze_packets(file_path):
    cap = pyshark.FileCapture(file_path)

    visited_links = set()
    total_packets = 0

    for packet in cap:
        total_packets += 1

        if "IP" in packet:
            src_ip = packet.ip.src
            dst_ip = packet.ip.dst

            if hasattr(packet, "dns") and packet.dns.qry_name:
                # DNS packet with a query name
                dns_query = packet.dns.qry_name.lower()
                visited_links.add(dns_query)

            elif hasattr(packet, "http") and packet.http.host:
                # HTTP packet with a host
                http_host = packet.http.host.lower()
                visited_links.add(http_host)

    print("Visited Links: ")
    for link in visited_links:
        print(link)

    print(f"\nTotal Packets: {total_packets}")

def protocol(file_path, max_rows = 5):
    try:
        with pyshark.FileCapture(file_path) as cap:
            for row_num, pkt in enumerate(cap):
                try:
                    layer_names = [lay.layer_name for lay in pkt.layers]
                    print(layer_names)
                except AttributeError as ex:
                    print(ex)

                if row_num >= max_rows - 1:
                    break
    except pyshark.FileCaptureException as e:
        print(f"Error opening file: {e}")



file_path = 'links.pcapng'
analyze_packets(file_path)
print("\n")
protocol(file_path,max_rows=5)