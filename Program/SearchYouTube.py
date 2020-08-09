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
from youtube_search import YoutubeSearch


class SearchYouTube(QFrame):
    def __init__(self, parent=QWidget):
        super().__init__(parent)

        self.parent = parent
        self.parent.search_locale_button.deleteLater()
        self.parent.search_youtube_button.deleteLater()

        self.setGeometry(0, 0, self.parent.width(), self.parent.height())

        self.media_button_list = []

        self.media_frame = QFrame(self)
        self.media_frame.setGeometry(0, 90, self.width(), self.height() - 90)

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
        self.scroll.setGeometry(0, 0, self.media_frame.width(), self.media_frame.height())
        self.scroll.setStyleSheet('background-color: rgba(0, 0, 0, 0); border: 0px solid')
        self.scroll.setWidget(self.content)

        self.search_line_youtube = SearchLine.SearchLine(self)

        self.thread = CheckMedia(self, self.media_button_list, self.search_line_youtube.text())
        self.thread.finished.connect(self.add_buttons)

        self.search_line_youtube.returnPressed.connect(self.thread.start)

        self.show()


    def add_buttons(self):
        buttons = []
        if len(self.media_button_list) > 0:
            for k in self.media_button_list:
                button = MediaButton(self.content, *k)
                buttons.append(button)
                self.vbox.addWidget(button)
            self.media_button_list = button


class CheckMedia(QThread):
    def __init__(self, parent, media_button_list, text):
        super().__init__(parent)
        self.text              = text
        self.parent            = parent
        self.media_button_list = media_button_list

    def run(self):
        for button in self.media_button_list:
            try: 
                button.deleteLater()
            except (RuntimeError, AttributeError): pass
        
        self.media_button_list = []

        results = YoutubeSearch(self.text + ' Калинка Караоке', max_results=10).to_dict()
        for video in results:
            if video['channel'] == 'Калинка Караоке':
                data = {
                    'Creator' : '',
                    'Name'    : video['title'] if len(video['title']) < 50 else video['title'][0:47] + '...',
                    'Genre'   : '',
                    'Date'    : '',
                    'Image'   : video['thumbnails'][0]
                }
                url = 'https://www.youtube.com' + video['url_suffix']

                # button = MediaButton(self.content, url, data)
                self.media_button_list.append((url, data))
                # self.vbox.addWidget(button)