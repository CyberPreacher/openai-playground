"""
create a window ui using pyqt5 where the user can drag and drop image file from the os and it will display this image on the ui window
"""


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QHBoxLayout
from PyQt5.QtGui import QPixmap, QDragEnterEvent, QDropEvent, QDragMoveEvent, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QSize, QMimeData, QEvent
from os import getcwd


class DropArea(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Drag and drop an image here!")
        self.setMinimumSize(QSize(250, 250))
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.setAutoFillBackground(True)
        self.setStyleSheet("border: 2px dashed black;")
        self.overlay = None
        self.point_list = []
        self.setMouseTracking(True)

    def dragEnterEvent(self, e: QDragEnterEvent):
        """
        override dragEnterEvent to accept image mime types
        :param e:
        :return:
        """
        if e.mimeData().hasImage():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e: QDropEvent):
        """
        override dropEvent to display the dropped image on the window
        :param e:
        :return:
        """
        if e.mimeData().hasImage():
            self.setPixmap(e.mimeData().imageData())
            self.update()
        else:
            self.setText("ERROR")

    def mousePressEvent(self, e: QDropEvent):
        """
        override mousePressEvent to add a point to the overlay on click
        :param e:
        :return:
        """
        if self.pixmap():
            self.point_list.append((e.pos().x(), e.pos().y()))
            self.update()
        else:
            pass

    def mouseMoveEvent(self, e):
        """
        override mouseMoveEvent to add a point to the overlay on mouse movement in the window
        :param e:
        :return:
        """
        if self.pixmap():
            self.point_list.append((e.pos().x(), e.pos().y()))
            self.update()
        else:
            pass

    def paintEvent(self, e):
        """
        override paintEvent to paint the image in the window with its overlay
        :param e:
        :return:
        """
        QLabel.paintEvent(self, e)
        if self.pixmap():
            painter = QPainter(self)
            painter.setPen(QPen(QColor(0, 255, 0), 5))
            for i in range(len(self.point_list) - 1):
                painter.drawLine(self.point_list[i][0], self.point_list[i][1], self.point_list[i + 1][0],
                                 self.point_list[i + 1][1])

    def clear(self):
        """
        clear the window of the pixmap and all points in the overlay
        :return:
        """
        self.clear()
        self.point_list = []


class DragDropWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = None
        self.image = None
        self.drop_area = None
        self.button = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image Annotation App")
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        self.drop_area = DropArea(self)
        self.button = QPushButton("Clear Window", self)
        self.button.clicked.connect(self.clear_window)

        self.drop_area.move(10, 10)
        self.button.move(10, 270)

        self.setGeometry(200, 200, 280, 300)
        main_layout.addWidget(self.drop_area)
        main_layout.addWidget(self.button)

    def clear_window(self):
        """
        clear the window on button click
        :return:
        """
        self.drop_area.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DragDropWindow()
    window.show()
    sys.exit(app.exec_())