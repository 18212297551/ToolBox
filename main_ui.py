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
import shutil
import os
import pickle
import re
import random
import socket
import sys
import time
import threading
import traceback
from pydub import AudioSegment
import requests
import json
import base64
from PIL import Image,ImageDraw
import pyautogui
import cv2
from multiprocessing import Process,Queue
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QTimer, QPoint, QSize, QThread, pyqtSignal, QUrl, QFileSelector, QFile, QRect
from PyQt5.QtGui import QIcon, QPalette, QBrush, QPixmap, QPainter, QFont, QTransform, QPen, QColor
from PyQt5.QtMultimediaWidgets import QVideoWidget

from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QProgressBar, QPushButton, QMenuBar, QAction, qApp, \
    QMenu, QTextEdit, QLabel, QColorDialog, QToolButton, QLineEdit, QListWidget, QComboBox, QSlider, QSpinBox, \
    QMessageBox, QFileDialog, QListWidgetItem
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist

from ToolBox.baidu_aip import AipSpeech, AipFace, AipBodyAnalysis, AipImageClassify,AipOcr,AipImageSearch,AipNlp,AipContentCensor,AipKg,imageprocess
from ToolBox.encrypt import *

# =========================================全局变量==============================================
ROOTDIR = os.getcwd() # 当前根目录
func_historys = [None,None,None,None,None,None] # 之前访问的各级窗口初始化函数，用于实现back and forward
func_before = None #上次刷新窗口调用的函数
before_layout = None # 当前窗口所在布局

socket.setdefaulttimeout(15)

# APPID = '17376947' #182
# APIKEY = 'K7G0KLcoQnTLH4QjmCZMigyM'
# SECRETKEY = 'xqdTGx6mMB6pu3WtD9c0r8yX9Sxy0OiL'

# 用于语音合成等
RUNID = time.strftime('%Y%m%d%H%M%S', time.localtime()) + str(random.randint(0,9))
BGCOLORS = [] # 背景设置使用过的颜色，保证文字与背景颜色不同

__init_my_dirs = ['Record/Voice/Temp', 'Record/Img/Crop', 'Record/Img/Merge', 'Record/Img/Draw', 'Record/Img/BodySeg', 'Config', 'Record\Img\Imgup']

for di in __init_my_dirs:
    di = os.path.abspath(di)
    if not os.path.exists(di): os.makedirs(di)


def catch_except(func):
    def wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except:
            with open('{}./Config/log.txt'.format(ROOTDIR), 'a+') as _f:
                _error = str(traceback.format_exc())
                _t = '[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ']'
                content = "\n{}\n{}\n".format(_t,_error)
                _f.write(content)
                print(_error)
                _err = _error[-400:] if len(_error) > 401 else _error
                classname = type(args[0]).__name__
                if not classname in ['Speech_synthesis','Voice_recognition','Setting','QVideoWidget','ScrollLabel']:
                    try:
                        args[0].pbar_bottom.reset()
                    except Exception as e:
                        _f.write(str(e))
                        print(str(e))
                    QMessageBox.warning(args[0], '出错了...', _err)
                if "KeyError: 'access_token'" in _err:
                    print('账户信息错误')

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
    设置上一个布局的控件不可见，以显示当前布局控件
    :param func:
    :return:
    """
    @catch_except
    def inner(*args):
        global before_layout, func_historys,func_before
        @catch_except
        def delete(layouts):
            if layouts:
                for _i in range(layouts.count()):
                    t = layouts.itemAt(_i).__doc__
                    # 防止layout中还有layout
                    if t == 'QGridLayout(QWidget)\nQGridLayout()':
                        delete(layouts.itemAt(_i))
                    elif not layouts.itemAt(_i).widget() is None:
                        layouts.itemAt(_i).widget().setVisible(False)
                        layouts.itemAt(_i).widget().close()
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
        BGCOLORS.append(color)

    elif mode == 'font':
        r = random.randint(0, 100)
        g = random.randint(0,100)
        b = random.randint(0,100)
        color = 'rgb({},{},{})'.format(r,g,b)
        if color in BGCOLORS:
            return random_color(mode,r,g,b)

    else: raise TypeError("invalid parameter {}".format(mode))

    return color

TopColor = random_color('background') # 顶部菜单栏随机颜色，为label_top_right颜色一致


class Ui(QWidget):
    """
    窗体主模块
    """
    def __init__(self,*args):
        super(Ui, self).__init__()
        self.__init_main__()
        self.__init_ui__() # 其他窗口依赖项
        self.__init_status__()
        self.__init_meau_main__()
        self.__init_home__()

        self.__init_var__() # 包含时间关联，最后初始化

        self.btn_home_audit.clicked.connect(self.no_compele)
        self.btn_home_kgraph.clicked.connect(self.no_compele)
        self.setAcceptDrops(True)


    def no_compele(self):
        QMessageBox.information(self,'提示','还没有开发呢')

    def __init_ui__(self,*args):
        self.resize(715,480)
        self.setWindowTitle('Toolbox')
        # self.setWindowIcon(QIcon('{}/Ico/toolbox.png'.format(ROOTDIR).format(ROOTDIR)))
        f_ico = open(r'{}/Ico/toolbox.png'.format(ROOTDIR).format(ROOTDIR),'rb')
        pix = QPixmap()
        pix.loadFromData(f_ico.read()) # 读取文件流生成图标
        self.setWindowIcon(QIcon(pix))
        self.setMouseTracking(True)
        # self.setWindowOpacity(0.8)

        self.setStyleSheet('*{background-color: #FFFFFF}')
        # self.setWindowFlags(Qt.WindowStaysOnTopHint) # 窗口置顶
        # 总布局
        self.glayout_main = QGridLayout()
        self.glayout_main.setSpacing(0)
        self.glayout_main.setContentsMargins(0, 0, 0, 0)
        # 为窗体添加布局
        self.setLayout(self.glayout_main)

        # C = QColorDialog().getColor()


    def __init_main__(self):
        self.APPID = '17621214'
        self.APIKEY = 'kUaRn85Ljekp2AapOZaSMNIe'
        self.SECRETKEY = 'SVABkvSEzMGMhRkFqV0gxCO19Aqwo4gK'
        self.user_info_all_dict = {}
        path = r'{}/Config/config'.format(ROOTDIR)
        if os.path.exists(path):
            with open(path, 'r') as f_config:
                data = self.read_info_from_file(f_config.read())
                if data:
                    data = json.loads(data)
                    if 'APPID' and 'APIKEY' and 'SECRETKEY' in data.keys():
                        self.user_info_all_dict.update(data)
                        self.APPID = self.user_info_all_dict.get('APPID')
                        self.APIKEY = self.user_info_all_dict.get('APIKEY')
                        self.SECRETKEY = self.user_info_all_dict.get('SECRETKEY')
            os.remove(path)
        self.user_info_all_dict['APPID'] = self.APPID
        self.user_info_all_dict['APIKEY'] = self.APIKEY
        self.user_info_all_dict['SECRETKEY'] = self.SECRETKEY
        self.userinfo_change_save()

    def read_info_from_file(self, fb, key=None):
        if not key: key = 'BNM123456'
        try:
            data = decrypt(int(fb), key)
            return data
        except Exception as e:
            return None
        # APPID = '17621214' #152
        # APIKEY = 'kUaRn85Ljekp2AapOZaSMNIe'
        # SECRETKEY = 'SVABkvSEzMGMhRkFqV0gxCO19Aqwo4gK'


    @catch_except
    def userinfo_change_save(self,*args):

        with open(r'Config\config','w') as f:
            key = 'BNM123456'
            data = json.dumps(self.user_info_all_dict)
            data_int,k = encrypt(data,key)
            f.write(data_int.__str__())
            # print('保存完成')

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
        self.glayout_main.addLayout(self.glayout_top, 1, 0, Qt.AlignTop)

        # 菜单栏 左侧
        self.glayout_meau = QGridLayout()
        self.glayout_top.addLayout(self.glayout_meau,0,0)
        self.meau_main = QMenuBar()
        self.meau_main.setFixedSize(100,30)
        # self.meau_main.setWindowIcon(QIcon('{}/Ico/bg_img.png'.format(ROOTDIR)))
        self.glayout_meau.addWidget(self.meau_main,0,0,1,1)

        self.set_btn = QAction('设置',self.meau_main)
        self.set_btn.setText('设置')
        # meau.triggered.connect(self._test_ui)
        self.meau_main.addAction(self.set_btn)


        # 返回按钮等
        self.btn_top_back = QToolButton()
        self.btn_top_back.setIcon(QIcon('{}/Ico/back.png'.format(ROOTDIR).format(ROOTDIR)))
        self.btn_top_back.setStyleSheet('*{width:22px;height:22px;border:0}')
        self.glayout_meau.addWidget(self.btn_top_back,0,1,1,1)
        self.btn_top_forward = QToolButton()
        self.btn_top_forward.setIcon(QIcon('{}/Ico/forward.png'.format(ROOTDIR).format(ROOTDIR)))
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

        self.label_top_right = ScrollLabel()
        self.label_top_right.setObjectName('label_top_right')
        # self.label_top_right.setText('label')
        self.label_top_right.setFixedWidth(150)
        self.label_top_right.setAlignment(Qt.AlignCenter)

        # self.label_top_show.setAutoFillBackground(True)
        self.label_top_right.setMouseTracking(True)
        self.glayout_top_right.addWidget(self.label_top_right, 0, 0, 1, 1)

        self.meau_widgets = [self.meau_main,self.btn_top_back,self.btn_top_forward,self.label_top_center,self.label_top_right]
        color = (TopColor, random_color(mode='font'), random_color(mode='background'),
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

        # 底部状态栏清空
        self.pbar_bottom.reset()
        self.label_status_left.clear()
        self.label_status_right.clear()

    @catch_except
    def btn_top_forward_clicked(self,*args):
        """实现窗口向前，注意子窗口调用函数中应该不包含sender()初始化，否则将导致窗口向前失效"""
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
        self.glayout_main.addLayout(self.glayout_status, 3, 0, Qt.AlignBottom)
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
        self.glayout_main.addLayout(self.glayout_home, 2, 0, Qt.AlignCenter)
        self.glayout_home.setSpacing(int(self.width()*0.2/6))
        self.glayout_home.setContentsMargins(10,10,10,10)

        # btn及其参数
        self.home_btns = []

        self.btn_home_voice = QPushButton()
        self.home_btns.append([self.btn_home_voice,0,0,1,1,'语音技术','btn_home_voice',80,60,'{}/Ico/voice.png'.format(ROOTDIR)])
        self.btn_home_face = QPushButton()
        self.home_btns.append([self.btn_home_face,0,1,1,1,'人脸识别','btn_home_face',80,60,'{}/Ico/face.png'.format(ROOTDIR)])
        self.btn_home_bodyays = QPushButton()
        self.home_btns.append([self.btn_home_bodyays,0,2,1,1,'人体分析','btn_home_bodyays',80,60,'{}/Ico/bodyays.png'.format(ROOTDIR)])
        self.btn_home_ocr = QPushButton()
        self.home_btns.append([self.btn_home_ocr,0,3,1,1,'文字识别','btn_home_ocr',80,60,'{}/Ico/ocr.png'.format(ROOTDIR)])
        self.btn_home_imgrec = QPushButton()
        self.home_btns.append([self.btn_home_imgrec,1,0,1,1,'图像识别','btn_home_imgrec',80,60,'{}/Ico/imgrec.png'.format(ROOTDIR)])
        self.btn_home_imgsearch = QPushButton()
        self.home_btns.append([self.btn_home_imgsearch,1,1,1,1,'图像搜索','btn_home_imgsearch',80,60,'{}/Ico/imgsearch.png'.format(ROOTDIR)])
        self.btn_home_imgup = QPushButton()
        self.home_btns.append([self.btn_home_imgup,1,2,1,1,'图像效果增强','btn_home_imgup',80,60,'{}/Ico/imgup.png'.format(ROOTDIR)])
        self.btn_home_nlp = QPushButton()
        self.home_btns.append([self.btn_home_nlp,1,3,1,1,'自然语言处理','btn_home_nlp',80,60,'{}/Ico/nlp.png'.format(ROOTDIR)])
        self.btn_home_kgraph = QPushButton()
        # self.home_btns.append([self.btn_home_kgraph,2,0,1,1,'知识图谱','btn_home_kgraph',80,60,'{}/Ico/kgraph.png'.format(ROOTDIR)])
        self.btn_home_audit = QPushButton()
        # self.home_btns.append([self.btn_home_audit,2,1,1,1,'内容审核','btn_home_audit',80,60,'{}/Ico/audit.png'.format(ROOTDIR)])
        self.btn_home_music = QPushButton()
        # self.home_btns.append([self.btn_home_music,2,2,1,1,'音乐','btn_home_music',80,60,'{}/Ico/music.png'.format(ROOTDIR)])
        self.btn_home_browser = QPushButton()
        # self.home_btns.append([self.btn_home_browser,2,1,1,1,'浏览器','btn_home_music',80,60,'{}/Ico/music.png'.format(ROOTDIR)])
        self.btn_home_video = QPushButton()
        self.home_btns.append([self.btn_home_video,2,0,1,1,'视频','btn_home_video',80,60,'{}/Ico/video.png'.format(ROOTDIR)])


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




    def bottom_pbar_changed(self,*args):
        pass

    def set_bottom_pabr_value(self,value=None):
        self.Outter_Run.value = list(range(101))
        self.Outter_Run.start()

    def dict_get_value(self, dicts, value='',grade=-1):
        """遍历字典并返回所有数据"""
        grade += 1
        if isinstance(dicts, dict):
            for k, v in dicts.items():
                if isinstance(v, dict):
                    value += '{}{}:\n'.format('  ' * grade, k)
                    value = self.dict_get_value(v, value, grade)
                elif isinstance(v, tuple) or isinstance(v, list):
                    value += "{}{}:\n".format('  ' * grade, k)
                    value = self.list_get_value(v, value, grade)
                else:
                    value += '{}{}:{}\n'.format('  ' * grade, k, v)
        elif isinstance(dicts, tuple) or isinstance(dicts, list):
            value = self.list_get_value(dicts, value, grade)
        else:
            value += '{}{}\n'.format('  ' * grade, dicts)
        return value

    def list_get_value(self,lists, value='', grade=-1):
        """遍历列表并返回所有数据"""
        if isinstance(lists, tuple) or isinstance(lists, list):
            for l in lists:
                if isinstance(lists, tuple) or isinstance(lists, list):
                    value = self.list_get_value(l, value, grade)
                elif isinstance(l, dict):
                    value = self.dict_get_value(l, value, grade)
                else:
                    if str(l).replace('\s','').replace('\n', ''):
                        value += "{}{}:\n".format('  ' * grade, l)
                    else:value += "{}{}\n".format('  ' * grade, l)
        elif isinstance(lists, dict):
            value = self.dict_get_value(lists, value, grade)

        else:
            if str(lists).replace('\n', '').replace('\t', ''):
                value += "{}{}:\n".format('  ' * grade, lists)
            else:
                value += "{}{}\n".format('  ' * grade, lists)

        return value

    def dict_get_value_by_key(self,dicts, key, value=''):
        """遍历字典并返回指定键值的所有数据"""

        def list_get_dict(lists, _key, _value=''):
            """遍历列表并返回所有数据"""
            if isinstance(lists, tuple) or isinstance(lists, list):
                for l in lists:
                    if isinstance(lists, tuple) or isinstance(lists, list):
                        _value = list_get_dict(l, _key, _value)
                    elif isinstance(l, dict):
                        _value = self.dict_get_value_by_key(l, _key, _value)
            elif isinstance(lists, dict):
                _value = self.dict_get_value_by_key(lists, _key, _value)
            return _value

        if isinstance(dicts, dict):
            if key in dicts.keys(): value += dicts.get(key) + '\n'
            for k, v in dicts.items():
                if isinstance(v, dict):
                    value = self.dict_get_value_by_key(v, key, value)
                elif isinstance(v, tuple) or isinstance(v, list):
                    value = list_get_dict(v, key, value)

        elif isinstance(dicts, tuple) or isinstance(dicts, list):
            value = list_get_dict(dicts, key, value)

        return value

    def resizeEvent_ui(self, a0: QtGui.QResizeEvent) -> None:
        value = int(self.width()*0.2 /6)
        self.glayout_home.setSpacing(value)
        pass


    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:

        # 背景
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), QPixmap('{}/Ico/bg_img.png'.format(ROOTDIR)))


    def dirs_to_files(self,path):
        my_files = []
        if os.path.isfile(path):
            my_files.append(path)
        elif os.path.isdir(path):
            alls = list(os.walk(path))
            for files in alls:
                for index, file in enumerate(files[2]):
                    filepath = r'{}\{}'.format(files[0],file)
                    my_files.append(filepath)
        if my_files:
            return my_files
        return False

    def setVisible_by_layout(self, layout, state):
        """隐藏或显示布里的控件"""
        for i in range(layout.count()):
            widget = layout.itemAt(i)
            if widget.__doc__.startswith('QGridLayout'):
                self.setVisible_by_layout(widget,state)
            else:widget.widget().setVisible(state)


class MLineEdit(QLineEdit):
    """增加接受拽入"""
    __doc__ = 'MLineEdit()' # 控件隐藏函数需要
    def __init__(self):
        super(MLineEdit, self).__init__()
        self.setObjectName('MLineEdit')
        self.setAcceptDrops(True)

    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent) -> None:
        if a0.mimeData():
            a0.accept()
        else:
            a0.ignore()

    def dropEvent(self, a0: QtGui.QDropEvent) -> None:
        text = a0.mimeData().text().replace('file:///','')
        self.setText(text)


class ScrollLabel(QLabel):
    __doc__ = 'QLabel()'
    def __init__(self):
        super(ScrollLabel, self).__init__()
        """重写QLabel,增加绘制文本滚动"""
        self.init_pen()
        self.newx = 0
        self.maxText =  self.width()// self.fontInfo().pointSize()

        self.painter_timer = QTimer()
        self.painter_timer.timeout.connect(self.__draw_text)

    def init_pen(self):
        penColor = random_color('font')
        color = re.findall('.*?\((.*?),(.*?),(.*?)\)$',penColor)
        if color:
            color = color[0]
            r, g, b = [int(x) for x in color]
            self.penColor = QColor.fromRgb(r,g,b)
        else: self.penColor = Qt.gray
        self.pen = QPen(self.penColor, 2)

        color = re.findall('.*?\((.*?),(.*?),(.*?)\)$',TopColor)
        if color:
            color = color[0]
            r, g, b = [int(x) for x in color]
            self.pixColor = QColor.fromRgb(r,g,b)
        else:
            self.pixColor = QColor(Qt.gray)

    def setText(self, a0: str, scroll=True) -> None:
        self.maxText = self.width() // self.fontInfo().pointSize() # 修正最大容量
        self.txt = ' '*self.maxText + a0
        if len(a0) > self.maxText and scroll: #判断文字长度和scroll参数，满足启用滚动
            self.painter_timer.start(500)
        else:
            a = (self.maxText - len(a0)) // 2
            text = ' '*a + a0 + ' '*a # 文字居中
            self.painter_timer.stop()
            self.__draw_text(text)\

    def new_text(self):
        if len(self.txt) <= self.newx:
            self.newx = 0
        txt = self.txt[self.newx:self.newx + self.maxText] if len(self.txt) > self.newx + self.maxText else self.txt[self.newx:]

        return txt

    @catch_except
    def __draw_text(self, txt=None, *args):
        """绘制文字"""
        pix = QPixmap(self.width(), self.height())
        pix.fill(self.pixColor)
        painter = QPainter(pix)
        painter.setPen(self.pen)
        self.newx += 2
        if not txt:
            txt = self.new_text()
        painter.drawText(0, self.height()-self.font().pointSize(), txt)
        self.setPixmap(pix)
        del painter


class Outter_Run(QThread):
    sign = pyqtSignal(object)

    def __init__(self,*args):
        super(Outter_Run, self).__init__()
        self.value = None

    def run(self,*args):
        for value in self.value:
            time.sleep(0.2)
            self.sign.emit(value)


class MPushButton(QPushButton):
    """video播放列表定制"""
    doubleClicked = pyqtSignal(object)
    focusIned = pyqtSignal(object)
    focusOuted = pyqtSignal(object)
    def __init__(self):
        super(MPushButton, self).__init__()

    def focusInEvent(self, a0: QtGui.QFocusEvent) -> None:
        self.focusIned.emit(a0)

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.doubleClicked.emit(a0)

    def focusOutEvent(self, a0: QtGui.QFocusEvent) -> None:
        self.focusOuted.emit(a0)

class MWidget(QWidget):
    """video播放列表定制"""
    def __init__(self,path):
        super(MWidget, self).__init__()
        self.setMouseTracking(True)
        self.btn_dele = MPushButton()
        self.btn_dele.setIcon(QIcon('{}/Ico/dele.png'.format(ROOTDIR)))
        self.btn_dele.setFixedSize(30, 30)
        self.btn_dele.setObjectName('dele')
        self.filename = MPushButton()
        self.filename.setObjectName('filename')
        # self.filename.focusOuted.connect(self.btn_dele_setVisible)
        self.filename.clicked.connect(self.btn_dele_setVisible)
        self.btn_dele.focusOuted.connect(self.btn_dele_focusOutEvent)

        glayout_widget = QGridLayout()
        glayout_widget.setSpacing(0)
        glayout_widget.setContentsMargins(0, 0, 0, 0)
        self.setLayout(glayout_widget)
        self.setFixedHeight(30)
        new_path = path.replace('\\', '/')
        name = re.findall('.*/(.*?)$', new_path)
        if name:
            self.filename.setText(name[0])
        else:
            self.filename.setText(path)
        self.filename.setFixedHeight(30)
        self.filename.setToolTip('双击播放')
        # self.filename.setContentsMargins(0, 0, 0, 0)
        css = ":hover{background-color:%s;color:%s}" \
              "*{background-color:%s;color:%s;text-align:left}" \
              ":pressed{background-color:%s;color:%s;}" \
              "QToolTip{background-color:%s;color:%s;font:Yahei;font-size:14px}" % (
                  random_color('background'), random_color('font'), random_color('background'), random_color('font'),
                  random_color('background'), random_color('font'), random_color('background'), random_color('font'))  # border:0px
        self.setStyleSheet(css)
        glayout_widget.addWidget(self.btn_dele, 0, 0, 1, 1)
        glayout_widget.addWidget(self.filename, 0, 1, 1, 1)
        self.btn_dele.setVisible(False)


    def btn_dele_setVisible(self,p):
        if self.btn_dele.isVisible():
            self.btn_dele.setVisible(False)

        else:
            self.btn_dele.setVisible(True)
            # self.btn_dele.setFocus()

        self.setFocus() # 必须设置焦点给widhet要不然listwidget无法正常更新当前选中

    def focusOutEvent(self, a0: QtGui.QFocusEvent) -> None:
        if not  (self.btn_dele.hasFocus() or self.filename.hasFocus()):
            self.btn_dele.setVisible(False)

    def btn_dele_focusOutEvent(self,*args):
        if not  (self.btn_dele.hasFocus() or self.filename.hasFocus()):
            self.btn_dele.setVisible(False)



if __name__ == "__main__":

    app = QApplication(sys.argv)
    UI = Ui()
    UI.show()
    sys.exit(app.exec_())