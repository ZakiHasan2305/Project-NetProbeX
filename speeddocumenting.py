import speedtest
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMessageBox, QLabel
from PySide6.QtCore import QTimer, Qt
import pyqtgraph as pg
from random import randint


class SpeedometerWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Speedometer')
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        # Create plot widget
        self.graphWidget = pg.PlotWidget()
        layout.addWidget(self.graphWidget)

        # Create labels for download and upload speed
        self.download_label = QLabel("Download Speed: ")
        layout.addWidget(self.download_label)
        self.upload_label = QLabel("Upload Speed: ")
        layout.addWidget(self.upload_label)

        self.speedtest = speedtest.Speedtest()

        # Set up plot
        self.x = []
        self.y_download = []
        self.y_upload = []
        self.graphWidget.setBackground('w')
        pen_download = pg.mkPen(color=(0, 0, 255))
        pen_upload = pg.mkPen(color=(255, 0, 0))
        self.data_line_download = self.graphWidget.plot(self.x, self.y_download, pen=pen_download, name="Download")
        self.data_line_upload = self.graphWidget.plot(self.x, self.y_upload, pen=pen_upload, name="Upload")

        self.timer = QTimer()
        self.timer.setInterval(1000)  # Update speed every second
        self.timer.timeout.connect(self.update_speed)
        self.timer.start()

    def update_speed(self):
        download_speed = self.speedtest.download() / 1000000  # Convert to Mbps
        upload_speed = self.speedtest.upload() / 1000000  # Convert to Mbps
        self.download_label.setText(f"Download Speed: {download_speed:.2f} Mbps")
        self.upload_label.setText(f"Upload Speed: {upload_speed:.2f} Mbps")

        # Add data points to plot
        self.x.append(len(self.x))
        self.y_download.append(download_speed)
        self.y_upload.append(upload_speed)
        self.data_line_download.setData(self.x, self.y_download)
        self.data_line_upload.setData(self.x, self.y_upload)


def speed(instance):
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    speedometer = SpeedometerWidget()
    speedometer.show()
    app.exec()


