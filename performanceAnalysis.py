import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPainter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from scapy.all import rdpcap
import pyshark
from constants import wireshark_file_path

class BackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background_image = QPixmap("background.jpg")  # Load background image

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_image)

class PacketLossGraph(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots(figsize=(4, 3))  # Adjust size here
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.packet_loss_data = None
        self.plotPacketLoss()

    def plotPacketLoss(self):
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

        self.packet_loss_data = packet_loss_data

        # Plot packet loss
        if packet_loss_data:
            times, losses = zip(*packet_loss_data)
            self.ax.plot(times, losses)
            self.ax.set_xlabel('Time (s)')
            self.ax.set_ylabel('Packets Lost')
            self.ax.set_title('Packet Loss Over Time')
            self.canvas.draw()
        else:
            self.ax.clear()
            self.ax.text(0.5, 0.5, 'No packet loss found', horizontalalignment='center', verticalalignment='center', fontsize=12, transform=self.ax.transAxes)
            self.ax.axis('off')
            self.canvas.draw()

class TransferSpeedGraph(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots(figsize=(4, 3))  # Adjust size here
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.updateGraph()

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
        else:
            self.ax.clear()
            self.ax.text(0.5, 0.5, 'No transfer speed data available', horizontalalignment='center', verticalalignment='center', fontsize=12, transform=self.ax.transAxes)
            self.ax.axis('off')
            self.canvas.draw()

class FilterAnalysisWindow(QWidget):
    def __init__(self):
        super(FilterAnalysisWindow, self).__init__()

        self.initUI()

    def initUI(self):
        # Set background image
        self.background = BackgroundWidget(self)

        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.background)

        # Add packet loss graph
        self.packet_loss_graph = PacketLossGraph(self)
        main_layout.addWidget(self.packet_loss_graph)  # Takes up the whole window

        # Add transfer speed graph
        self.transfer_speed_graph = TransferSpeedGraph(self)
        main_layout.addWidget(self.transfer_speed_graph)  # Takes up the other half of the window

        self.setWindowTitle('Filter and Analysis')
        self.setGeometry(100, 100, 800, 400)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FilterAnalysisWindow()
    sys.exit(app.exec_())