
import sys

# from PyQt5.QtCore import QObject, pyqtSignal

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QMainWindow



class MainWindow(QMainWindow): 
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NetProbeX")
        button = QPushButton("Press this!")
        button.setCheckable(True)
        button.clicked.connect(self.thebuttonwasclicked)
        button.clicked.connect(self.thebuttonwaschecked)

        # sets size of the window 
        self.setFixedSize(QSize(800,300))

        # sets position of button on screen (centres widget)
        self.setCentralWidget(button)
    
    # connects button to function when clicked 
    def thebuttonwasclicked(self): 
        print("Clicked!")
    def thebuttonwaschecked(self, checked):
        self.checkedButton = checked
        print(self.checkedButton)
        
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # Windows are hidden by default.
app.exec()
    