import sys
import subprocess
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox, QInputDialog, QLineEdit
from PyQt5.QtGui import QPixmap

class WiresharkOpener(QWidget):
    def __init__(self):
        super().__init__()
        self.config_file = 'wireshark_config.json'  # Configuration file name
        self.loadConfig()  # Load configuration on initialization
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Wireshark Opener')
        self.setGeometry(100, 100, 600, 300)

        # Load the JPG image
        background_image = "background-overlay.jpg"
        self.pixmap = QPixmap(background_image)

        # Create a QLabel to display the background image
        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.label.setGeometry(0, 0, self.width(), self.height())

        layout = QVBoxLayout()

        label = QLabel("Please select the location of Wireshark:")
        layout.addWidget(label)

        self.path_label = QLabel(f"Path: {self.wireshark_path}")
        layout.addWidget(self.path_label)

        select_button = QPushButton("Select Wireshark")
        select_button.setStyleSheet("background-color: #007bff; color: white; border: none;")
        select_button.clicked.connect(self.selectWireshark)
        layout.addWidget(select_button)

        open_button = QPushButton("Open Wireshark")
        open_button.setStyleSheet("background-color: #28a745; color: white; border: none;")
        open_button.clicked.connect(self.openWireshark)
        layout.addWidget(open_button)

        close_button = QPushButton("Close")
        close_button.setStyleSheet("background-color: #605c5c; color: white; border: none;")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def selectWireshark(self):
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getOpenFileName(self, "Select Wireshark Executable", "", "Executable Files (*.app *.exe)" if os.name == 'nt' else "All Files (*)", options=options)
        if filepath:
            self.wireshark_path = filepath
            self.path_label.setText(f"Path: {self.wireshark_path}")
            self.saveConfig()  # Save the selected path to the configuration file


    def openWireshark(self):
        filepath = self.path_label.text().split(": ")[-1]
        if filepath and filepath != "Not Selected":
            if os.path.exists(filepath):
                try:
                    if os.name == 'nt':
                        subprocess.Popen([filepath])
                    else:  # For macOS and Linux
                        subprocess.Popen(['open', '-a', filepath])
                except Exception as e:
                    QMessageBox.critical(self, 'Error', f"Error occurred while opening Wireshark: {e}")
            else:
                QMessageBox.warning(self, 'Warning', "The selected Wireshark application does not exist.")
        else:
            QMessageBox.warning(self, 'Warning', "Please select the location of Wireshark first.")

    def saveConfig(self):
        config_data = {'wireshark_path': self.wireshark_path}
        with open(self.config_file, 'w') as file:
            json.dump(config_data, file)

    def loadConfig(self):
        try:
            with open(self.config_file, 'r') as file:
                config_data = json.load(file)
                self.wireshark_path = config_data.get('wireshark_path', 'Not Selected')
        except FileNotFoundError:
            self.wireshark_path = 'Not Selected'
    
    
    def resizeEvent(self, event):
        # Update the background size when the window is resized
        self.update_background_size()

    def update_background_size(self):
        # Resize the background image to match the window size
        self.pixmap = self.pixmap.scaled(self.size())
        self.label.setGeometry(0, 0, self.width(), self.height())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WiresharkOpener()
    window.show()
    sys.exit(app.exec_())
