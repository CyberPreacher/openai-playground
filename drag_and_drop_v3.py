"""
create a widget using pyqt5 where the user can drag and drop png or jpeg image file from the os and it will display this image on the widget
"""

import sys
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt5.QtGui import QPixmap, QDragEnterEvent, QDropEvent

class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setAcceptDrops(True)

        self.label = QLabel()

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)

        self.setLayout(vbox)

        self.setWindowTitle('drop image')
        self.setGeometry(500,500,500,500)
        self.show()

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/uri-list'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        for url in e.mimeData().urls():
            #print(url.toLocalFile())
            pixmap = QPixmap(url.toLocalFile())
            self.label.setPixmap(pixmap)
            self.label.adjustSize()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


# create a second window and apply drag and drop functionality on it to allow the user to drag and drop the image from the first window
# to the second window of the app

import sys
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QApplication
from PyQt5.QtGui import QPixmap, QDragEnterEvent, QDropEvent

class FirstWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setAcceptDrops(True)

        self.label = QLabel()

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)

        self.setLayout(vbox)

        self.setWindowTitle('first window')
        self.setGeometry(150,150,500,500)
        self.show()

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/uri-list'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        for url in e.mimeData().urls():
            pixmap = QPixmap(url.toLocalFile())
            self.label.setPixmap(pixmap)
            self.label.adjustSize()


class SecondWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setAcceptDrops(True)
        self.label = QLabel()

        hbox = QHBoxLayout()
        hbox.addWidget(self.label)

        self.setLayout(hbox)

        self.setWindowTitle('second window')
        self.setGeometry(150,150,500,500)
        self.show()

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/uri-list'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        for url in e.mimeData().urls():
            pixmap = QPixmap(url.toLocalFile())
            self.label.setPixmap(pixmap)
            self.label.adjustSize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = FirstWindow()
    ex1 = SecondWindow()
    sys.exit(app.exec_())