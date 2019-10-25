"""
@author 微&风
@data   2019.10.20

实现：
    调用百度API，实现所有功能，并且可以通过微信进行调用

思路：
    窗体使用PYQT5进行设计，
    1、暂不考虑无边框
    2、功能分类，多TAB还是单TAB?
    3、先实现窗体调用，再考虑微信调用
    4、使用百度API提供的包
    5、考虑设计用户登录？密码保护？数据加密？


"""
import os
import re
import random
import sys
import time
import threading
import traceback
from pydub.utils import mediainfo
import requests
import json
import base64
from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import urlencode
from urllib.parse import quote_plus
from PIL import Image,ImageDraw
import pyautogui
import cv2
from multiprocessing import Process,Queue
from ToolBox.baidu_aip import AipSpeech, AipFace, AipBodyAnalysis
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QTimer, QPoint, QSize, QThread, pyqtSignal, QUrl, QFileSelector,QFile
from PyQt5.QtGui import QIcon, QPalette, QBrush, QPixmap, QPainter, QFont, QTransform

from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QProgressBar, QPushButton, QMenuBar, QAction, qApp, \
    QMenu, QTextEdit, QLabel, QColorDialog, QToolButton, QLineEdit, QListWidget, QComboBox, QSlider,QSpinBox,\
    QMessageBox,QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist

# =========================================全局变量==============================================
ROOTDIR = os.getcwd() # 当前根目录
func_historys = [None,None,None,None,None,None] # 之前访问的各级窗口初始化函数，用于实现back and forward
func_before = None #上次刷新窗口调用的函数
before_layout = None # 当前窗口所在布局

APPID = '17376947'
APIKEY = 'K7G0KLcoQnTLH4QjmCZMigyM'
SECRETKEY = 'xqdTGx6mMB6pu3WtD9c0r8yX9Sxy0OiL'

my_dirs = ['Record/Voice/Temp','Record/Img/Crop','Record/Img/Merge','Record/Img/Draw','Record/Img/BodySeg']

for i in my_dirs:
    i = os.path.abspath(i)
    if not os.path.exists(i): os.makedirs(i)


def catch_except(func):
    def wrapper(*args,**kwargs):
        try:

            return func(*args,**kwargs)
        except:
            with open('./log.txt', 'a+') as _f:
                _error = traceback.format_exc()
                _t = '[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ']'
                content = "\n{}\n{}\n".format(_t,_error)
                _f.write(content)
                print(_error)
                args[0].pbar_bottom.reset()
                QMessageBox.warning(args[0], '出错了...', str(_error))





    return wrapper

def layout_dele2(func):
    """
    删除上一个布局的控件，以显示当前布局控件
    :param func:
    :return:
    """
    @catch_except
    def inner(*args):
        global before_layout, func_historys,func_before

        if before_layout:
            for i in range(before_layout.count()):
                before_layout.itemAt(i).widget().deleteLater()

        before_layout = func(*args)
        func_before = func


        if before_layout.objectName() == 'grade_1':
            func_historys[1] = func
        elif before_layout.objectName() == 'grade_2':
            func_historys[2] = func
        elif before_layout.objectName() == 'grade_3':
            func_historys[3] = func
        elif before_layout.objectName() == 'grade_4':
            func_historys[4] = func
        elif before_layout.objectName() == 'grade_5':
            func_historys[5] = func




    return inner

def layout_dele(func):
    """
    删除上一个布局的控件，以显示当前布局控件
    :param func:
    :return:
    """
    @catch_except
    def inner(*args):
        global before_layout, func_historys,func_before
        @catch_except
        def delete(layouts):
            if layouts:
                for i in range(layouts.count()):
                    t = layouts.itemAt(i).__doc__
                    # 防止layout中还有layout
                    if t == 'QGridLayout(QWidget)\nQGridLayout()':
                        delete(layouts.itemAt(i))
                    elif not layouts.itemAt(i).widget() is None:
                        layouts.itemAt(i).widget().setVisible(False)

        delete(before_layout)
        func_before = func
        before_layout = func(*args)

        # print(before_layout.objectName(),func_before)
        if before_layout.objectName() == 'grade_1':
            func_historys[1] = func
        elif before_layout.objectName() == 'grade_2':
            func_historys[2] = func
        elif before_layout.objectName() == 'grade_3':
            func_historys[3] = func
        elif before_layout.objectName() == 'grade_4':
            func_historys[4] = func
        elif before_layout.objectName() == 'grade_5':
            func_historys[5] = func

    return inner

def random_color(mode='rgb',r=None,g=None,b=None):
    """获取随机颜色"""
    mode = mode.lower()
    if mode == 'hex':
        value = list(range(10))
        value.extend(['A','B','C','D','E','F'])
        color = '#'
        for i in range(6): color += str(random.choice(value))
    elif mode == 'rgb':
        if r is None: r = random.randint(50, 200)
        if g is None: g = random.randint(50,200)
        if b is None : b = random.randint(50,200)
        color = 'rgb({},{},{})'.format(r,g,b)

    elif mode == 'background':
        r = random.randint(140, 255)
        g = random.randint(140,255)
        b = random.randint(140,255)
        color = 'rgb({},{},{})'.format(r, g, b)

    elif mode == 'font':
        r = random.randint(0, 100)
        g = random.randint(0,100)
        b = random.randint(0,100)
        color = 'rgb({},{},{})'.format(r,g,b)

    else: raise TypeError("invalid parameter {}".format(mode))

    return color



class Ui(QWidget):
    """
    窗体主模块
    """
    def __init__(self,*args):
        super(Ui, self).__init__()
        self.__init_ui__()
        self.__init_var__()
        self.__init_meau_main__()
        self.__init_status__()
        self.__init_home__()

    def __init_ui__(self,*args):
        self.resize(640,480)
        self.setWindowTitle('Toolbox')
        self.setWindowIcon(QIcon('./Ico/toolbox.png'))
        self.setMouseTracking(True)
        # self.setWindowOpacity(0.8)

        self.setStyleSheet('*{background-color: #FFFFFF}')
        # self.setWindowFlags(Qt.WindowStaysOnTopHint) # 窗口置顶
        # 总布局
        self.glayout_main = QGridLayout()
        self.glayout_main.setSpacing(0)
        self.glayout_main.setContentsMargins(0,0,0,0)
        # 为窗体添加布局
        self.setLayout(self.glayout_main)

        # C = QColorDialog().getColor()



    def time_show_out(self, *args):
        self.time_now = time.strftime('%Y-%m-%d %a %H:%M:%S', time.localtime())
        self.label_top_center.setText(self.time_now)
        # self.btn_0_openfolder.setText(self.time_now)

    def __init_var__(self,*args):
        # 时间
        self.timer_top = QTimer()
        self.timer_top.timeout.connect(self.time_show_out)
        self.timer_top.start(100)

        # 多线程执行程序
        self.Outter_Run = Outter_Run()
        self.Outter_Run.sign.connect(self.Outter_Run_sign_deal)


    def __init_meau_main__(self,*args):
        """
        主菜单栏
        :return:
        """
        # 窗口顶部主布局
        self.glayout_top = QGridLayout()
        self.glayout_main.addLayout(self.glayout_top,1,0,Qt.AlignTop)

        # 菜单栏 左侧
        self.glayout_meau = QGridLayout()
        self.glayout_top.addLayout(self.glayout_meau,0,0)
        self.meau_main = QMenuBar()
        self.meau_main.setFixedSize(100,30)
        # self.meau_main.setWindowIcon(QIcon('./Ico/bg_img.png'))
        self.glayout_meau.addWidget(self.meau_main,0,0,1,1)

        meau = QAction('设置',self.meau_main)
        meau.setText('设置')
        # meau.triggered.connect(self._test_ui)
        self.meau_main.addAction(meau)


        # 返回按钮等
        self.btn_top_back = QToolButton()
        self.btn_top_back.setIcon(QIcon('./Ico/back.png'))
        self.btn_top_back.setStyleSheet('*{width:22px;height:22px;border:0}')
        self.glayout_meau.addWidget(self.btn_top_back,0,1,1,1)
        self.btn_top_forward = QToolButton()
        self.btn_top_forward.setIcon(QIcon('./Ico/forward.png'))
        self.btn_top_forward.setStyleSheet('*{width:22px;height:22px;border:0}')
        self.glayout_meau.addWidget(self.btn_top_forward,0,2,1,1)

        self.btn_top_forward.setVisible(False)
        self.btn_top_back.setVisible(False)

        # 顶部中心
        self.glayout_top_center = QGridLayout()
        self.glayout_top.addLayout(self.glayout_top_center,0,1)


        self.label_top_center = QLabel()
        self.glayout_top_center.addWidget(self.label_top_center,0,1,1,1)
        self.label_top_center.setFixedHeight(25)
        # self.label_top_center.setMouseTracking(True)
        self.label_top_center.setAlignment(Qt.AlignCenter)


        # 顶部右侧
        self.glayout_top_right = QGridLayout()
        self.glayout_top.addLayout(self.glayout_top_right,0,2)

        self.label_top_right = QLabel()
        self.label_top_right.setObjectName('label_top_right')
        # self.label_top_right.setText('label')
        self.label_top_right.setFixedWidth(150)
        self.label_top_right.setAlignment(Qt.AlignCenter)

        # self.label_top_show.setAutoFillBackground(True)
        self.label_top_right.setMouseTracking(True)
        self.glayout_top_right.addWidget(self.label_top_right, 0, 0, 1, 1)

        self.meau_widgets = [self.meau_main,self.btn_top_back,self.btn_top_forward,self.label_top_center,self.label_top_right]
        color = (random_color(mode='background'), random_color(mode='font'), random_color(mode='background'),
                random_color(mode='font'))
        # self.meau_main.setStyleSheet("*{background-color:%s;color:%s;border:0;font:YaHei;} :pressed{background-color:%s;color:%s;}" % color)

        for widget in self.meau_widgets:
            widget.setFixedHeight(25)
            widget.setStyleSheet("*{background-color:%s;color:%s;border:0;font:YaHei;} :pressed{background-color:%s;color:%s;}" % color)

        self.btn_top_forward.clicked.connect(self.btn_top_forward_clicked)
        self.btn_top_back.clicked.connect(self.btn_top_back_clicked)











    @catch_except
    def btn_top_back_clicked(self,*args):
        """返回按钮实际实现方法"""

        # print('back',func_before,func_historys)
        if func_before:
            index = func_historys.index(func_before)
            if func_historys[index - 1]:
                layout_dele(func_historys[index - 1])(self,*args)

            if func_historys[index]:
                self.btn_top_forward.setVisible(True)
            else:
                self.btn_top_forward.setVisible(False)


    @catch_except
    def btn_top_forward_clicked(self,*args):

        # global func_historys
        # print('forward',func_before)
        if func_before:
            index = func_historys.index(func_before)
            if func_historys[index+1]:
                layout_dele(func_historys[index+1])(self)
                # func_historys[index+1](self)
        self.btn_top_back.setVisible(True)



    def leave_home_event(self,*args):
        self.btn_top_back.setVisible(True)


    def __init_status__(self,*args):
        self.glayout_status = QGridLayout()
        self.glayout_main.addLayout(self.glayout_status,3,0,Qt.AlignBottom)
        self.label_status_left = QLabel()
        # self.label_status_left.setText('这是状态栏')
        self.label_status_left.setFixedWidth(200)
        self.label_status_left.setAlignment(Qt.AlignCenter)
        self.glayout_status.addWidget(self.label_status_left,0,0,1,1)
        self.pbar_bottom = QProgressBar()
        self.pbar_bottom.setObjectName('bottom_par')
        self.pbar_bottom.setAlignment(Qt.AlignCenter)
        self.pbar_bottom.setRange(0,100)
        self.glayout_status.addWidget(self.pbar_bottom, 0, 1, 1, 1)
        self.label_status_right = QLabel()
        # self.label_status_right.setText('这是状态栏')
        self.label_status_right.setAlignment(Qt.AlignCenter)
        self.label_status_right.setFixedWidth(200)
        self.glayout_status.addWidget(self.label_status_right, 0, 2, 1, 1)

        self.status_widgets = [self.label_status_right, self.label_status_left, self.pbar_bottom]
        color = (random_color(mode='background'), random_color(mode='font'), random_color(mode='background'),
                random_color(mode='font'))
        for widget in self.status_widgets:
            widget.setStyleSheet(
                "*{background-color:%s;color:%s;border:0;height:25px;font:YaHei;} :pressed{background-color:%s;color:%s;}" %color)

    def Outter_Run_sign_deal(self,p):
        self.pbar_bottom.setValue(p)


    def __init_home__(self,*args):
        """
        主页布局
        :return:
        """


        self.glayout_home = QGridLayout()
        self.glayout_home.setObjectName('grade_1')
        self.glayout_main.addLayout(self.glayout_home,2,0,Qt.AlignCenter)
        self.glayout_home.setSpacing(int(self.width()*0.2/6))
        self.glayout_home.setContentsMargins(10,10,10,10)

        # btn及其参数
        self.home_btns = []

        self.btn_home_voice = QPushButton()
        self.home_btns.append([self.btn_home_voice,0,0,1,1,'语音技术','btn_home_voice',80,60,'./Ico/voice.png'])
        self.btn_home_face = QPushButton()
        self.home_btns.append([self.btn_home_face,0,1,1,1,'人脸识别','btn_home_face',80,60,'./Ico/face.png'])
        self.btn_home_bodyays = QPushButton()
        self.home_btns.append([self.btn_home_bodyays,0,2,1,1,'人体分析','btn_home_bodyays',80,60,'./Ico/bodyays.png'])
        self.btn_home_ocr = QPushButton()
        self.home_btns.append([self.btn_home_ocr,0,3,1,1,'文字识别','btn_home_ocr',80,60,'./Ico/ocr.png'])
        self.btn_home_imgrec = QPushButton()
        self.home_btns.append([self.btn_home_imgrec,1,0,1,1,'图像识别','btn_home_imgrec',80,60,'./Ico/imgrec.png'])
        self.btn_home_imgsearch = QPushButton()
        self.home_btns.append([self.btn_home_imgsearch,1,1,1,1,'图像搜索','btn_home_imgsearch',80,60,'./Ico/imgsearch.png'])
        self.btn_home_imgup = QPushButton()
        self.home_btns.append([self.btn_home_imgup,1,2,1,1,'图像效果增强','btn_home_imgup',80,60,'./Ico/imgup.png'])
        self.btn_home_nlp = QPushButton()
        self.home_btns.append([self.btn_home_nlp,1,3,1,1,'自然语言处理','btn_home_nlp',80,60,'./Ico/nlp.png'])
        self.btn_home_kgraph = QPushButton()
        self.home_btns.append([self.btn_home_kgraph,2,0,1,1,'知识图谱','btn_home_kgraph',80,60,'./Ico/kgraph.png'])
        self.btn_home_audit = QPushButton()
        self.home_btns.append([self.btn_home_audit,2,1,1,1,'内容审核','btn_home_audit',80,60,'./Ico/audit.png'])
        self.btn_home_music = QPushButton()
        self.home_btns.append([self.btn_home_music,2,2,1,1,'音乐','btn_home_music',80,60,'./Ico/music.png'])
        self.btn_home_video = QPushButton()
        self.home_btns.append([self.btn_home_video,2,3,1,1,'视频','btn_home_video',80,60,'./Ico/video.png'])


        # 为btn设置参数
        for btn in self.home_btns:
            list(map(lambda v1, v2, v3, v4,v5: self.glayout_home.addWidget(v1, v2, v3, v4, v4), [btn[0]],[btn[1]],[btn[2]],[btn[3]],[btn[4]]))
            btn[0].setObjectName(btn[6])
            # btn[0].setText(btn[5])
            # btn[0].setFixedSize(btn[7],btn[8])
            # 设置css样式表
            css = ":hover{background-color:%s;}" \
                  "QPushButton{background-color:%s;}" \
                  "QPushButton:pressed{background-color:%s;}" \
                  "QToolTip{color:%s;font:Yahei;font-size:14px}" %(random_color(),random_color(),random_color(),random_color()) # border:0px
            #background-color:%s; random_color(),
            btn[0].setStyleSheet(css)
            btn[0].setToolTip(btn[5])

            btn[0].setIcon(QIcon(btn[9]))
            btn[0].resize(btn[7],btn[8])

            # btn[0].setIconSize(QSize(btn[7], btn[8]))
            h = self.height()*0.8/5
            w = self.width()*0.8/4
            if h > 100: h = 100
            if w > h*1.3: w = h*1.3
            if h > w/1.3: h = w/1.3
            btn[0].setIconSize(QSize(w,h ))
            # 掩膜，不规则图
            # pix = QPixmap(btn[9])
            # btn[0].setFixedSize(pix.size())
            # btn[0].setMask(pix.mask())

            # self.btn_home_voice.clicked.connect(self._init_voice_ui__)
            btn[0].clicked.connect(self.leave_home_event)


        self._home_reload()


    @layout_dele
    def _home_reload(self,*args):
        # 更新forward btn
        if func_historys[2]:
            self.btn_top_forward.setVisible(True)
        else:
            self.btn_top_forward.setVisible(False)
        self.btn_top_back.setVisible(False)
        for btn in self.home_btns:
            btn[0].setVisible(True)

        return self.glayout_home


    @layout_dele
    def _tool_voice(self,*args):
        """
        语音合成，识别模块
        :return:
        """
        # 初始化模块总布局
        self.glayout_voice = QGridLayout()
        self.glayout_main.addLayout(self.glayout_voice,2,0)

        self.txedit_voice = QTextEdit()
        self.glayout_voice.addWidget(self.txedit_voice, 0,0,1,1)

        return self.glayout_voice

    @layout_dele
    def _test_ui(self,*args):
        self.glayout_test = QGridLayout(self)
        self.glayout_main.addLayout(self.glayout_test,1,0)

        self.pbar = QProgressBar()
        self.pbar.setAlignment(Qt.AlignCenter)
        self.pbar.setFixedSize(100,10)
        self.glayout_test.addWidget(self.pbar,0,0,1,1)
        self.btn_ok = QPushButton()
        self.glayout_test.addWidget(self.btn_ok,1,1,1,1)
        self.btn_ok.clicked.connect(self._tool_voice)

        return self.glayout_test

    def bottom_pbar_changed(self,*args):
        pass

    def set_bottom_pabr_value(self,value=None):
        self.Outter_Run.value = list(range(101))
        self.Outter_Run.start()





    def resizeEvent_ui(self, a0: QtGui.QResizeEvent) -> None:
        value = int(self.width()*0.2 /6)
        self.glayout_home.setSpacing(value)
        pass


    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:

        # 背景
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), QPixmap('./Ico/bg_img.png'))

class Outter_Run(QThread):
    sign = pyqtSignal(object)

    def __init__(self,*args):
        super(Outter_Run, self).__init__()
        self.value = None

    def run(self,*args):
        for value in self.value:
            time.sleep(0.2)
            self.sign.emit(value)


if __name__ == "__main__":


    app = QApplication(sys.argv)
    UI = Ui()
    UI.show()
    sys.exit(app.exec_())