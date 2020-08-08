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
import SearchWidget
from MediaWidget import MediaButton


class SearchLocale(QFrame):
    def __init__(self, parent=QWidget):
        super().__init__(parent)

        self.parent = parent
        self.parent.search_locale_button.deleteLater()
        self.parent.search_youtube_button.deleteLater()

        self.setGeometry(0, 0, self.parent.width(), self.parent.height())

        self.get_media()

        self.media_button_list = []

        self.media_frame = QFrame(self)
        self.media_frame.setGeometry(0, 100, self.width(), self.height() - 100)

        self.layout = QtWidgets.QVBoxLayout(self.media_frame)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.scroll  = QScrollArea(self.media_frame)
        self.content = QWidget(self.scroll)

        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.vbox.setSpacing(30)

        self.content.setLayout(self.vbox)
        self.content.setStyleSheet('color: white')
        self.content.setContentsMargins(0, 30, 0, 30)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setGeometry(0, 0, self.width(), self.height())
        self.scroll.setStyleSheet('background-color: rgba(0, 0, 0, 0); border: 0px solid')
        self.scroll.setWidget(self.content)

        self.search_line_locale = SearchLine.SearchLine(self)
        self.search_line_locale.textEdited.connect(self.check_media)

        self.show()


    def check_media(self, text=''):
        text = text.upper()

        for button in self.media_button_list:
            try: 
                button.deleteLater()
            except RuntimeError: pass

        if text != '':
                # self.vbox.removeWidget(button)
            for key_file in self.data:
                file = self.data[key_file]

                if ((file['Name'].upper().find(text) != -1 or file['Creator'].upper().find(text) != -1) or
                    ((file['Creator'].upper() + ' - ' + file['Name'].upper()).find(text) != -1)):
                    for k in self.file_path:
                        if k.find(key_file) == -1:
                            path = k
                            break
                        else:
                            path = ''

                    button = MediaButton(self.content, path, file)
                    self.media_button_list.append(button)
                    self.vbox.addWidget(button)



    def get_media(self):
        import json
        path       = sys.path[0] + '/Songs'
        list_dir   = os.listdir(path)
        files      = [file for file in list_dir if file.find('.mp4') != -1]
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
                        'Image'   : '',
                    }
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        self.data      = data
        self.file_path = path_files