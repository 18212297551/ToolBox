import requests
from PyQt5.QtGui import QIconEngine

from ToolBox.main_ui import *


class Music(Ui):
    def __init__(self):
        super(Music, self).__init__()

    def __init_music_ui(self):
        """音乐播放界面"""

        self.glayout_music_home = QGridLayout()
        self.glayout_music_home.aetObject('grade_2')
        self.glayout_main.addLayout(self.glayout_music_home,2,0)

        self.glayout_music_lrc = QGridLayout()
        self.glayout_music_home.addLayout(self.glayout_music_lrc,0,0)

        self.glayout_music_info = QGridLayout()
        self.glayout_music_home.addLayout(self.glayout_music_info,0,1)








