import os
import sys

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

import MainMenu


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Karaoke")
        self.setFixedSize(1280, 720)

        self.central_widget = QWidget(self)

        self.main_menu = MainMenu.MainMenu(self.central_widget, app)

        # self.central_widget.setLayout(self.main_menu.vbox_layout)
        self.setCentralWidget(self.central_widget)

        self.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())