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
    def __init__(self, parent=None, path=''):
        super().__init__(parent)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SplashScreen)

        desktop = QDesktopWidget()
        self.resize(desktop.width(), desktop.height())


        self.mediaPlayer = QMediaPlayer(self, QMediaPlayer.VideoSurface)

        self.videoWidget = QVideoWidget(self)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.positionSlider.hide()

        self.wid = QWidget(self)
        self.setCentralWidget(self.wid)

        self.controlLayout = QHBoxLayout()
        self.controlLayout.setContentsMargins(0, 0, 0, 0)
        self.controlLayout.addWidget(self.positionSlider)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.videoWidget)
        self.layout.addLayout(self.controlLayout)

        self.wid.setLayout(self.layout)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
        self.mediaPlayer.play()

        self.setMinimumSize(parent.width(), parent.height())

        self.show()

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)

    def closeEvent(self, a0):
        self.deleteLater()
        self.close()
        return super().closeEvent(a0)

    def keyPressEvent(self, a0):
        if a0.key() == QtCore.Qt.Key_Escape:
            self.close()
        return super().keyPressEvent(a0)


    def mousePressEvent(self, a0):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
        return super().mousePressEvent(a0)


    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        # self.playButton.setEnabled(False)
        # self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())
        print("Error: " + self.mediaPlayer.errorString())
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())