import os
import sys

import PyQt5
import requests
from PyQt5 import QtCore, QtGui, QtMultimedia, QtMultimediaWidgets, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtWidgets import *

import RightWidget
import VideoPlayer


class MediaWidget(RightWidget.RightWidget):
    def __init__(self, parent, left_menu):
        super().__init__(parent, left_menu)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.scroll  = QScrollArea(self)
        self.content = QWidget(self.scroll)

        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.vbox.setSpacing(30)

        self.content.setLayout(self.vbox)
        self.content.setStyleSheet('color: white')
        # self.content.resize(self.content.width(), int(len(names) / 4 * 320))
        self.content.setContentsMargins(0, 30, 0, 30)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setGeometry(0, 0, self.width(), self.height())
        self.scroll.setStyleSheet('background-color: rgba(0, 0, 0, 0); border: 0px solid')
        self.scroll.setWidget(self.content)

        self.get_media()
        self.scroll.show()

    def get_media(self):
        import json

        path = sys.path[0] + '/Songs'

        list_dir = os.listdir(path)

        files = [file for file in list_dir if file.find('.mp4') != -1]

        path_files = [path + '/' + k for k in files]

        try:
            with open('descs.json', 'r', encoding='utf-8') as f:
                data = json.loads(f.read())
        except FileNotFoundError:
            with open('descs.json', 'w', encoding='utf-8') as f:
                data = {}
                for filename in files:
                    data[filename] = {
                        'Creator' : '',
                        'Name'    : '',
                        'Genre'   : '',
                        'Date'    : '',
                        'Image'   : ''
                    }
                json.dump(data, f, indent=2, ensure_ascii=False)

        for k in range(len(files)):
            button = MediaButton(self.content, path_files[k], data[files[k]])
            self.vbox.addWidget(button)





class MediaButton(QPushButton):
    def __init__(self, parent, path, data):
        super().__init__(parent)

        self.data = data
        self.path = path

        self.clicked.connect(lambda: VideoPlayer.Window(parent, path))

        self.setFixedSize(parent.width() - 40, 100)
        self.setStyleSheet('background-color: rgb(60, 60, 60); color: white; border: 1px solid rgba(60, 60, 60, 255); border-radius: 10px')
        self.setFont(QFont('oblique', 13))

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
        self.anim_borders.setStartValue(QRect(60, 60, 60, 255))
        self.anim_borders.setEndValue(QRect(255, 130, 0, 255))
        self.anim_borders.valueChanged.connect(self.hover_button_restyle)

        self.description = QLabel(self)
        self.description.setGeometry(180, 0, self.width() - 200, self.height())
        self.description.setAlignment(QtCore.Qt.AlignCenter)
        self.description.setFont(QFont('oblique', 13))
        self.description.setStyleSheet('background-color: rgba(0, 0, 0, 0); border: 0px solid black')

        self.image_label = QLabel(self)
        self.image_label.setGeometry(10, 10, 160, 80)
        self.image_label.setStyleSheet('background-color: rgba(0, 0, 0, 0); border-radius: 0px')
        self.image_label.setScaledContents(True)

        self.write_description()

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
            border-radius   : 10px
            '''
        )
    
    def write_description(self):
        try:
            desc = ''
            translate = {
                'Name'    : 'Название',
                'Creator' : 'Создатель',
                'Genre'   : 'Жанр',
                'Date'    : 'Дата выпуска',
            }

            desc = f"{self.data['Creator']} - {self.data['Name']}\n{self.data['Genre']}\n{self.data['Date']}"

            self.description.setText(desc)

            if self.data['Image'] != '':
                url = self.data['Image']

                if url.find('http') != -1:
                    image  = QImage().fromData(requests.get(url).content)
                    pixmap = QPixmap().fromImage(image)
                else:
                    pixmap = QPixmap(url)
                self.image_label.setPixmap(pixmap)
            else:
                self.image_label.hide()
                self.description.setGeometry(0, 0, self.width(), self.height())
                
        except FileNotFoundError as e:
            pass







    # app.quit()


if __name__ == "__main__":
    app = QApplication([])
    get_media().start()
    sys.exit(app.exec_())
    pass
