import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt

WINDOW_SIZE = 500
LABEL_HEIGHT = 40

class SysInfoWindow(QMainWindow):
    """System Information Window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Information")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createInfoDisplay()

    def _createInfoDisplay(self):
        self.display = QWidget()
        self.display.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.display.setStyleSheet("background-color: black;")
        self.generalLayout.addWidget(self.display)

        infoLayout = QVBoxLayout(self.display)

        # Define labels for displaying the info
        self.infoLabels = {
            "Computer name": QLabel("Computer name: ..."),
            "IP Address": QLabel("IP Address: ..."),
            "Protocol": QLabel("Protocol: ..."),
            "Websites Visited": QLabel("Websites Visited: ..."),
            "SFTP": QLabel("SFTP: ..."),
        }

        # Update label style and add to layout
        for label in self.infoLabels.values():
            label.setStyleSheet("QLabel { color : white; }")
            label.setFixedHeight(LABEL_HEIGHT)
            infoLayout.addWidget(label)

        # This is where you would connect to the backend to update the labels
        self.updateInfo()

    def updateInfo(self):
        """Update the information labels with data from the backend."""
        self.infoLabels["Computer name"].setText(f"Computer name: {self.getComputerName()}")
        self.infoLabels["IP Address"].setText(f"IP Address: {self.getIPAddress()}")
        # ... update other labels similarly ...

    def getComputerName(self):
        # Placeholder for actual backend function to get the computer name
        return "Placeholder-ComputerName"

    def getIPAddress(self):
        # Placeholder for actual backend function to get the IP Address
        return "Placeholder-IPAddress"

    # ... define other backend function placeholders ...

def main():
    """Main function."""
    app = QApplication([])
    sysInfoWindow = SysInfoWindow()
    sysInfoWindow.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
