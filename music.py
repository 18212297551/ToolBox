import requests
from PyQt5.QtGui import QIconEngine

from ToolBox.main_ui import *


class Music(Ui):
    def __init__(self):
        super(Music, self).__init__()
        self.__init_music_ui()
        self.btn_home_music.clicked.connect(self.music_home_reload)


    def __init_music_ui(self):
        """音乐播放界面"""

        self.glayout_music_home = QGridLayout()
        self.glayout_music_home.setObjectName('grade_2')
        self.glayout_main.addLayout(self.glayout_music_home, 2, 0)

        self.glayout_music_lrc = QGridLayout()
        self.glayout_music_home.addLayout(self.glayout_music_lrc,0,0)

        self.glayout_music_info = QGridLayout()
        self.glayout_music_home.addLayout(self.glayout_music_info,0,1)

        self.label_music_out_lrc = MuLabel()
        self.glayout_music_lrc.addWidget(self.label_music_out_lrc,0,0,1,1)
        self.label_music_out_lrc.draw_text('你今天真好看\n以后也好看')
        self.label_music_out_lrc.setVisible(False)



    @layout_dele
    def music_home_reload(self,*args):
        """music主页重载"""
        if func_historys[3]:
            self.btn_top_forward.setVisible(True)
        else:self.btn_top_forward.setVisible(False)

        self.setVisible_by_layout(self.glayout_music_home,True)

        return self.glayout_music_home


class MuLabel(QLabel):
    def __init__(self):
        super(MuLabel, self).__init__()
        self.setWindowOpacity(0.5)
    def draw_text(self, text):
        pix = QPixmap(self.size())
        pix.fill(QColor(Qt.transparent))
        painter = QPainter(pix)
        painter.setPen(QPen(Qt.red))
        painter.drawText(100,100,text)
        self.setPixmap(pix)
        pix.save('./Temp/transpaent.jpg')
        del painter







