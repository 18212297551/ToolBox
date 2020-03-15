from PyQt5.QtWidgets import QCheckBox, QSizePolicy

from ToolBox.main_ui import *
from ToolBox.styleSheet import *

screenRecordState = False

class Screen(Ui):
    def __init__(self):
        super(Screen, self).__init__()
        self.__screen_var__()
        self.__screen_ui__()
        self.btn_home_screen.clicked.connect(self.screen_reload)

        self.getWindows()

    def __screen_ui__(self):
        self.glayout_screen_main = QGridLayout()
        self.glayout_screen_main.setObjectName("grade_2")
        self.glayout_main.addLayout(self.glayout_screen_main, 2, 0)

        self.glayout_screen_widget = QGridLayout()
        self.glayout_screen_main.addLayout(self.glayout_screen_widget,0,0,Qt.AlignTop)

        self.glayout_screen_show = QGridLayout()
        self.glayout_screen_main.addLayout(self.glayout_screen_show,1,0)

        self.btn_screen_record = QPushButton("录制")
        self.btn_screen_record.clicked.connect(self.btn_screen_ok_clicked)

        self.btn_screen_shoot = QPushButton('截屏')
        self.btn_screen_shoot.clicked.connect(self.getScreen)

        # 可录屏窗口
        self.cmbox_screen_windows = QComboBox()
        self.cmbox_screen_windows.setFont(QFont("YaHei", 10))
        self.cmbox_screen_windows.setToolTip("选择需要录制的窗口。\n请确定窗口被打开，\n并且没有最小化")
        self.cmbox_screen_windows.currentTextChanged.connect(self.cmbox_screen_windows_currentTextChanged)

        # 刷新可录屏窗口
        self.btn_screen_update = QPushButton('刷新窗口')
        self.btn_screen_update.clicked.connect(self.getWindows)

        # 保存文件名
        self.lnedit_screen_filename = QLineEdit()
        self.lnedit_screen_filename.setClearButtonEnabled(True)
        self.lnedit_screen_filename.setPlaceholderText("保存文件名")

        # 录屏坐标
        self.lnedit_screen_offset = QLineEdit()
        self.lnedit_screen_offset.setClearButtonEnabled(True)
        self.lnedit_screen_offset.setPlaceholderText('录屏区域 x1, y1, x2, y2')

        # 帧率
        self.spb_screen_fps = QSpinBox()
        self.spb_screen_fps.setRange(1,120)
        self.spb_screen_fps.setValue(24)
        self.spb_screen_fps.valueChanged.connect(self.spb_screen_fps_valueChanged)

        # 录制时间
        self.label_screen_record_time = QLabel()
        self.label_screen_record_time.setAlignment(Qt.AlignCenter)

        # 超帧限制
        self.ckbox_screen_fps_limit = QCheckBox()
        self.ckbox_screen_fps_limit.stateChanged.connect(self.ckbox_screen_fps_limit_stateChanged)
        self.ckbox_screen_fps_limit.setText('超帧限制')
        self.ckbox_screen_fps_limit.setChecked(True)

        # 录屏内容显示
        self.label_screen_show = QLabel()
        self.glayout_screen_show.addWidget(self.label_screen_show,0,1,1,1)
        self.label_screen_show.setVisible(False)
        self.label_screen_show.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))

        # 录屏时间显示
        self.sld_screen_show = QSlider(Qt.Vertical)
        self.sld_screen_show.setFixedWidth(0)
        self.glayout_screen_show.addWidget(self.sld_screen_show,0,0,1,1)
        self.sld_screen_show.setVisible(False)

        self.screen_widgets = [[self.ckbox_screen_fps_limit, (1,0,1,1)],[self.label_screen_record_time, (0,3,1,1)],[self.btn_screen_record, (0, 4, 1, 1)],[self.btn_screen_shoot,(0,5,1,1)],[self.lnedit_screen_filename,(0,0,1,3)],
                               [self.lnedit_screen_offset,(1,3,1,2)],[self.cmbox_screen_windows,(1,2,1,1)], [self.btn_screen_update,(1,1,1,1)],[self.spb_screen_fps,(1,5,1,1)]]

        for w in self.screen_widgets:
            w[0].setVisible(False)
            w[0].setObjectName('screen')
            self.glayout_screen_widget.addWidget(w[0],*w[1])
            w[0].setStyleSheet(get_css())
            w[0].setMinimumWidth(30)




    def __screen_var__(self):
        self.screen_resize_state = True
        self.screen_btnLeft_press = False
        self.stateQueue = Queue()
        self.screenRecordState = False
        self.windows_info = []
        self.myWindowId = 4131912

        # 存储显示的图像，用于缩放，防止失真严重，所有显示图像均需经过此变量
        self.screen_show_pic = None


        self.screenFPS = 24
        self.recordX1 = 0
        self.recordY1 = 0
        self.recordX2 = 1920
        self.recordY2 = 1080
        self.screenSize = (self.recordX2-self.recordX1, self.recordY2-self.recordY1)
        self.screenBbox = (self.recordX1, self.recordY1, self.recordX2, self.recordY2)
        self.videowriter = None #cv2.VideoWriter('./Temp/myVideo{}.mp4'.format(random.randint(100, 999)), cv2.VideoWriter_fourcc(*"mp4v"), self.screenFPS, self.screenSize)

        self.screenRecordProcess = MyScreenProcess()
        self.screenRecordProcess.videotime.connect(self.screenRecordProcess_videotime)
        self.screen_fps_upper_limit = True


    @layout_dele
    def screen_reload(self, *args):
        """屏幕录制模块重载"""

        if func_historys[3]: self.btn_top_forward.setVisible(True)
        else: self.btn_top_forward.setVisible(False)

        self.setVisible_by_layout(self.glayout_screen_main,True)

        return self.glayout_screen_main

    @catch_except
    def btn_screen_ok_clicked(self, *args):
        if self.screenRecordState:
            self.screenRecordState = False
            self.stateQueue.put(False)
            self.btn_screen_record.setText('录制')
            self.label_screen_record_time.clear()

            return
        self.screenRecordState = True
        img = QApplication.primaryScreen().grabWindow(self.myWindowId).toImage()
        self.screenRecordProcess.myWindowId = self.myWindowId
        self.screenRecordProcess.state = self.stateQueue
        self.screenRecordProcess.screen = QApplication.primaryScreen()
        self.screenRecordProcess.screenFPS = self.screenFPS

        text = self.lnedit_screen_offset.text()
        if text and not text.endswith(','):
            text += ','
            text = text.replace('，', ',')
        xys = re.findall('(.*?),', text)
        if xys:
            xys = [int(x) for x in xys]
            offset = (xys[0], xys[1], xys[2]-xys[0], xys[3]-xys[1])
            self.screenRecordProcess.offset = offset
        else: self.screenRecordProcess.offset = ()

        filename = self.lnedit_screen_filename.text()
        if filename:
            filename = filename.replace('/', '\\')
            if '.' not in filename: filename += '.mp4'
            if filename[1:3] != ':\\':
                filename = '{}\Record\Video\{}'.format(ROOTDIR, filename)
            self.screenRecordProcess.filename = filename
        else: self.screenRecordProcess.filename = r'{}\Record\Video\V{}.mp4'.format(ROOTDIR,time.strftime("%Y%m%d%H%M%S", time.localtime()))

        self.screenRecordProcess.fps_upper_limit = self.screen_fps_upper_limit
        self.screenRecordProcess.start()
        self.btn_screen_record.setText('停止')


    def getWindows(self):
        """获取可录制窗口"""
        self.windows_info.clear()
        self.cmbox_screen_windows.clear()

        def get_windeow_info(wid, mouse):
            if win32gui.IsWindow(wid) and win32gui.IsWindowEnabled(wid) and win32gui.IsWindowVisible(wid):
                text = win32gui.GetWindowText(wid)
                if len(text)>20: text = text[:20]
                self.windows_info.append("{}: {}".format(wid, text))
        win32gui.EnumWindows(get_windeow_info,0)

        for i in range(len(self.windows_info)):
            index = 0
            for j in range(len(self.windows_info)-i-1):
                if len(self.windows_info[index]) < len(self.windows_info[index+1]):
                    self.windows_info[index], self.windows_info[index+1] = self.windows_info[index+1], self.windows_info[index]
                index += 1

        self.windows_info.insert(0,"0: 全屏")
        for w in self.windows_info:
            self.cmbox_screen_windows.addItem(w)


    def getScreen(self):
        """获取屏幕截图"""
        text = self.lnedit_screen_offset.text()
        if text and not text.endswith(','):
            text += ','
            text = text.replace('，', ',')
        xys = re.findall('(.*?),', text)
        if xys:
            xys = [int(x) for x in xys]
            offset = (xys[0], xys[1], xys[2]-xys[0], xys[3]-xys[1])
        else: offset = ()

        filename = self.lnedit_screen_filename.text()
        if filename:
            filename = filename.replace('/', '\\')
            if '.' not in filename: filename += '.png'
            if filename[1:3] != ':\\':
                filename = '{}\Record\Img\ScreenShots\{}'.format(ROOTDIR, filename)
            filename = filename
        else: filename = r'{}\Record\Img\ScreenShots\{}.png'.format(ROOTDIR,time.strftime("%Y%m%d%H%M%S", time.localtime()))

        screen = QApplication.primaryScreen()
        img = screen.grabWindow(self.myWindowId, *offset)#.toImage()
        img.save(filename)
        self.screen_show_pic = img

        img2 = img.scaled(self.label_screen_show.width(), self.label_screen_show.height())
        self.label_screen_show.setPixmap(img2)
        # QMessageBox.information(self,"截屏提示", self.text_to_newline('截屏完成, 保存在: {}'.format(filename),40)) #'截屏完成, 保存在:\n {}'.format(filename)
        self.label_top_right.setText('截屏完成, 保存在: {}'.format(filename), maxt=30, sec=200, alive=20000)


    def cmbox_screen_windows_currentTextChanged(self, p):
        # 修改录制窗口
        wid = re.findall('(.*?):',p)
        if wid:
            self.myWindowId = int(wid[0])

    def spb_screen_fps_valueChanged(self, p):
        self.screenFPS = p

    def screenRecordProcess_videotime(self, content):
        # 显示录制时长
        p = content[1]
        m = p // 60
        s = p % 60
        h = m //60
        m = m % 60
        self.label_screen_record_time.setText("{}:{}:{}".format(h,m,s))
        if self.label_screen_show.isVisible():
            pix = QPixmap()
            pix = pix.fromImage(content[0])
            self.screen_show_pic = pix
            pix = pix.scaled(self.label_screen_show.width(), self.label_screen_show.height())
            self.label_screen_show.setPixmap(pix)

        # 避免线程关闭延迟造成time_label未重置
        if not self.screenRecordState:
            self.label_screen_record_time.clear()


    def ckbox_screen_fps_limit_stateChanged(self,p):
        # 当获取屏幕速度高于设定帧率时，是否设定等待时间
        if self.ckbox_screen_fps_limit.isChecked():
            self.screen_fps_upper_limit = True
        else: self.screen_fps_upper_limit = False

    @catch_except
    def resizeEvent_screen(self, a0: QtGui.QResizeEvent, *args) -> None:
        if self.btn_screen_record.isVisible():
            self.screen_show_pic_resize()



    def screen_show_pic_resize(self):
        """图片尺寸随窗口缩放"""
        pix = self.label_screen_show.pixmap()
        if pix:
            # 复制保存图片，不能直接更改，避免图片多次调整尺寸失真
            pix = self.screen_show_pic.copy()
            self.label_screen_show.clear()
            self.label_screen_show.resize(QSize(self.width(), self.height()-90))
            img = Image.fromqpixmap(pix)
            img = img.resize(size=(self.label_screen_show.width(), self.label_screen_show.height()))
            img = img.toqpixmap()
            self.label_screen_show.setPixmap(img)


class MyScreenProcess(QThread):
    videotime = pyqtSignal(object)
    def __init__(self):
        super(MyScreenProcess, self).__init__()

        self.myWindowId = int
        self.videoWriter = object
        self.state = object
        self.filename = './Temp/myVideo{}.mp4'.format(random.randint(100, 999))
        self.screenFPS = 24
        self.screen = None
        self.offset = ()
        self.fps_upper_limit = True


    @catch_except
    def run(self, *args) -> None:
        # self.screen = QApplication.primaryScreen()
        img = self.screen.grabWindow(self.myWindowId, *self.offset).toImage()

        self.videoWriter = cv2.VideoWriter(self.filename, cv2.VideoWriter_fourcc(*"mp4v"),
                        self.screenFPS, (img.width(), img.height()))

        num = 0
        while True:
            num += 1
            start = time.time()
            img = self.screen.grabWindow(self.myWindowId, *self.offset).toImage()
            img = img.convertToFormat(4)
            ptr = img.bits()
            ptr.setsize(img.byteCount())
            # strData = ptr.asstring()
            arr = np.array(ptr).reshape(img.height(), img.width(), 4)
            img2 = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
            img3 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
            self.videoWriter.write(img3)

            if not self.state.empty():
                state = self.state.get()
                if state is False:
                    self.videoWriter.release()
                    break
            if self.fps_upper_limit:
                end = time.time()
                pause = 1.0/self.screenFPS - (end-start)
                if pause > 0:
                    time.sleep(pause)

            self.videotime.emit([img, num//self.screenFPS])

