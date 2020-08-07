import os
import sys

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *


class RightWidget(QFrame):
    def __init__(self, parent, left_menu=QFrame):
        super().__init__(parent)

        self.setStyleSheet('border: 0px solid white; background-color: rgba(0, 0, 0, 0)')

        self.resize(1280 - left_menu.width(), 720)
        self.move(1280 - self.width(), 0)

        # self.find_line = QLineEdit(parent)
        # self.find_line.setGeometry(self.x(), 0, self.width(), 30)
        # self.find_line.show()

        self.show()