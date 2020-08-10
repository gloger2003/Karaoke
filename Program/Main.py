import os
import sys

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

import SignWidget


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Karaoke")

        self.setFixedSize(480, 620)

        desktop  = QDesktopWidget()
        self.geo = QPoint(int(desktop.width() / 2 - 1280 / 2), int(desktop.height() / 2 - 720 / 2))


        self.central_widget = QWidget(self)

        self.main_menu = SignWidget.SignWidget(self.central_widget, app)
        self.main_menu.sign_admin_button.clicked.connect(lambda: (self.setFixedSize(1280, 720), self.move(self.geo)))
        self.main_menu.sign_user_button.clicked.connect(lambda: (self.setFixedSize(1280, 720), self.move(self.geo)))
        
        self.setCentralWidget(self.central_widget)

        self.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())