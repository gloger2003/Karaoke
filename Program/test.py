import os
import sys

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *



class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Karaoke") 

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Create new action
        self.openAction = QAction(QIcon('open.png'), '&Open', self)        
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.setStatusTip('Open movie')
        self.openAction.triggered.connect(self.openFile)

        # Create exit action
        self.exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        self.menuBar = self.menuBar()
        self.fileMenu = self.menuBar.addMenu('&File')
        #self.fileMenu.addAction(newAction)
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.exitAction)

        # Create a widget for window contents
        self.wid = QWidget(self)
        self.setCentralWidget(self.wid)

        # Create layouts to place inside widget
        self.controlLayout = QHBoxLayout()
        self.controlLayout.setContentsMargins(0, 0, 0, 0)
        self.controlLayout.addWidget(self.playButton)
        self.controlLayout.addWidget(self.positionSlider)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.videoWidget)
        self.layout.addLayout(self.controlLayout)
        self.layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        self.wid.setLayout(self.layout)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        self.mediaPlayer.setVolume(0)

        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile('D:/Видео/2020.08.05-16.15.mp4')))
        self.playButton.setEnabled(True)
        self.play()

        self.text_widget = TextWidget(self)
        self.setMinimumSize(self.text_widget.width(), self.text_widget.height())

        self.resize(640, 480)
        self.show()

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

    def resizeEvent(self, e):
        super().resizeEvent(e)
        try:
            self.text_widget.move(
                int(self.width() / 2 - self.text_widget.width() / 2),
                int(self.height() - self.text_widget.height()))
        except Exception as ex: print(ex)



class TextWidget(QLabel):
    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet('background-color: rgba(0, 0, 0, 100)')
        self.resize(400, 100)

        # self.label_text = QLabel(self)
        # self.

        # self.label_blur = QLabel(self)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())