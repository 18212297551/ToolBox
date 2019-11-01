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


@20191026
现阶段基本实现策略
采用窗口控件先加载，要访问哪个业务，就重载出那个业务所需的控件，使用layouy_dele装饰器函数，将其他未使用的控件进行隐藏，
由此实现不同业务的多窗口需求，
通过在调用layout_dele装饰器时，记录各个层次窗口，以实现forward和back功能
通过self.send()函数，监测点击的按钮的text，从而判断是哪个按钮被点击了，该进入哪个业务，重载哪个窗口

"""
from PyQt5.QtWidgets import QCheckBox

from ToolBox.voice import *
from ToolBox.face_ import *
from ToolBox.bodyays import *
from ToolBox.imrec import *
from ToolBox.t_ocr import *
from ToolBox.imsearch import *
from ToolBox.imgup import *
from ToolBox.t_nlp import *
from ToolBox.video import *



class Main(Voice,Face,Body,Imrec,Ocr,Imsearch,ImgUp,Nlp,Video):
    def __init__(self):
        super(Main, self).__init__()


    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.resizeEvent_ui(a0)
        self.resizeEvent_face(a0)
        self.resizeEvent_body(a0)
        self.resizeEvent_ocr(a0)
        self.resizeEvent_imrec(a0)
        self.resizeEvent_imsearch(a0)
        self.resizeEvent_nlp(a0)
        self.resizeEvent_imup(a0)
        self.resizeEvent_video(a0)
        a0.accept()


    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.mouseDoubleClickEvent_video(a0)
        a0.accept()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if Set_UI.isEnabled():
            Set_UI.close()
        a0.accept()

    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        self.wheelEvent_video(a0)
        a0.accept()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.mouseMoveEvent_video(a0)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.mousePressEvent_video(a0)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.mouseReleaseEvent_video(a0)

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        self.keyPressEvent_video(a0)

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        self.keyPressEvent_video(a0)


    def user_info_change(self, infos=None, *args):
        infos = infos or {}
        appid = infos.get('APPID')
        apikey = infos.get('APIKEY')
        secretkey = infos.get('SECRETKEY')
        if appid:
            self.user_info_all_dict['APPID'] = appid
            self.APPID = appid
        if apikey:
            self.user_info_all_dict['APIKEY'] = apikey
            self.APIKEY = apikey
        if secretkey:
            self.user_info_all_dict['SECRETKEY'] = secretkey
            self.SECRETKEY = secretkey

        self.api_reload()
        self.userinfo_change_save()


    def api_reload(self):
        self.ApiVoice = AipSpeech(self.APPID,self.APIKEY,self.SECRETKEY)
        self.speech_syn = Speech_synthesis(self.ApiVoice)
        self.voice_ars = Voice_recognition(self.ApiVoice)
        self.speech_syn.speech_synthesis_log.connect(self.speech_syn_log_deal)
        self.voice_ars.asr_result.connect(self.voice_asr_result_deal)

        self.ApiImsearch = AipImageSearch(self.APPID,self.APIKEY,self.SECRETKEY)
        self.Apiocr = AipOcr(self.APPID,self.APIKEY,self.SECRETKEY)
        self.ApiBody = AipBodyAnalysis(self.APPID,self.APIKEY,self.SECRETKEY)
        self.ApiFace = AipFace(self.APPID,self.APIKEY,self.SECRETKEY)
        self.ApiImrec = AipImageClassify(self.APPID,self.APIKEY,self.SECRETKEY)



class Setting(QWidget):
    def __init__(self):
        super(Setting, self).__init__()
        self.__init_ui()
        self.infos = None

    def __init_ui(self):
        self.setWindowTitle('设置')
        self.setFixedSize(QSize(360,270))
        self.setWindowIcon(QIcon('{}/Ico/toolbox2.png'.format(ROOTDIR)))
        # self.setMaximumSize(QSize(640,480))
        self.setWindowFlags(Qt.WindowStaysOnTopHint) # 窗口置顶
        self.setObjectName('login')
        self.glayout_set_ui = QGridLayout()
        self.setLayout(self.glayout_set_ui)

        # 底部
        self.glayout_set_ui_bottom = QGridLayout()
        self.glayout_set_ui.addLayout(self.glayout_set_ui_bottom,2,0)

        self.btn_set_ui_ok = QPushButton('确定')
        self.btn_set_ui_cancel = QPushButton('关闭')
        self.glayout_set_ui_bottom.addWidget(self.btn_set_ui_ok,0,0,1,1)
        self.glayout_set_ui_bottom.addWidget(self.btn_set_ui_cancel,0,1,1,1)
        self.btn_set_ui_ok.setFixedWidth(60)
        self.btn_set_ui_cancel.setFixedWidth(60)
        self.btn_set_ui_cancel.setStyleSheet("*{color:%s;background:%s;border:0;height:30px}:pressed{color:%s;background:%s;}"%(random_color(mode='font'),random_color(mode='background'),random_color(mode='font'),random_color(mode='background')))
        self.btn_set_ui_ok.setStyleSheet("*{color:%s;background:%s;border:0;height:30px}:pressed{color:%s;background:%s;}"%(random_color(mode='font'),random_color(mode='background'),random_color(mode='font'),random_color(mode='background')))

        # 中部
        self.glayout_set_ui_center = QGridLayout()
        self.glayout_set_ui.addLayout(self.glayout_set_ui_center,1,0)

        self.lnedit_set_ui_appid = MLineEdit()
        self.label_set_ui_appid = QLabel()
        self.label_set_ui_appid.setText('APPID')
        self.lnedit_set_ui_apikey = MLineEdit()
        self.label_set_ui_apikey = QLabel()
        self.label_set_ui_apikey.setText('APIKEY')
        self.lnedit_set_ui_secretkey = MLineEdit()
        self.label_set_ui_secretkey = QLabel()
        self.label_set_ui_secretkey.setText('SECRETKEY')

        self.lnedit_set_ui_apikey.setClearButtonEnabled(True)
        self.lnedit_set_ui_apikey.returnPressed.connect(self.lnedit_set_ui_secretkey.setFocus)
        self.lnedit_set_ui_appid.setClearButtonEnabled(True)
        self.lnedit_set_ui_appid.returnPressed.connect(self.lnedit_set_ui_apikey.setFocus)
        self.lnedit_set_ui_secretkey.setClearButtonEnabled(True)
        self.lnedit_set_ui_secretkey.returnPressed.connect(self.btn_set_ui_ok_clicked)

        self.label_set_ui_changeUser = QLabel('账号信息')

        self.label_set_ui_form_top = QLabel('窗口样式')
        self.cmbox_set_ui_form_top = QComboBox()
        self.cmbox_set_ui_form_top.addItems(['Normal','Top','Bottom','NoFrame'])
        self.cmbox_set_ui_form_top.currentTextChanged.connect(self.cmbox_set_ui_form_top_changed)
        self.label_set_ui_opacity = QLabel('透明度')
        self.sd_set_ui_opacity = QSlider()
        self.sd_set_ui_opacity.setOrientation(Qt.Horizontal)
        self.sd_set_ui_opacity.setRange(0,100)
        self.sd_set_ui_opacity.setValue(0)
        self.sd_set_ui_opacity.valueChanged.connect(self.sd_set_ui_opacity_valuechanged)


        self.btn_set_ui_cancel.clicked.connect(self.btn_set_ui_cancel_clicked)
        self.btn_set_ui_ok.clicked.connect(self.btn_set_ui_ok_clicked)

        self.set_ui_widgets = [[self.label_set_ui_form_top,self.cmbox_set_ui_form_top],[self.label_set_ui_opacity,self.sd_set_ui_opacity],[self.label_set_ui_changeUser],[self.label_set_ui_appid,self.lnedit_set_ui_appid],[self.label_set_ui_apikey,self.lnedit_set_ui_apikey],[self.label_set_ui_secretkey,self.lnedit_set_ui_secretkey],
                               ]


        for row, widgets in enumerate(self.set_ui_widgets):
            for col, widget in enumerate(widgets):
                if len(widgets) == 1:
                    self.glayout_set_ui_center.addWidget(widget,row, col, 1, 2)
                    if widget.__doc__.startswith('QLabel'):
                        widget.setAlignment(Qt.AlignCenter)
                        widget.setFixedHeight(30)
                else:
                    self.glayout_set_ui_center.addWidget(widget,row, col, 1, 1)
                    if widget.__doc__.startswith('QLabel'):
                        widget.setAlignment(Qt.AlignCenter)
                        widget.setFixedWidth(80)

                css = "*{color:%s;background:%s;border:0;height:30px}" % (
                random_color(mode='font'), random_color(mode='background'))
                if widget == self.sd_set_ui_opacity:
                    css += "QSlider::handle{border: 0 ;background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 %s, stop:1 %s);border-radius:3px}" \
                           "QSlider::sub-page:horizontal{background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 %s, stop:1 %s)}" % (
                               random_color('background'), random_color('font'), random_color('background'),
                               random_color(
                                   'font'))

                widget.setStyleSheet(css)

    def sd_set_ui_opacity_valuechanged(self,p):
        # UI.form_ui_opacity(p)
        value = float(100 - p) / 100
        UI.setWindowOpacity(value)
        text = "透明度（{}）".format(p)
        self.label_set_ui_opacity.setText(text)

    def cmbox_set_ui_form_top_changed(self,mode):
        if mode == 'Top':
            UI.setWindowFlags(Qt.WindowStaysOnTopHint) # 窗口置顶

        elif mode == 'Bottom':
            UI.setWindowFlags(Qt.WindowStaysOnBottomHint) # 底部
        elif mode == 'NoFrame':
            warn = QMessageBox.warning(self,'提示','窗口将无法拖动、关闭和调整大小\n调整为其他类型即可恢复',QMessageBox.Ok|QMessageBox.Cancel)
            if warn == 1024:
                UI.setWindowFlags(Qt.FramelessWindowHint)
        else:
            UI.setWindowFlags(Qt.Window) # 取消窗口置顶

        UI.show()


    def btn_set_ui_ok_clicked(self):
        appid = self.lnedit_set_ui_appid.text()
        apikey = self.lnedit_set_ui_apikey.text()
        secretkey = self.lnedit_set_ui_secretkey.text()

        option = {}
        if appid: option.update({'APPID':appid})
        if apikey: option.update({'APIKEY':apikey})
        if secretkey: option.update({'SECRETKEY':secretkey})

        UI.user_info_change(option)
        code = QMessageBox.warning(self,'提示',"修改完成",QMessageBox.Ok|QMessageBox.Cancel)
        if code == 1024:
            self.close()



    def btn_set_ui_cancel_clicked(self):
        self.close()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.infos = UI.user_info_all_dict
        self.lnedit_set_ui_appid.setText(self.infos.get('APPID'))
        self.lnedit_set_ui_apikey.setText(self.infos.get('APIKEY'))
        self.lnedit_set_ui_secretkey.setText(self.infos.get('SECRETKEY'))
        self.lnedit_set_ui_secretkey.setEchoMode(MLineEdit.PasswordEchoOnEdit)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        UI.setEnabled(True)
        a0.accept()






if __name__ == "__main__":
    app = QApplication(sys.argv)
    UI = Main()
    Set_UI = Setting()
    btn = UI.set_btn
    btn.triggered.connect(Set_UI.show)
    UI.show()
    sys.exit(app.exec_())