from PyQt5.QtWidgets import QListWidgetItem

from ToolBox.main_ui import *


class Video(Ui):
    def __init__(self):
        super(Video, self).__init__()
        self.__init_video_ui()
        self.btn_home_video.clicked.connect(self.video_home_reload)

        # 鼠标滚轮控制音量
        self.video_mouse_to_set_vol = False


    def __init_video_ui(self):
        self.glayout_video_home = QGridLayout()
        self.glayout_video_home.setObjectName('grade_2')
        self.glayout_video_home.setSpacing(0)
        self.glayout_main.addLayout(self.glayout_video_home,2,0,Qt.AlignTop)

        self.glayout_video_top = QGridLayout()
        self.glayout_video_home.addLayout(self.glayout_video_top,0,0)

        self.glayout_video_center = QGridLayout()
        self.glayout_video_home.addLayout(self.glayout_video_center,1,0)

        self.glayout_video_bottom = QGridLayout()
        self.glayout_video_home.addLayout(self.glayout_video_bottom,2,0)
        self.lnedit_video_url = MLineEdit()
        self.lnedit_video_url.setClearButtonEnabled(True)
        self.lnedit_video_url.returnPressed.connect(self.btn_video_home_ok_clicked)
        self.lnedit_video_url.setPlaceholderText('支持本地和URL播放，鼠标移到窗体右下侧显示列表，双击播放')
        self.glayout_video_top.addWidget(self.lnedit_video_url,0,2,1,1)
        self.btn_video_home_ok = QPushButton('播放')
        self.glayout_video_top.addWidget(self.btn_video_home_ok,0,3,1,1)
        self.btn_video_home_ok.clicked.connect(self.btn_video_home_ok_clicked)
        self.btn_video_home_ok.setFixedSize(60,30)
        self.btn_video_stop = QPushButton('暂停')
        self.btn_video_stop.setFixedSize(60,30)
        self.glayout_video_top.addWidget(self.btn_video_stop,0,4,1,1)
        self.btn_video_stop.clicked.connect(self.btn_video_stop_clicked)

        self.label_video_proPos = QLabel()
        self.label_video_proPos.setFixedSize(80,30)
        self.glayout_video_top.addWidget(self.label_video_proPos, 0, 0, 1, 1)
        self.slider_video_vol = QSlider(Qt.Horizontal)
        self.slider_video_vol.setRange(0,100)
        self.slider_video_vol.setValue(30)
        self.slider_video_vol.setFixedSize(80,30)
        self.slider_video_vol.valueChanged.connect(self.slider_video_vol_valueChanged)
        self.glayout_video_top.addWidget(self.slider_video_vol,0,1,1,1)
        self.video_player = QMediaPlayer()
        self.video_plist = QMediaPlaylist()
        self.video_plist.setPlaybackMode(QMediaPlaylist.Sequential) # 循环模式设置

        self.video_player.setPlaylist(self.video_plist)
        self.video_player.setVolume(30)
        self.video_videowidget = QVideoWidget()
        self.video_player.setVideoOutput(self.video_videowidget)
        self.glayout_video_center.addWidget(self.video_videowidget,0,1,1,3)
        # self.video_plist_additem(r"{}\Ico\b8.png".format(ROOTDIR))
        self.video_videowidget.setMouseTracking(True)
        self.pix_video_center = QPixmap(self.video_videowidget.size())
        self.video_videowidget.addAction(QAction(QIcon().addPixmap(self.pix_video_center)))
        # self.glayout_video_center.addWidget(self.pix_video_center,0,1,1,3)

        # self.label_video_center = QLabel()
        # self.glayout_video_center.addWidget(self.label_video_center,0,1,1,3)

        self.video_videowidget.dropEnterChanged.connect(self.video_plist_additem)
        self.video_player.durationChanged.connect(self.video_player_durationChanged)
        self.video_player.positionChanged.connect(self.video_player_positionchanged)
        self.video_player.stateChanged.connect(self.video_player_stateChanged)

        # 播放列表
        self.lwdt_video_indo = QListWidget()
        self.glayout_video_center.addWidget(self.lwdt_video_indo,0,3,1,1)
        self.lwdt_video_indo.setFixedWidth(120)
        self.lwdt_video_indo.doubleClicked.connect(self.lwdt_video_info_item_doubleclicked)
        self.lwdt_video_indo.setToolTip('未播放状态下窗口不会刷新，\n所以出现过的界面不会消失，\n但是不能点击，只是显示而已')
        # self.video_videowidget.setToolTip('未播放状态下窗口不会刷新，\n所以出现过的界面不会消失，\n但是不能点击，只是显示而已')

        item = QListWidgetItem()
        item.setText('   双击打开文件夹')
        item.setFont(QFont('YaHei', 12))
        item.setTextAlignment(Qt.AlignLeft)
        self.lwdt_video_indo.addItem(item)
        self.lwdt_video_indo.setSpacing(2)
        self.slider_video_process = QSlider()
        self.glayout_video_center.addWidget(self.slider_video_process,0,0,1,1 )
        self.slider_video_process.setOrientation(Qt.Vertical)
        self.slider_video_process.setFixedWidth(5)
        self.slider_video_process.sliderMoved.connect(self.slider_video_process_sliderMoved)


        self.video_home_widgets = [self.lwdt_video_indo,self.btn_video_stop,self.label_video_proPos, self.slider_video_vol, self.slider_video_process,self.lnedit_video_url,self.btn_video_home_ok,self.video_videowidget]
        for widget in self.video_home_widgets:
            color = (random_color(mode='background'), random_color(mode='font'), random_color(mode='background'), random_color(mode='font'), random_color(mode='background'),
                     random_color(mode='font'))
            if widget not in [self.video_videowidget]:
                css = "*{background-color:%s;color:%s;border:0;font:YaHei;height:30px} :pressed{background-color:%s;color:%s;} QToolTip{background-color:%s;color:%s;border:0;font:YaHei;height:30px}" % color
                if widget in [self.slider_video_vol, self.slider_video_process]:
                    css += "QSlider::handle{border: 0 ;background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 %s, stop:1 %s);border-radius:3px}" \
                           "QSlider::sub-page:horizontal{background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 %s, stop:1 %s)}" % (
                               random_color('background'), random_color('font'), random_color('background'),
                               random_color(
                                   'font'))  # border-radius:px  background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
                if widget in [self.lwdt_video_indo]:
                    css += "QListWidget{alternate-background-color: %s; }"
                widget.setStyleSheet(css)
            widget.setVisible(False)




    @catch_except
    def btn_video_stop_clicked(self,*args):
        # self.video_player.stop()
        if self.video_player.state() == 1:
            self.btn_video_stop.setText('继续')
            self.video_player.pause()
        else:
            self.btn_video_stop.setText('暂停')
            self.video_player.play()


    def slider_video_vol_valueChanged(self, p):
        self.video_player.setVolume(p)

    @catch_except
    def slider_video_process_sliderMoved(self, p):
        self.video_player.setPosition(p)
        # self.video_player.

    @catch_except
    def label_propos_textchange(self, p):
        maxtime = self.slider_video_process.maximum()
        secmax = maxtime // 1000
        minmax = secmax // 60
        hmax = minmax // 60
        secmax -= minmax * 60
        if minmax == 0 and secmax == 0 and hmax == 0:
            self.label_video_proPos.clear()
        else:
            if len(str(minmax)) == 1: minmax = '0' + str(minmax)
            if len(str(secmax)) == 1: secmax = '0' + str(secmax)
            maxtime = '{}:{}:{}'.format(hmax, minmax, secmax)
            if hmax == 0:
                maxtime = '{}:{}'.format(minmax, secmax)
                if self.label_video_proPos.width() != 80:
                    self.label_video_proPos.setFixedSize(80,30)
            else:
                self.label_video_proPos.setFixedSize(120,30)
            sec = p // 1000
            min_ = sec // 60
            h = min_ // 60
            sec -= min_ * 60
            if min_ == 0 and sec == 0 and hmax == 0:
                self.label_video_proPos.setText(' --/{}'.format(maxtime))
            else:
                if len(str(sec)) == 1: sec = '0' + str(sec)
                if len(str(min_)) == 1: min_ = '0' + str(min_)
                currentTime = '{}:{}:{}'.format(h,min_, sec)
                if h == 0:
                    currentTime = '{}:{}'.format(min_, sec)
                self.label_video_proPos.setText(' {}/{}'.format(currentTime, maxtime))

    @catch_except
    def video_player_positionchanged(self,p):
        self.slider_video_process.setValue(p)
        self.label_propos_textchange(p)

    @catch_except
    def video_player_stateChanged(self, p):
        if p == 1:
            self.video_player_durationChanged(p=None) # 重新执行top_label_scroll
            self.btn_video_home_ok.setText('添加')  # ok按钮设置
            self.btn_video_stop.setText('暂停')
        else:
            self.label_top_right.setText('')
            self.btn_video_home_ok.setText('播放') # ok按钮设置
            self.btn_video_stop.setText('继续')


    @catch_except
    def video_player_durationChanged(self, p, *args):
        """修改top_label_right_text, 设置进度条范围"""
        if p:
            self.slider_video_process.setRange(0, p)
        index = self.video_plist.currentIndex()
        if index != -1:
            self.lwdt_video_indo.setCurrentRow(index+1) # 更新播放列表显示, 第一项是自定义的，要排除
            filepath = self.lwdt_video_indo.currentItem().text()
            filepath = filepath.replace('/', '\\')
            name = re.findall('(.*)\\\\(.*?)$', filepath)
            if name:
                self.label_top_right.setText(name[0][1])

    @catch_except
    def video_player_currentMediaChanged(self):
        """修改top_label_right_text"""
        index = self.video_plist.currentIndex()
        filepath = self.video_list[index]
        filepath = filepath.replace('/', '\\')
        name = re.findall('(.*)\\\\(.*?)$', filepath)
        if name:
            self.label_top_right.setText(name[0][1])


    @catch_except
    def lwdt_video_info_item_doubleclicked(self, p):
        p = self.lwdt_video_indo.currentRow()
        if p > 0:
            self.video_plist.setCurrentIndex(p-1)
            self.video_player_play()
        elif p == 0:
            files = QFileDialog.getOpenFileNames(self, '选择文件','./','AllFile(*)')
            if files:
                files = files[0]
                for file in files:
                    self.video_plist_additem(file,False)


    @catch_except
    def video_player_play(self, p=None):
        self.video_player.play()

    @catch_except
    def video_plist_additem(self, p, pl=True):
        """与QVideoWidget的dropenterchanged绑定，拽入播放,所有的添加都应该使用此方法 """
        if re.sub('\s','',p):
            self.lnedit_video_url.setText(str(p))
            if os.path.isfile(p) or os.path.isdir(p):
                filepaths = self.dirs_to_files(p)
                for index, filepath in enumerate(filepaths):
                    self.lwdt_video_indo.addItem(filepath)
                    self.video_plist.addMedia(QMediaContent(QUrl.fromLocalFile(filepath)))
                    if (index == 0 and pl) or self.video_player.state() == 0:
                        self.video_plist.setCurrentIndex(self.video_plist.mediaCount()-1)
                        self.video_player_play() #E:\Programme\GIT\Python\Others\Exceise\sndn

            else:
                self.lwdt_video_indo.addItem(p)
                self.video_plist.addMedia(QMediaContent(QUrl.fromLocalFile(p)))
                if pl or self.video_player.state() == 0:
                    self.video_plist.setCurrentIndex(self.video_plist.mediaCount() - 1)
                    self.video_player_play()
            self.video_videowidget.show()
            self.lwdt_video_indo.scrollToBottom()  # 滚动到底部

        else:
            QMessageBox.information(self,'提示','请输入播放文件路径或URL，\n或双击播放列表播放')





    def btn_video_home_ok_clicked(self,*args):
        """播放按钮绑定事件"""
        url = self.lnedit_video_url.text()
        if self.btn_video_home_ok.text() == '播放':
            self.video_plist_additem(url)
        else:
            self.video_plist_additem(url,pl=False)



    @catch_except
    def video_fullscreen_play(self, p=True):
        main_homes = self.meau_widgets + self.status_widgets
        videos = []
        for i in range(self.glayout_video_top.count()):
            videos.append(self.glayout_video_top.itemAt(i).widget())
        if p:
            if self.video_videowidget.isVisible(): # 避免在通过菜单返回时显示
                self.slider_video_process.setFixedWidth(5)
                for video in videos:
                    video.setVisible(True)
            else:
                for video in videos:
                    video.setVisible(False)

            for widget in main_homes:
                    widget.setVisible(True)

        else:
            if self.video_videowidget.isVisible():
                self.slider_video_process.setFixedWidth(0)
            for video in videos:
                video.setVisible(False)

            for widget in main_homes:
                widget.setVisible(False)
            self.showFullScreen()

        self.update()

    def resizeEvent_video(self, a0: QtGui.QResizeEvent) -> None:
        if self.width() > 1910 and self.height() >1000 and self.video_player.state() == 1:
            self.video_fullscreen_play(False)



    def keyPressEvent_video(self, a0: QtGui.QKeyEvent) -> None:
        if self.video_videowidget.isVisible() and self.video_player.state() == 1:
            # 音量进度键盘控制
            self.lnedit_video_url.clearFocus()
            self.video_videowidget.setFocus()
            old = self.video_player.position()
            if a0.key() == 16777236:#右
                self.video_player.setPosition(old + 3000)
            elif a0.key() == 16777234:#左
                self.video_player.setPosition(old - 3000)
            elif a0.key() == 16777237:#向下
                self.video_plist.next()
            elif a0.key() == 16777235:#向上
                self.video_plist.previous()

            elif a0.key() == 16777249:
                self.video_mouse_to_set_vol = True

        if a0.key() == 16777216:  # esc
            # if self.width() > 1900 and self.height() > 1000:
            self.video_fullscreen_play(True)  # 还原隐藏的控件
            if self.video_videowidget.isVisible():
                self.video_videowidget.showNormal()
            self.showNormal()

    def keyReleaseEvent_video(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == 16777249: #ctri
            self.video_mouse_to_set_vol = False

    def wheelEvent_video(self, a0: QtGui.QWheelEvent) -> None:
        if self.video_videowidget.isVisible() and not self.lwdt_video_indo.isVisible():
            """鼠标进度音量控制"""
            y = a0.angleDelta().y()
            if self.video_mouse_to_set_vol:
                old = self.slider_video_vol.value()
                if y > 0:
                    self.slider_video_vol.setValue(old + 2)
                elif y < 0:
                    self.slider_video_vol.setValue(old - 2)

            elif self.video_player.state() == 1:
                old = self.video_player.position()
                if a0.pos() in self.video_videowidget.geometry():
                    if y > 0:
                        self.video_player.setPosition(old + 2000)
                    elif y < 0:
                        self.video_player.setPosition(old - 2000)
    def mousePressEvent_video(self, a0: QtGui.QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            self.video_mouse_to_set_vol = True

    def mouseReleaseEvent_video(self, a0: QtGui.QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            self.video_mouse_to_set_vol = False

    def mouseMoveEvent_video(self, a0: QtGui.QMouseEvent) -> None:
        if self.video_videowidget.isVisible():
            # 播放列表显示
            if a0.pos().x() > self.width() - 40 and a0.pos().y() > self.height() // 3:
                self.lwdt_video_indo.setFixedWidth(self.width()//4)
                self.lwdt_video_indo.setVisible(True)
                self.lwdt_video_indo.show()
            else:
                self.lwdt_video_indo.setVisible(False)
                self.lwdt_video_indo.hide()

            if self.isFullScreen():
                # 全屏播放时显示播放控制     #菜单栏
                configs = self.meau_widgets
                for i in range(self.glayout_video_top.count()):
                    configs.append(self.glayout_video_top.itemAt(i).widget())
                if a0.y() < 60:
                    for widhet in configs:
                        widhet.setVisible(True)
                elif self.lnedit_video_url.isVisible():
                    for widhet in configs:
                        widhet.setVisible(False)
                elif a0.x() < 40 and a0.y() > 60 and self.slider_video_process.width() == 0: # 进度条显示
                    self.slider_video_process.setFixedWidth(5)
                elif a0.x() > 35 and self.slider_video_process.width() == 5:
                    self.slider_video_process.setFixedWidth(0)
        self.clearMask()

    def mouseDoubleClickEvent_video(self, a0: QtGui.QMouseEvent) -> None:
        if self.video_videowidget.isVisible():
            if a0.button() == Qt.LeftButton:
                if not self.lwdt_video_indo.isVisible():
                    if self.video_player.state() != 1:
                        self.video_player.play()
                    else:
                        self.video_player.pause()
            elif a0.button() == Qt.RightButton:
                if self.isFullScreen():
                    self.video_fullscreen_play(True)
                    self.showNormal()
                else:
                    self.video_fullscreen_play(False)


        # if self.video_videowidget.isVisible():
        #     if a0.button() == 1:
        #         if self.video_videowidget.isFullScreen():
        #             self.video_videowidget.showNormal()
        #         else:
        #             self.video_videowidget.showFullScreen()

    @layout_dele
    def video_home_reload(self,*args):
        """视频播放重载"""
        if func_historys[3]:self.btn_top_forward.setVisible(True)
        else:self.btn_top_forward.setVisible(False)

        for widget in self.video_home_widgets:
            widget.setVisible(True)

        self.lwdt_video_indo.setVisible(False) # 默认隐藏播放列表


        return self.glayout_video_home


class QVideoWidget(QVideoWidget):
    __doc__ = 'QVideoWidget()'
    dropEnterChanged = pyqtSignal(object)
    def __init__(self):
        super(QVideoWidget, self).__init__()
        self.setAcceptDrops(True)


    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent) -> None:
        if a0.mimeData():
            a0.accept()
        else:
            a0.ignore()

    @catch_except
    def dropEvent(self, a0: QtGui.QDropEvent) -> None:
        text = a0.mimeData().text().replace('file:///', '')
        self.setObjectName(text)
        self.dropEnterChanged.emit(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    UI = Video()
    # Set_UI = Setting()
    # btn = UI.set_btn
    # btn.triggered.connect(Set_UI.show)
    UI.show()
    sys.exit(app.exec_())


