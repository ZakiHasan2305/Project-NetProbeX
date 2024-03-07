import sys
from PyQt5.QtCore import Qt, QUrl
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
        qml_file = "home.qml"
        if not QUrl.fromLocalFile(qml_file).isValid():
            print("Error: QML file not found or invalid.")
            sys.exit(1)
        self.view.setSource(QUrl.fromLocalFile(qml_file))

        self.setCentralWidget(self.container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

