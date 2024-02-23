from PyQt5 import QtWidgets, uic
import sys
app = QtWidgets.QApplication([])
win = uic.loadUi("mydesign.ui") #specify the location of your .ui file
win.show()
sys.exit(app.exec())



from PyQt5 import QtWidgets, QtGui,QtCore
from mydesign import Ui_MainWindow
import sys

class netprobeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(netprobeWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.label.setFont(QtGui.QFont('SansSerif', 30))
        self.ui.label.setGeometry(QtCore.QRect(10, 10, 200, 200)) # change label geometry
app = QtWidgets.QApplication([])
application = netprobeWindow()
application.show()
sys.exit(app.exec())