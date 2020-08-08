import os
import sys

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

import MediaWidget
import SearchWidget


class LeftMenu(QFrame):
    def __init__(self, parent, app=QApplication):
        super().__init__(parent)

        self.setMinimumSize(300, 720)

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(10, 10, 10))
        self.shadow.setYOffset(0.0)
        self.setGraphicsEffect(self.shadow)

        self.button_layout = QVBoxLayout()
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setAlignment(QtCore.Qt.AlignTop)
        self.button_layout.setSpacing(0)
        self.setLayout(self.button_layout)

        self.button_list = [
            LeftMenuButton(self, 'Медиатека',  [MediaWidget.MediaWidget,   (parent, self)]),
            LeftMenuButton(self, 'Поиск',      [SearchWidget.SearchWidget, (parent, self)]),
            LeftMenuButton(self, 'Настройки',  None),
            LeftMenuButton(self, 'Помощь',     None),
            LeftMenuButton(self, 'Выход',      [app.quit, ()]),
        ]

        for button in self.button_list:
            self.button_layout.addWidget(button)
        


class LeftMenuButton(QPushButton):
    def __init__(self, parent, text, connect):
        super().__init__(parent)

        self.left_menu = parent

        self.setStyleSheet(
            '''
            background-color: rgb(30, 30, 30);
            color           : white;
            border-top      : rgba(255, 130, 0, 0);
            border-bottom   : rgba(255, 130, 0, 0);
            '''
        )
        self.connect = connect
        if connect: 
            self.clicked.connect(lambda: self.run())


        self.setFixedHeight(100)
        self.setFont(QFont('oblique', 15))
        self.setText(text)

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(10, 10, 10))
        self.shadow.setYOffset(0)
        self.setGraphicsEffect(self.shadow)

        self.anim_borders = QVariantAnimation()
        self.anim_borders.setStartValue(0)
        self.anim_borders.setEndValue(255)
        self.anim_borders.setDuration(250)
        self.anim_borders.valueChanged.connect(self.hover_button_restyle)

        self.anim_font = QVariantAnimation()
        self.anim_font.setStartValue(15)
        self.anim_font.setEndValue(20)
        self.anim_font.setDuration(100)
        self.anim_font.valueChanged.connect(self.font_button_restyle)

        self.anim_shadow = QVariantAnimation()
        self.anim_shadow.setStartValue(0)
        self.anim_shadow.setEndValue(5)
        self.anim_shadow.setDuration(100)
        self.anim_shadow.valueChanged.connect(self.shadow_button_restyle)


    def enterEvent(self, a0):
        self.anim_borders.setDirection(self.anim_borders.Forward)
        self.anim_borders.start()
        self.anim_font.setDirection(self.anim_borders.Forward)
        self.anim_font.start()
        self.anim_shadow.setDirection(self.anim_borders.Forward)
        self.anim_shadow.start()
        return super().enterEvent(a0)

    def leaveEvent(self, a0):
        self.anim_borders.setDirection(self.anim_borders.Backward)
        self.anim_borders.start()
        self.anim_font.setDirection(self.anim_borders.Backward)
        self.anim_font.start()
        self.anim_shadow.setDirection(self.anim_borders.Backward)
        self.anim_shadow.start()
        return super().leaveEvent(a0)

    def hover_button_restyle(self, level):
        self.setStyleSheet(
            f'''
            background-color: rgb(30, 30, 30);
            color           : white;
            border-top      : 1px solid rgba(255, 130, 0, {level});
            border-bottom   : 1px solid rgba(255, 130, 0, {level});
            '''
        )

    def font_button_restyle(self, level):
        self.setFont(QFont('oblique', level))

    def shadow_button_restyle(self, level):
        self.shadow.setYOffset(level)

    def run(self):
        try:
            for k in self.left_menu.button_list:
                try:
                    k.wid.deleteLater()
                except: pass
            self.wid = self.connect[0](*self.connect[1])
        except Exception as e:
            self.wid = self.connect[0](*self.connect[1])