import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap

class WiresharkConfigUpdater(QWidget):
    def __init__(self):
        super().__init__()
        self.config_file = 'wireshark_config.json'  # Configuration file name
        self.loadConfig()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Wireshark Data File Updater')
        self.setGeometry(100, 100, 600, 300)

        # Load the JPG image
        background_image = "background-overlay.jpg"
        self.pixmap = QPixmap(background_image)

        # Create a QLabel to display the background image
        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.label.setGeometry(0, 0, self.width(), self.height())

        layout = QVBoxLayout()

        label = QLabel("Please select the location of the Wireshark .pcapng packet file:")
        layout.addWidget(label)

        self.path_label = QLabel(f"Path: {self.pcapng_path}")
        layout.addWidget(self.path_label)

        select_button = QPushButton("Select File")
        select_button.setStyleSheet("background-color: #007bff; color: white; border: none;")
        select_button.clicked.connect(self.selectPcapngFile)
        layout.addWidget(select_button)

        save_button = QPushButton("Save File Path")
        save_button.setStyleSheet("background-color: #28a745; color: white; border: none;")
        save_button.clicked.connect(self.saveToConfig)
        layout.addWidget(save_button)

        close_button = QPushButton("Close")
        close_button.setStyleSheet("background-color: #605c5c; color: white; border: none;")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def selectPcapngFile(self):
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getOpenFileName(self, "Select pcapng File", "", "pcapng Files (*.pcapng)", options=options)
        if filepath:
            self.pcapng_path = os.path.relpath(filepath)  # Get relative path
            self.path_label.setText(f"Path: {self.pcapng_path}")

    def loadConfig(self):
        try:
            with open(self.config_file, 'r') as file:
                config_data = json.load(file)
                self.pcapng_path = config_data.get('wireshark_pcapng_path', 'Not Selected')
        except FileNotFoundError:
            self.pcapng_path = 'Not Selected'

    def saveToConfig(self):
        try:
            with open(self.config_file, 'r') as file:
                config_data = json.load(file)
                config_data['wireshark_pcapng_path'] = self.pcapng_path
            with open(self.config_file, 'w') as file:
                json.dump(config_data, file)
            QMessageBox.information(self, 'Success', "Path saved to config file successfully.")
        except FileNotFoundError:
            QMessageBox.critical(self, 'Error', "Config file not found.")
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Error occurred while saving to config file: {e}")

    def resizeEvent(self, event):
        # Update the background size when the window is resized
        self.update_background_size()

    def update_background_size(self):
        # Resize the background image to match the window size
        self.pixmap = self.pixmap.scaled(self.size())
        self.label.setGeometry(0, 0, self.width(), self.height())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WiresharkConfigUpdater()
    window.show()
    sys.exit(app.exec_())
