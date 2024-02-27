from PySide6.QtWidgets import QMessageBox, QApplication
from PySide6.QtCore import QTimer
import pyqtgraph as pg
from random import randint
import speedtest
import pyshark
import sys
from constants import wireshark_file_path

def byte(instance):
    # Path to your pcap/pcapng file
    pcap_file = wireshark_file_path

    # Open the capture file
    capture = pyshark.FileCapture(pcap_file)

    # List to store packet lengths
    packet_lengths = []

    # Iterate over the first 10 packets in the capture
    for packet in capture:
        # Access the length attribute of the packet and append to the list
        packet_lengths.append(int(packet.length))
        

    # Close the capture file
    capture.close()

    # Sort the packet lengths
    sorted_lengths = sorted(packet_lengths)

    # Calculate statistics
    total_packets = len(sorted_lengths)
    median_index = total_packets // 2
    lower_quartile_index = total_packets // 4
    upper_quartile_index = 3 * total_packets // 4

    # Statistics
    highest_packet = sorted_lengths[-1]
    lowest_packet = sorted_lengths[0]
    median_packet = sorted_lengths[median_index]
    lower_quartile_packet = sorted_lengths[lower_quartile_index]
    upper_quartile_packet = sorted_lengths[upper_quartile_index]

    # Create a bar graph
    win = pg.GraphicsLayoutWidget()
    win.setWindowTitle('Packet Length Statistics')
    plot = win.addPlot(title="Packet Length Statistics")
    plot.setLabel('left', 'Packet Length (bytes)')
    plot.setLabel('bottom', 'Statistics')

    # Create bar items
    x_labels = [0, 1, 2, 3, 4]
    y_values = [highest_packet, lowest_packet, median_packet, lower_quartile_packet, upper_quartile_packet]
    x_tick_labels = ['Highest', 'Lowest', 'Median', 'Lower Quartile', 'Upper Quartile']
    x_ticks = [(i, label) for i, label in enumerate(x_tick_labels)]
    plot.getAxis('bottom').setTicks([x_ticks, []])  # Set custom ticks for x-axis
    bar = pg.BarGraphItem(x=x_labels, height=y_values, width=0.5, brush='b')
    plot.addItem(bar)

    # Display the plot
    win.show()

    # Display statistics
    message = f"Highest Packet Length: {highest_packet} bytes\n"
    message += f"Lowest Packet Length: {lowest_packet} bytes\n"
    message += f"Median Packet Length: {median_packet} bytes\n"
    message += f"Lower Quartile Packet Length: {lower_quartile_packet} bytes\n"
    message += f"Upper Quartile Packet Length: {upper_quartile_packet} bytes\n"
    QMessageBox.information(None, "Byte Statistics", message)

def main():
    # Create the QApplication instance
    app = QApplication(sys.argv)

    # Call the byte function
    byte(None)

    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
