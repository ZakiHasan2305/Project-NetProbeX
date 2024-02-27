import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtQuick import QQuickView
from PyQt5.QtGui import QGuiApplication

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 1280, 720)
        self.setWindowTitle("Test Application")

        self.view = QQuickView()
        self.container = QWidget.createWindowContainer(self.view, self)
        self.container.setGeometry(0, 0, 1280, 720)
        self.container.setFocusPolicy(Qt.StrongFocus)

        self.view.setResizeMode(QQuickView.SizeRootObjectToView)
        self.view.setSource(QUrl.fromLocalFile("screen01.qml"))

        self.setCentralWidget(self.container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
