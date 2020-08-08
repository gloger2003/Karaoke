import os
import sys

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *


class SearchLine(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.setGeometry(20, 20, self.parent.width() - 40, 50)
        self.setStyleSheet('''
            QLineEdit           {border-bottom: 1px solid rgb(100, 100, 100); color: white}
            QLineEdit:hover     {border-bottom: 1px solid rgb(255, 130, 0)}
            QLineEdit:focus     {border-bottom: 1px solid rgb(255, 130, 0)}''')
        self.setFont(QFont('oblique', 15))
        self.setPlaceholderText('Введите имя исполнителя или название песни, чтобы найти')