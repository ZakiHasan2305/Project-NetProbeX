from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox
from PySide6.QtCore import QTimer, Qt
import pyqtgraph as pg
from random import randint
import speedtest

class Visual_Aid(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Visual Aid")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        # Create buttons
        self.speed_button = QPushButton("Speed")
        self.close_button = QPushButton("Close")

        # Add buttons to layout
        layout.addWidget(self.speed_button)
        layout.addWidget(self.close_button)

        # Create plot widget
        self.graphWidget = pg.PlotWidget()
        layout.addWidget(self.graphWidget)

        self.speedtest = speedtest.Speedtest()

        # Connect button signals
        self.speed_button.clicked.connect(self.calculate_speed)
        self.close_button.clicked.connect(self.confirm_close)

        # Set up plot
        self.x = list(range(100))  # 100 time points
        self.y = [randint(0, 100) for _ in range(100)]  # 100 data points
        self.graphWidget.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)

        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append(randint(0, 100))  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.

    def calculate_speed(self):
        download_speed = self.speedtest.download() / 1000000  # Convert to Mbps
        upload_speed = self.speedtest.upload() / 1000000  # Convert to Mbps

        QMessageBox.information(self, "Speed Test", f"Download Speed: {download_speed:.2f} Mbps\nUpload Speed: {upload_speed:.2f} Mbps")

    def confirm_close(self):
        reply = QMessageBox.question(self, 'Confirmation', 'Are you sure you want to close the application?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()


def main():
    app = QApplication([])
    main_window = Visual_Aid()
    main_window.show()
    app.exec()

if __name__ == "__main__":
    main()
