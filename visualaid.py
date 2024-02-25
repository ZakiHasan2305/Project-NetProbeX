import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PySide6.QtCore import QTimer, Qt
import pyqtgraph as pg
from random import randint
import speedtest
import pyshark

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from bytes import byte  # Import the byte function from bytes.py

height = 500

def confirm_close(instance):
    content = BoxLayout(orientation='vertical')
    content.add_widget(Label(text='Are you sure you want to close the application?'))

    # Create "Yes" button to close the app
    yes_button = Button(text='Yes', size_hint=(1, None), height=40)
    yes_button.bind(on_press=close_app)
    content.add_widget(yes_button)

    # Create "No" button to cancel
    no_button = Button(text='No', size_hint=(1, None), height=40)
    content.add_widget(no_button)

    # Create Popup
    popup = Popup(title='Confirmation', content=content, size_hint=(None, None), size=(300, 200))
    popup.open()

    # Bind "No" button to dismiss the popup
    no_button.bind(on_press=popup.dismiss)

def close_app(instance):
    App.get_running_app().stop()

class BackgroundApp(App):

    def build(self):
        root = FloatLayout()  # Switch this to whatever png we need
        bg_image = Image(source='Project-NetProbeX/redandblack.jpg', allow_stretch=True, keep_ratio=False)
        close_button = Button(text='Close', size_hint=(0.2, 0.1), pos_hint={'right': 1, 'top': 1})
        close_button.bind(on_press=confirm_close)
        byte_button = Button(text='Byte',size_hint= (0.2,0.1), pos_hint = {'left' : 1, 'top': 1})
        byte_button.bind(on_press=byte)  # Bind the byte function to the byte button press event

        # Add the Image and Button widgets to the root widget
        root.add_widget(bg_image)
        root.add_widget(close_button)
        root.add_widget(byte_button)
        return root    

    

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

    BackgroundApp().run()
    app = QApplication(sys.argv)
    
    main_window = Visual_Aid()
    main_window.show()
    sys.exit(app.exec())
   

if __name__ == "__main__":
    
    main()
