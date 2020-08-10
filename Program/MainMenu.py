import os
import sys

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

import LeftMenu

class MainMenu(QWidget):
    def __init__(self, parent, app, is_admin=False):
        super().__init__(parent)
        
        self.resize(640, 480)

        self.frame = QFrame(self)
        self.frame.setStyleSheet('background-color: rgb(30, 30, 30)')


        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 0, 0))

        self.left_menu = LeftMenu.LeftMenu(self.frame, app, is_admin)

        self.vbox_layout = QVBoxLayout(parent)
        self.vbox_layout.setContentsMargins(0, 0, 0, 0)

        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.setContentsMargins(0, 0, 0, 0)
        self.vbox_layout.addLayout(self.hbox_layout)

        self.vbox_layout.addWidget(self.frame)
        # self.vbox_layout.addWidget(self.left_menu)

        # self.setLayout(self.vbox_layout)
        parent.setLayout(self.vbox_layout)





