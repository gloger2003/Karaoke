import os
import sys

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

import RightWidget

class MediaWidget(RightWidget.RightWidget):
    def __init__(self, parent, left_menu):
        super().__init__(parent, left_menu)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.scroll  = QScrollArea(self)
        self.content = QWidget(self.scroll)

        self.vbox = QGridLayout()
        self.vbox.setSpacing(30)


        
        names = [a for a in range(50)]
        positions = [(i,j) for i in range(int(len(names) / 4) + 1) for j in range(4)]
        for position, name in zip(positions, names):
            if name == '':
                continue
            button = MediaButton(self.content)
            self.vbox.addWidget(button, *position)



        self.content.setLayout(self.vbox)
        self.content.setStyleSheet('color: white')
        self.content.resize(self.content.width(), int(len(names) / 4 * 320))
        self.content.setContentsMargins(0, 30, 0, 30)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setGeometry(0, 0, self.width(), self.height())
        self.scroll.setStyleSheet('background-color: rgba(0, 0, 0, 0); border: 0px solid')
        self.scroll.setWidget(self.content)
        self.scroll.show()



class MediaButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)

        self.setFixedSize(200, 300)
        self.setStyleSheet('background-color: rgb(60, 60, 60)')

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QColor(10, 10, 10))
        self.shadow.setOffset(0, 0)
        
        self.setGraphicsEffect(self.shadow)
    
        self.anim_shadow = QVariantAnimation()
        self.anim_shadow.setStartValue(0)
        self.anim_shadow.setEndValue(10)
        self.anim_shadow.setDuration(100)
        self.anim_shadow.valueChanged.connect(self.shadow_button_restyle)

        self.anim_borders = QVariantAnimation()
        self.anim_borders.setStartValue(0)
        self.anim_borders.setEndValue(255)
        self.anim_borders.setDuration(100)
        self.anim_borders.valueChanged.connect(self.hover_button_restyle)



    def enterEvent(self, a0):
        self.anim_borders.setDirection(self.anim_borders.Forward)
        self.anim_borders.start()
        self.anim_shadow.setDirection(self.anim_shadow.Forward)
        self.anim_shadow.start()
        return super().enterEvent(a0)

    def leaveEvent(self, a0):
        self.anim_borders.setDirection(self.anim_borders.Backward)
        self.anim_borders.start()
        self.anim_shadow.setDirection(self.anim_shadow.Backward)
        self.anim_shadow.start()
        return super().leaveEvent(a0)

    def shadow_button_restyle(self, level):
        self.shadow.setOffset(level, level)

    def hover_button_restyle(self, level):
        self.setStyleSheet(
            f'''
            background-color: rgb(60, 60, 60);
            color           : white;
            border          : 1px solid rgba(255, 130, 0, {level});;
            '''
        )