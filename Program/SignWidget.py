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


class SignWidget(QWidget):
    def __init__(self, parent, app):
        super().__init__(parent)
        
        self.resize(480, 720)

        self.frame = QFrame(self)
        self.frame.setStyleSheet('background-color: rgb(30, 30, 30)')
        self.frame.setGeometry(0, 0, self.width(), self.height())


        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 0, 0))
        self.shadow.setOffset(0, 5)

        self.label = QLabel(self.frame)
        self.label.setGeometry(0, 0, 480, 100)
        self.label.setGraphicsEffect(self.shadow)
        self.label.setStyleSheet('''
            border-bottom: 1px solid qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, 
                stop:0 rgba(30, 30, 30, 255), 
                stop:0.494318 rgba(255, 130, 0, 255), 
                stop:1 rgba(30, 30, 30, 255));
            color: white;
        ''')
        self.label.setFont(QFont('oblique', 20))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText('Вход')


        self.shadow_2 = QGraphicsDropShadowEffect()
        self.shadow_2.setBlurRadius(15)
        self.shadow_2.setColor(QColor(0, 0, 0))
        self.shadow_2.setOffset(0, -5)

        self.label = QLabel(self.frame)
        self.label.setGeometry(0, 320, 480, 10)
        self.label.setGraphicsEffect(self.shadow_2)
        self.label.setStyleSheet('''
            border-top: 1px solid qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, 
                stop:0 rgba(30, 30, 30, 255), 
                stop:0.494318 rgba(255, 130, 0, 255), 
                stop:1 rgba(30, 30, 30, 255));
            color: white;
        ''')
        self.label.setFont(QFont('oblique', 20))
        self.label.setAlignment(Qt.AlignCenter)


        self.login_line    = SignLine(self.frame, (10, 140, 460, 50), 'Логин',  'Неверный логин',  False)
        self.password_line = SignLine(self.frame, (10, 220, 460, 50), 'Пароль', 'Неверный пароль', True)

        self.sign_admin_button = Button(self.frame, (10, 330, 460, 80),  'Войти',      [MainMenu.MainMenu, (parent, app, True)])
        self.sign_user_button  = Button(self.frame, (10, 420, 460, 80),  'Пропустить', [MainMenu.MainMenu, (parent, app, False)])
        self.quit_button       = Button(self.frame, (120, 510, 240, 80), 'Выход',      [app.quit, ()])

        self.sign_admin_button.clicked.connect(self.deleteLater)
        self.sign_user_button.clicked.connect(self.deleteLater)




class SignLine(QLineEdit):
    def __init__(self, parent, rect=(0, 0, 0, 0), place_text='', error_text='', is_password=False):
        super().__init__(parent)

        # self.parent = parent

        self.plac_text  = place_text
        self.error_text = error_text

        self.setGeometry(*rect)
        self.setStyleSheet('''
            QLineEdit           {border: 0px solid black; border-bottom: 1px solid rgb(100, 100, 100); color: white}
            QLineEdit:hover     {border-bottom: 1px solid rgb(255, 130, 0)}
            QLineEdit:focus     {border-bottom: 1px solid rgb(255, 130, 0)}''')
        self.setFont(QFont('oblique', 15))
        self.setPlaceholderText(place_text)

        if is_password: self.setEchoMode(QLineEdit.Password)




class Button(QPushButton):
    def __init__(self, parent, rect=(0, 0, 0, 0), text='', connect=None):
        super().__init__(parent)

        self.setGeometry(*rect)
        self.setStyleSheet('background-color: rgba(30, 30, 30, 255); color: white; border: 1px solid rgba(30, 30, 30, 255); border-radius: 15px')
        self.setFont(QFont('oblique', 20))
        self.setText(text)

        if connect: 
            self.clicked.connect(lambda: connect[0](*connect[1]))

        self.anim_borders = QVariantAnimation()
        self.anim_borders.setStartValue(QRect(30, 30, 30, 255))
        self.anim_borders.setEndValue(QRect(255, 130, 0, 255))
        self.anim_borders.setDuration(100)
        self.anim_borders.valueChanged.connect(self.hover_button_restyle)


    def enterEvent(self, a0):
        self.anim_borders.setDirection(self.anim_borders.Forward)
        self.anim_borders.start()
        return super().enterEvent(a0)

    def leaveEvent(self, a0):
        self.anim_borders.setDirection(self.anim_borders.Backward)
        self.anim_borders.start()
        return super().leaveEvent(a0)

    def shadow_button_restyle(self, level):
        self.shadow.setOffset(level, level)

    def hover_button_restyle(self, QRect=QRect):
        self.setStyleSheet(f'''
            background-color: rgba(30, 30, 30, 255);
            color           : white;
            border          : 1px solid rgba({QRect.x()}, {QRect.y()}, {QRect.width()}, {QRect.height()});
            border-radius   : 15px
        ''')