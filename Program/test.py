import json
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


from youtube_search import YoutubeSearch
results = YoutubeSearch('noixes', max_results=1).to_dict()


with open('text.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(results)

app = QApplication([])

window = QLabel()
image = QImage().fromData(requests.get(results[0]['thumbnails'][0]).content)
window.setPixmap(QPixmap().fromImage(image))
window.show()
app.exec_()
# returns a dictionary
