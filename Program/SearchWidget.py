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
import VideoPlayer
import SearchLine
import SearchLocale
from MediaWidget import MediaButton


class SearchWidget(RightWidget.RightWidget):
    def __init__(self, parent, left_menu=QFrame):
        super().__init__(parent, left_menu)
        
        self.vbox = QVBoxLayout(self)
        self.vbox.setAlignment(QtCore.Qt.AlignCenter)
        self.vbox.setSpacing(30)

        self.search_locale_button  = Button(self, 'Найти на компьютере', [SearchLocale.SearchLocale, (self, )])
        self.search_youtube_button = Button(self, 'Найти в YouTube')

        self.vbox.addWidget(self.search_locale_button)
        self.vbox.addWidget(self.search_youtube_button)

        self.show()



class Button(QPushButton):
    def __init__(self, parent, text, connect=None):
        super().__init__(parent)

        self.setFixedSize(int(parent.width() / 2), 200)
        self.setStyleSheet('background-color: rgb(60, 60, 60); color: white; border: 1px solid rgba(60, 60, 60, 255); border-radius: 15px')
        self.setFont(QFont('oblique', 20))
        self.setText(text)

        if connect: self.clicked.connect(lambda: connect[0](*connect[1]))

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QColor(10, 10, 10))
        self.shadow.setOffset(0, 0)
        
        self.setGraphicsEffect(self.shadow)
    
        self.anim_shadow = QVariantAnimation()
        self.anim_shadow.setStartValue(0.0)
        self.anim_shadow.setEndValue(10.0)
        self.anim_shadow.setDuration(100)
        self.anim_shadow.valueChanged.connect(self.shadow_button_restyle)

        self.anim_borders = QVariantAnimation()
        self.anim_borders.setStartValue(QRect(60, 60, 60, 255))
        self.anim_borders.setEndValue(QRect(255, 130, 0, 255))
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

    def hover_button_restyle(self, QRect=QRect):
        self.setStyleSheet(
            f'''
            background-color: rgb(60, 60, 60);
            color           : white;
            border          : 1px solid rgba({QRect.x()}, {QRect.y()}, {QRect.width()}, {QRect.height()});
            border-radius   : 15px
            '''
        )



        


if __name__ == "__main__":
    App = QApplication([])
    a = SearchWidget(None)
    App.exec_()
    pass