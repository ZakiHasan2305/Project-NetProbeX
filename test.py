import subprocess
import re

def get_active_interface():
    try:
        result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True)
        output = result.stdout
        interfaces = re.findall(r"Ethernet adapter (.*?):", output)
        for interface in interfaces:
            if "Wi-Fi" in interface:
                return interface
        return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def capture_traffic(output_file, duration, interface):
    try:
        # Start tshark to capture traffic
        command = ['tshark', '-i', interface, '-w', output_file]
        tshark_process = subprocess.Popen(command)

        # Let it capture traffic for specified duration
        time.sleep(duration)

        # Stop tshark
        tshark_process.terminate()
        print("Traffic capture completed.")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    output_file = "captured_traffic.pcap"
    duration = 60  # Capture traffic for 60 seconds
    interface = get_active_interface()
    if interface:
        print(f"Active network interface found: {interface}")
        capture_traffic(output_file, duration, interface)
    else:
        print("Unable to find active network interface.")


