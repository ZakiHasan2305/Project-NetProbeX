import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QProgressBar, QLabel, QListWidgetItem
from PyQt5.QtCore import Qt, QSize
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from scapy.all import rdpcap
from constants import wireshark_file_path
from securitycheck import get_packets_and_entropy

class TransferSpeedGraph(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def updateGraph(self):
        self.ax.clear()
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

        if transfer_speeds:
            self.ax.plot(times, transfer_speeds)
            self.ax.set_xlabel('Time (s)')
            self.ax.set_ylabel('Transfer Speed (bytes/s)')
            self.ax.set_title('Transfer Speed Over Time')
            self.canvas.draw()

class FilterAnalysisWindow(QWidget):
    def __init__(self):
        super(FilterAnalysisWindow, self).__init__()

        self.initUI()

        # Call the method to get initial packet data and entropy
        self.updateUI()

    def initUI(self):
        # Create main layout
        main_layout = QHBoxLayout(self)

        # Create list widget for displaying packets with low entropy
        self.packet_list_label = QLabel("Low Entropy Packets", self)
        main_layout.addWidget(self.packet_list_label)

        # Create list widget for displaying packets with low entropy
        self.packet_list_widget = QListWidget(self)
        main_layout.addWidget(self.packet_list_widget, 1)  # Takes up half of the window

        # Add transfer speed graph
        self.transfer_speed_graph = TransferSpeedGraph(self)
        main_layout.addWidget(self.transfer_speed_graph, 1)  # Takes up the other half of the window

        # Set the main layout for the window
        self.setLayout(main_layout)

        self.setWindowTitle('Filter and Analysis')
        self.setGeometry(100, 100, 800, 400)
        self.show()

    def updateUI(self):
        # Call the backend method to get packets and entropy
        self.packets, self.entropy_levels = get_packets_and_entropy(wireshark_file_path)

        # Update the packet list in the UI
        self.updatePacketList(self.packets)

        # Update the transfer speed graph
        self.transfer_speed_graph.updateGraph()

    def updatePacketList(self, packet_data):
        # Clear existing items in the list
        self.packet_list_widget.clear()

        # Add new items to the list based on packet_data
        for packet in packet_data:
            item = QListWidgetItem(packet, self.packet_list_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FilterAnalysisWindow()
    sys.exit(app.exec_())
