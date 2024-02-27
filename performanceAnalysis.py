//this is not updated
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QProgressBar, QLabel, QListWidgetItem
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import Qt
from constants import wireshark_file_path
from securitycheck import get_packets_and_entropy

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

        # Create right side layout
        right_layout = QVBoxLayout()

        # Create progress bar for showing entropy levels
        self.progress_label = QLabel("Entropy Level:", self)
        right_layout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(-2, 4)  # Set the range from 0 to 4
        right_layout.addWidget(self.progress_bar)

       # Add labels above the progress bar to simulate ticks
        ticks_layout = QHBoxLayout()

        # Calculate the tick positions dynamically based on the current range of the progress bar
        range_min, range_max = self.progress_bar.minimum(), self.progress_bar.maximum()
        for tick_value in range(range_min, range_max + 1):
            tick_label = QLabel(str(tick_value), self)
            tick_label.setAlignment(Qt.AlignTop)

            # Calculate the position of the tick label relative to the progress bar width
            tick_position = int((tick_value - range_min) / (range_max - range_min) * self.progress_bar.width())
            tick_label.move(tick_position - tick_label.width() // 2, 0)
            ticks_layout.addWidget(tick_label)

        right_layout.addLayout(ticks_layout)

        self.entropy_value_label = QLabel("", self)
        right_layout.addWidget(self.entropy_value_label)

        # Create label for displaying details of the packet
        self.details_label = QLabel(self)
        right_layout.addWidget(self.details_label)

        # Set right layout in the main layout
        main_layout.addLayout(right_layout, 1)  # Takes up the other half of the window

        # Set the main layout for the window
        self.setLayout(main_layout)

        # Connect the itemClicked signal of the packet_list_widget to the showDetails method
        self.packet_list_widget.itemClicked.connect(self.showDetails)

        self.setWindowTitle('Filter and Analysis')
        self.setGeometry(100, 100, 800, 400)
        self.show()

    def updateUI(self):
        # Call the backend method to get packets and entropy
        self.packets, self.entropy_levels = get_packets_and_entropy(wireshark_file_path)

        # Update the packet list in the UI
        self.updatePacketList(self.packets)

        # For demonstration purposes, use the first entropy level to update the progress bar
        if self.entropy_levels:
            self.updateProgressBar(self.entropy_levels[0])

    def updatePacketList(self, packet_data):
        # Clear existing items in the list
        self.packet_list_widget.clear()

        # Add new items to the list based on packet_data
        for packet in packet_data:
            item = QListWidgetItem(packet, self.packet_list_widget)

    def updateProgressBar(self, entropy_level):
        # Update the progress bar with the given entropy level
        self.progress_bar.setValue(int(entropy_level))

        # Update the entropy value label
        self.entropy_value_label.setText(f"Entropy: {entropy_level}")

        print(f'Entropy Level: {entropy_level}')

    def showDetails(self, item):
        # Update the details_label with details of the selected packet
        self.details_label.setText(f"Details of {item.text()}")

        # Get the index of the selected item
        selected_index = self.packet_list_widget.row(item)

        # Update the progress bar with the entropy level of the selected packet
        if selected_index < len(self.entropy_levels):
            entropy_level = self.entropy_levels[selected_index]
            self.updateProgressBar(entropy_level)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FilterAnalysisWindow()
    sys.exit(app.exec_())