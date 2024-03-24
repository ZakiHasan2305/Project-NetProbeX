import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow
import pyshark
import matplotlib.pyplot as plt
from constants import get_wireshark_file_path
wireshark_file_path = get_wireshark_file_path()

class MainWindow(QMainWindow): 
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NetProbeX")
        button = QPushButton("Analyze Packets")
        button.clicked.connect(self.analyze_packets)

        # sets size of the window 
        self.setFixedSize(QSize(800,300))

        # sets position of button on screen (centres widget)
        self.setCentralWidget(button)
    
    # function to analyze packets
    def analyze_packets(self):
        # Load Wireshark capture file
        cap = pyshark.FileCapture(wireshark_file_path)

        # Initialize variables to track packet loss
        previous_packet_number = 0
        packet_loss_data = []

        # Iterate through the packets
        for packet in cap:
            packet_number = int(packet.number)
            if packet_number != previous_packet_number + 1:
                packet_loss_data.append((float(packet.sniff_time), packet_number - previous_packet_number - 1))
            previous_packet_number = packet_number

        cap.close()

        # Plot packet loss
        if packet_loss_data:
            times, losses = zip(*packet_loss_data)
            plt.plot(times, losses)
            plt.xlabel('Time (s)')
            plt.ylabel('Packets Lost')
            plt.title('Packet Loss Over Time')
            plt.show()
        else:
            print("No packet loss detected.")

app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # Windows are hidden by default.
sys.exit(app.exec())