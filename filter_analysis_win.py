import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QProgressBar, QLabel, QListWidgetItem, QSpacerItem, QSizePolicy, QFrame, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from constants import get_wireshark_file_path
wireshark_file_path = get_wireshark_file_path()
from securitycheck import get_packets_and_entropy

class FilterAnalysisWindow(QWidget):
    def __init__(self):
        super(FilterAnalysisWindow, self).__init__()

        self.initUI()

        # Call the method to get initial packet data and entropy
        self.updateUI()

    def initUI(self):
        # Create main layout
        main_layout = QVBoxLayout(self)

        # Load the JPG image
        background_image = "background-overlay.jpg"
        self.pixmap = QPixmap(background_image)

        # Create a QLabel to display the background image
        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.label.setGeometry(0, 0, self.width(), self.height())

        # Create close button
        self.close_button = QPushButton("Close", self)
        self.close_button.setStyleSheet("background-color: #605c5c; color: white; border: none;")
        self.close_button.setFixedSize(100, 50)  # Set the size of the button to be 80x40 pixels
        self.close_button.clicked.connect(self.close)
        main_layout.addWidget(self.close_button, alignment=Qt.AlignTop | Qt.AlignRight)

        # Create list widget for displaying packets with low entropy
        self.packet_list_label = QLabel("Low Entropy Packets", self)
        self.packet_list_label.setStyleSheet("font-size: 24px; color: white; font-weight: bold;")
        main_layout.addWidget(self.packet_list_label)

        # Create list widget for displaying packets with low entropy
        self.packet_list_widget = QListWidget(self)
        self.packet_list_widget.setStyleSheet("font-size: 14px; color: black; background-color: white; border: 1px solid black;")
        main_layout.addWidget(self.packet_list_widget, 1)  # Takes up the available space

        # Create right side layout
        right_layout = QVBoxLayout()

        # Create progress bar for showing entropy levels
        self.progress_label = QLabel("Entropy Level:", self)
        self.progress_label.setStyleSheet("font-size: 16px; color: white;")
        right_layout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(-2, 4)  # Set the range from 0 to 4
        right_layout.addWidget(self.progress_bar)

        # Add labels above the progress bar to simulate ticks
        ticks_layout = QHBoxLayout()

        # Create a label for "Low" on the left side (minimum value of the progress bar)
        low_tick_label = QLabel("Low", self)
        low_tick_label.setStyleSheet("font-size: 16px; color: red;")
        ticks_layout.addWidget(low_tick_label, Qt.AlignLeft)

        # Add a larger stretch to push the "High" label to the right end
        ticks_layout.addItem(QSpacerItem(10000, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Create a label for "High" on the right side (maximum value of the progress bar)
        high_tick_label = QLabel("High", self)
        high_tick_label.setStyleSheet("font-size: 16px; color: green;")
        ticks_layout.addWidget(high_tick_label, Qt.AlignRight)

        right_layout.addLayout(ticks_layout)

        self.entropy_value_label = QLabel("", self)
        right_layout.addWidget(self.entropy_value_label)

        # Create label for displaying details of the packet
        self.details_label = QLabel(self)
        right_layout.addWidget(self.details_label)

        # Set right layout in the main layout
        main_layout.addLayout(right_layout)  # No need to specify a stretch factor

        # Set the main layout for the window
        self.setLayout(main_layout)

        # Connect the itemClicked signal of the packet_list_widget to the showDetails method
        self.packet_list_widget.itemClicked.connect(self.showDetails)

        self.setWindowTitle('Filter and Analysis')
        self.setGeometry(100, 100, 1200, 600)
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
        self.entropy_value_label.setStyleSheet("font-size: 16px; color: white;")

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
    
    def resizeEvent(self, event):
        # Update the background size when the window is resized
        self.update_background_size()

    def update_background_size(self):
        # Resize the background image to match the window size
        self.pixmap = self.pixmap.scaled(self.size())
        self.label.setGeometry(0, 0, self.width(), self.height())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FilterAnalysisWindow()
    sys.exit(app.exec_())
