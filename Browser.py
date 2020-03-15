"""
窗口布局
"""

import sys
import typing
import sip
from PyQt5 import QtGui,QtCore
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QWidget, QApplication, QToolButton, QGridLayout, QLineEdit, QLabel, QMessageBox,QPushButton

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from ToolBox.main_ui import *

def catch_except(func):
    import time
    import traceback
    def wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except:
            with open('./log.txt', 'a+') as _f:
                _error = traceback.format_exc()
                _t = '>'*10 + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '<'*10
                content = "\n{}\n{}\n".format(_t,_error)
                _f.write(content)
                print(_error)
    return wrapper

class Browser(Ui):
    def __init__(self):
        super(Browser, self).__init__()
        # self.resize(480,640)
        # self.setWindowTitle("Twinkstar")
        # # self.setWindowFlag(Qt.FramelessWindowHint)
        self.btn_home_browser.clicked.connect(self.browser_ui_reload)

        # 窗口配置初始化
        self.__init_var()
        self.__init_main()
        self.__init_tools()
        # self.__init_zoom()
        self.__init_bookmark()
        self.__init_browser_tab()
        self.__init_browser()
        self.__init_event_connect()
        self.setVisible_by_layout(self.glayout_browser_main, False)

        # # css样式表导入
        # css = open(r'.\resources\main_ui.css','r',encoding='utf-8').read()
        # self.setStyleSheet(css)

        # 屏幕分辨率
        self.screen_size = QApplication.desktop()


    @layout_dele
    def browser_ui_reload(self,*args):

        if func_historys[3]:self.btn_top_forward.setVisible(True)
        else:self.btn_top_forward.setVisible(False)

        self.setVisible_by_layout(self.glayout_browser_main, True)
        self.widget_browser.setVisible(True)

        return self.glayout_browser_main

    def __init_main(self):

        self.glayout_browser_main = QGridLayout()
        self.glayout_browser_main.setObjectName('grade_2')
        self.glayout_browser_main.setContentsMargins(0, 0, 0, 0)
        self.glayout_browser_main.setSpacing(0)
        # self.setMouseTracking(True)
        self.widget_browser = QWidget()
        self.widget_browser.setLayout(self.glayout_browser_main)
        self.widget_browser.setFixedSize(self.width(),self.height()-25)
        self.widget_browser.setVisible(False)
        # css样式表导入
        css = open(r'.\resources\main_ui.css','r',encoding='utf-8').read()
        # self.setStyleSheet(css)
        self.widget_browser.setStyleSheet(css)
        # 设置窗口总布局
        # self.setLayout(self.glayout_browser_main)
        # self.glayout_main.addLayout(self.glayout_browser_main, 2, 0)
        self.glayout_main.addWidget(self.widget_browser,2,0)
        # 为第一行的工具栏和窗口管理设置一个总布局
        self.glayout_first_row = QGridLayout()
        self.glayout_first_row.setObjectName("glayout_first_row")
        self.glayout_browser_main.addLayout(self.glayout_first_row, 0, 0)

        # 浏览器TAB页总布局
        self.glayout_tab_main = QGridLayout()
        self.glayout_tab_main.setObjectName("glayout_tab_main")
        self.glayout_browser_main.addLayout(self.glayout_tab_main, 1, 0)
        self.glayout_tab_main.setContentsMargins(0, 0, 0, 0)

    def __init_zoom(self):
        """
        窗口关闭、最小化、最大化
        :return:
        """
        self.glayout_zoom = QGridLayout()
        self.glayout_first_row.addLayout(self.glayout_zoom, 0,1)
        self.btn_zoom_min = QToolButton()
        self.btn_zoom_min.setObjectName("btn_zoom")
        self.btn_zoom_max = QToolButton()
        self.btn_zoom_max.setObjectName("btn_zoom")
        self.btn_zoom_close = QToolButton()
        self.btn_zoom_close.setObjectName("btn_zoom")
        Tools = [self.btn_zoom_min, self.btn_zoom_max, self.btn_zoom_close]
        ICOS = ['min.png', 'max1.png', 'close.png']
        for index, tool in enumerate(Tools):
            _ico = QIcon("./resources/ico/{}".format(ICOS[index]))
            tool.setIcon(_ico) # 添加图标
            # tool.setFixedSize(30,30)
            self.glayout_zoom.addWidget(tool, 0,index,1,1) # 加入布局
        # 记录鼠标按键状态
        self.mouse_left_state = False
        self.mouse_right_state = False
        self.mouse_mid_state = False
        # 记录鼠标相对窗口的位置
        self.mouse_curser = object

        # 窗口最大化状态
        self.zoom_max_state = False
        # 窗口最大化前的尺寸
        self.old_size = self.size()
        # 窗口最大化之前的位置
        self.old_pos = self.pos()



    def __init_tools(self):
        """
        工具栏&菜单栏
        :return:
        """
        self.glayout_tools = QGridLayout()
        self.glayout_tools.setSpacing(0)
        self.glayout_first_row.addLayout(self.glayout_tools,0,0)

        ICOS = [ "back.png", "pre.png", "space", "reload.png", "home.png", "download.png"]
        self.btn_tools_reload = QToolButton()
        self.btn_tools_reload.setObjectName('btn_tools')
        self.btn_tools_back = QToolButton()
        self.btn_tools_back.setObjectName("btn_tools")
        self.btn_tools_pre = QToolButton()
        self.btn_tools_pre.setObjectName("btn_tools")
        self.btn_tools_home = QToolButton()
        self.btn_tools_home.setObjectName("btn_tools")
        self.btn_tools_download = QToolButton()
        self.btn_tools_download.setObjectName("btn_tools")
        self.lnedit_tools_url = QLineEdit()
        self.lnedit_tools_url.setObjectName("lnedit_tools_url")
        Tools = [self.btn_tools_back, self.btn_tools_pre, self.lnedit_tools_url, self.btn_tools_reload, self.btn_tools_home, self.btn_tools_download]
        for tool, ico in zip(Tools, ICOS):
            _ico = QIcon("./resources/ico/{}".format(ico))
            if tool.objectName() == 'lnedit_tools_url':
                continue
            tool.setIcon(_ico)

        for index, tool in enumerate(Tools):
            self.glayout_tools.addWidget(tool, 0,index,1,1)
            # if tool.objectName() == 'lnedit_tools_url':
            #     tool.setFixedHeight(25)
            #     continue
            # tool.setFixedSize(30,30)


    def __init_bookmark(self):
        """
        书签栏
        :return:
        """
        self.glayout_bookmark = QGridLayout()
        self.glayout_browser_main.addLayout(self.glayout_bookmark, 2, 0)
        self.btn_bookmark_ = QToolButton()
        self.btn_bookmark_.setObjectName("btn_bookmark_")
        _ico = QIcon("./resources/ico/bookmark.png")
        self.btn_bookmark_.setIcon(_ico)

        self.glayout_bookmark.addWidget(self.btn_bookmark_, 0,0,1,1)

    def __init_browser_tab(self):
        # 浏览器标签布局
        self.tab_num = 0
        self.glayout_browser_tab = QGridLayout()
        self.glayout_tab_main.addLayout(self.glayout_browser_tab, 0,2)

        # 首部LABEL
        self.label_btab_first = QLabel()
        self.label_btab_first.setObjectName("label_btab_first")
        self.glayout_tab_main.addWidget(self.label_btab_first,0,0)
        self.label_btab_first.setFixedWidth(60)
        self.label_btab_first.setText(" 可拖动")

        # 前部TAB隐藏显示按钮
        self.btn_btab_showtab_first = QToolButton()
        self.btn_btab_showtab_first.setObjectName("btn_btab")
        self.glayout_tab_main.addWidget(self.btn_btab_showtab_first, 0,1)
        self.btn_btab_showtab_first.setIcon(QIcon("./resources/ico/left_s.png"))
        # self.btn_btab_showtab_first.setFixedSize(30,30)


        # 后部TAB隐藏显示
        self.btn_btab_showtab_last = QToolButton()
        self.btn_btab_showtab_last.setObjectName("btn_btab")
        self.glayout_tab_main.addWidget(self.btn_btab_showtab_last,0,3)
        self.btn_btab_showtab_last.setIcon(QIcon("./resources/ico/right_s.png"))
        # self.btn_btab_showtab_last.setFixedSize(30,30)


        # 新建tab按钮
        self.btn_btab_newtab = QToolButton()
        self.btn_btab_newtab.setObjectName("btn_btab")
        self.glayout_tab_main.addWidget(self.btn_btab_newtab,0,4)
        # self.btn_btab_newtab.clicked.connect(self.btn_btab_newtab_clicked)
        self.btn_btab_newtab.setIcon(QIcon("./resources/ico/add.png"))
        # self.btn_btab_newtab.setFixedSize(30,30)

        # 尾部label
        self.label_btab_last = QLabel()
        self.label_btab_last.setObjectName("label_btab_last")
        self.glayout_tab_main.addWidget(self.label_btab_last, 0,5)
        self.label_btab_last.setText("Twinkstar Browser ")
        self.label_btab_last.setAlignment(Qt.AlignRight)







    def __init_browser(self):
        """
        浏览器界面
        :return:
        """

        self.glayout_browser = QGridLayout()
        self.glayout_browser_main.addLayout(self.glayout_browser, 3, 0)
        self.browser = QWebEngineView()
        self.browser.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.glayout_browser.addWidget(self.browser)
        self.browser.load(QUrl("https://www.csdn.net/"))
        # self.breowser.show()


    def __init_var(self):
        # 按键状态
        self.ctrl_state = False
        self.shift_state = False

        # 浏览器缩放比例
        self.breowser_zoom_factor = 1

    def __init_event_connect(self):
        # self.btn_zoom_min.clicked.connect(self.showMinimized)
        # self.btn_zoom_max.clicked.connect(self.showMaximized)
        # self.btn_zoom_close.clicked.connect(self.closeEvent)
        self.lnedit_tools_url.returnPressed.connect(self.lnedit_tools_url_returnPressed)

        # 浏览器
        self.btn_tools_reload.clicked.connect(self.browser.reload)
        self.btn_tools_pre.clicked.connect(self.browser.forward)
        self.btn_tools_back.clicked.connect(self.browser.back)
        self.btn_tools_home.clicked.connect(self.btn_tools_home_clicked)
        self.browser.urlChanged.connect(self.browser_urlChanged)
        self.browser.showMaximized()


    def browser_urlChanged(self,p):
        self.lnedit_tools_url.setText(p.toString())
        u = self.browser.url()
        t = self.browser.title().title()


    def btn_tools_home_clicked(self):
        self.browser.load(QUrl("http://www.baidu.com"))


    def lnedit_tools_url_returnPressed(self):
        url = self.lnedit_tools_url.text()
        print(url)
        if not url.startswith("http"):
            url = 'https://www.baidu.com/s?word={}&tn=88093251_35_hao_pg'.format(url)
        self.browser.load(QUrl(url))




    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        if self.zoom_max_state:
            _ico = QIcon("./resources/ico/max1.png")
            self.btn_zoom_max.setIcon(_ico)
            self.zoom_max_state = False


    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        warn = QMessageBox.warning(self,'提示', '确认退出？', QMessageBox.Ok|QMessageBox.No, QMessageBox.No)
        if warn == 1024: # cancel 65536
            sys.exit()



    def showMaximized(self) -> None:
        if self.zoom_max_state:
            self.move(self.old_pos)
            self.resize(self.old_size)
            _ico = QIcon("./resources/ico/max1.png")
            self.btn_zoom_max.setIcon(_ico)
            self.zoom_max_state = False
        else:
            self.old_size = self.size()
            self.old_pos = self.pos()
            _ico = QIcon("./resources/ico/max2.png")
            self.btn_zoom_max.setIcon(_ico)
            self.showFullScreen()
            self.setGeometry(0,0,self.screen_size.width(), self.screen_size.height())
            self.zoom_max_state = True




    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        # l:16777234 r:16777236 t:16777235 d:16777237 enter:16777221 return:16777220 ctrl:16777249 shift:16777248

        if a0.key() == 16777249: #16777249
            self.ctrl_state = True

        elif a0.key() == 16777248: #16777248
            self.shift_state = True


    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == 16777249:
            self.ctrl_state = False
        elif a0.key() == 16777248:
            self.shift_state = False



    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        # 调整浏览器缩放
        if self.ctrl_state and self.browser.hasFocus():
            delta = a0.angleDelta()
            if delta.y() > 0:
                if self.breowser_zoom_factor <= 2:
                    self.breowser_zoom_factor *= 1.2
            else:
                if self.breowser_zoom_factor >= 0.3:
                    self.breowser_zoom_factor *= 0.8
            self.browser.setZoomFactor(self.breowser_zoom_factor)

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:

        if self.mouse_left_state:
            # 实现窗口移动
            pos = a0.globalPos() - self.mouse_curser
            self.move(pos)

    def mousePressEvent_(self, a0: QtGui.QMouseEvent) -> None:
        # 将鼠标按键信号与状态变量绑定
        if a0.button() == Qt.LeftButton:
            self.mouse_curser = a0.pos()
            self.mouse_left_state = True
        elif a0.button() == Qt.RightButton:
            self.mouse_right_state = True
        elif a0.button() == Qt.MidButton:
            self.mouse_mid_state = True

    def mouseReleaseEven_t(self, a0: QtGui.QMouseEvent) -> None:
        # 恢复鼠标按键状态
        if a0.button() == Qt.LeftButton:
            self.mouse_left_state = False
        elif a0.button() == Qt.RightButton:
            self.mouse_right_state = False
        elif a0.button() == Qt.MidButton:
            self.mouse_mid_state = False

    def mousePressEvent__(self, event):
        if (event.button() == QtCore.Qt.LeftButton) and (event.pos() in self.corner_rect):
            # 鼠标左键点击右下角边界区域
            self._corner_drag = True
            event.accept()
        elif (event.button() == QtCore.Qt.LeftButton) and (event.pos() in self.right_rect):
            # 鼠标左键点击右侧边界区域
            self._right_drag = True
            event.accept()
        elif (event.button() == QtCore.Qt.LeftButton) and (event.pos() in self.bottom_rect):
            # 鼠标左键点击下侧边界区域
            self._bottom_drag = True
            event.accept()
        elif (event.button() == QtCore.Qt.LeftButton) and (event.pos() in self.left_rect):
            # 鼠标左键点击右侧边界区域
            self._left_drag = True
            event.accept()

        elif (event.button() == QtCore.Qt.LeftButton) and (event.pos() in self.top_rect):
            # 鼠标左键点击下侧边界区域
            self._top_drag = True
            event.accept()
        elif (event.button() == QtCore.Qt.LeftButton) and (event.pos() in self.leftcprner_rect):
            self._leftcorner_drag = True
            event.accept()

        # 移动
        elif (event.button() == QtCore.Qt.LeftButton or event.button() == QtCore.Qt.MidButton) and (event.pos() in self.move_rect):
            # if  self._top_drag == False and self._left_drag == False and self._corner_drag == False and self._bottom_drag == False and self._right_drag == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标





    def mouseMoveEvent__(self, QMouseEvent):
        if QMouseEvent.pos() in self.corner_rect:
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif QMouseEvent.pos() in self.bottom_rect:
            self.setCursor(QtCore.Qt.SizeVerCursor)
        elif QMouseEvent.pos() in self.right_rect:
            self.setCursor(QtCore.Qt.SizeHorCursor)
        elif QMouseEvent.pos() in self.top_rect:
            self.setCursor(QtCore.Qt.SizeVerCursor)
        elif QMouseEvent.pos() in self.left_rect:
            self.setCursor(QtCore.Qt.SizeHorCursor)
        elif QMouseEvent.pos() in self.leftcprner_rect:
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif self.m_flag:
            self.setCursor(QtCore.Qt.OpenHandCursor)


        else:
            self.setCursor(QtCore.Qt.ArrowCursor)

        if QtCore.Qt.LeftButton and self._right_drag:
            # 右侧调整窗口宽度
            self.resize(QMouseEvent.pos().x(), self.height())
            QMouseEvent.accept()
        elif QtCore.Qt.LeftButton and self._bottom_drag:
            # 下侧调整窗口高度
            self.resize(self.width(), QMouseEvent.pos().y())
            QMouseEvent.accept()
        elif QtCore.Qt.LeftButton and self._corner_drag:
            # 右下角同时调整高度和宽度
            self.resize(QMouseEvent.pos().x(), QMouseEvent.pos().y())
            QMouseEvent.accept()
        elif QtCore.Qt.LeftButton and self._top_drag:
            # 上侧侧调整窗口高度
            self.setGeometry(self.pos().x(), QMouseEvent.globalPos().y(), self.width(), (self.pos().y() + self.height() - QMouseEvent.globalPos().y()))
            QMouseEvent.accept()
        elif QtCore.Qt.LeftButton and self._left_drag:
            # 左侧同时调整高度和宽度
            self.setGeometry(QMouseEvent.globalPos().x(), self.pos().y(), (self.pos().x() + self.width() - QMouseEvent.globalPos().x()), self.height())

            QMouseEvent.accept()
        elif QtCore.Qt.LeftButton and self._leftcorner_drag:
            self.setGeometry(QMouseEvent.globalPos().x(), QMouseEvent.globalPos().y(),
                             (self.width() + self.pos().x() - QMouseEvent.globalPos().x()), (self.height() + self.pos().y() - QMouseEvent.globalPos().y()))
            QMouseEvent.accept()

        elif QtCore.Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    UI = Form_Ui()
    UI.show()
    sys.exit(app.exec_())


