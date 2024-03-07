import sys
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from scapy.all import rdpcap
import matplotlib.pyplot as plt
from constants import wireshark_file_path

class MainWindow(QMainWindow): 
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NetProbeX")
        button = QPushButton("Analyze Packets")
        button.clicked.connect(self.analyze_packets)

        self.setFixedSize(QSize(800,300))
        self.setCentralWidget(button)
    
    def analyze_packets(self):
        packets = rdpcap(wireshark_file_path)

        times = []
        transfer_speeds = []

        previous_time = packets[0].time
        previous_size = len(packets[0])

        for packet in packets[1:]:
            time = packet.time
            size = len(packet)
            
            time_difference = time - previous_time
            size_difference = size - previous_size
            
            if time_difference > 0:
                transfer_speed = size_difference / time_difference
                times.append(time)
                transfer_speeds.append(transfer_speed)
            
            previous_time = time
            previous_size = size

        print("Number of packets captured:", len(times))
        print("Transfer speeds:", transfer_speeds)

        if transfer_speeds:
            plt.plot(times, transfer_speeds)
            plt.xlabel('Time (s)')
            plt.ylabel('Transfer Speed (bytes/s)')
            plt.title('Transfer Speed Over Time')
            plt.show()
        else:
            print("No transfer speed data available.")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())