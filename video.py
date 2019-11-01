from PyQt5.QtWidgets import QListWidgetItem

from ToolBox.main_ui import *


class Video(Ui):
    def __init__(self):
        super(Video, self).__init__()
        self.__init_video_ui()
        self.__init_video_first = True
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
        self.btn_video_home_ok.setToolTip('操作输入框')
        self.glayout_video_top.addWidget(self.btn_video_home_ok,0,3,1,1)
        self.btn_video_home_ok.clicked.connect(self.btn_video_home_ok_clicked)
        self.btn_video_home_ok.setFixedSize(60,30)
        self.btn_video_pause = QPushButton()
        self.btn_video_pause.setFixedSize(60, 30)
        self.glayout_video_top.addWidget(self.btn_video_pause, 0, 4, 1, 1)
        self.btn_video_pause.clicked.connect(self.btn_video_pause_clicked)

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
        self.video_plist.setPlaybackMode(QMediaPlaylist.Sequential) # 循环模式设置 #Sequential 顺序

        self.video_player.setPlaylist(self.video_plist)
        self.video_player.setVolume(30)
        self.video_videowidget = QVideoWidget()
        self.video_player.setVideoOutput(self.video_videowidget)
        self.glayout_video_center.addWidget(self.video_videowidget,0,1,1,3)
        # self.video_plist_additem(r"{}\Ico\b8.png".format(ROOTDIR))
        self.video_videowidget.setMouseTracking(True)
        self.pix_video_center = QPixmap(self.video_videowidget.size())
        self.video_videowidget.addAction(QAction(QIcon().addPixmap(self.pix_video_center)))


        # self.widget_video_center = QWidget()
        # glayout_video = QGridLayout()
        # self.widget_video_center.setLayout(glayout_video)
        #

        self.video_videowidget.dropEnterChanged.connect(self.video_plist_additem)
        self.video_player.durationChanged.connect(self.video_player_durationChanged)
        self.video_player.positionChanged.connect(self.video_player_positionchanged)
        self.video_player.stateChanged.connect(self.video_player_stateChanged)

        # 播放列表
        self.lwdt_video_info = QListWidget()
        self.glayout_video_center.addWidget(self.lwdt_video_info, 0, 3, 1, 1)
        self.lwdt_video_info.setFixedWidth(120)
        # self.lwdt_video_info.doubleClicked.connect(self.lwdt_video_info_item_doubleclicked)
        # self.lwdt_video_info.setToolTip('未播放状态下窗口不会刷新，\n所以出现过的界面不会消失，\n但是不能点击，只是显示而已')
        self.lwdt_video_info_dele_tips = True  # 设置是否启用删除确认
        self.lwdt_video_info_opened = True
        self.__init_lwdt_video_toolBtn() # 生成播放列表顶部tool按键

        # self.lwdt_video_info.setSpacing(2)
        self.slider_video_process = QSlider()
        self.glayout_video_center.addWidget(self.slider_video_process,0,0,1,1 )
        self.slider_video_process.setOrientation(Qt.Vertical)
        self.slider_video_process.setFixedWidth(5)
        self.slider_video_process.sliderMoved.connect(self.slider_video_process_sliderMoved)


        self.video_home_widgets = [self.lwdt_video_info, self.btn_video_pause, self.label_video_proPos, self.slider_video_vol, self.slider_video_process, self.lnedit_video_url, self.btn_video_home_ok, self.video_videowidget]
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
                if widget in [self.lwdt_video_info]:
                    css += "QListWidget{alternate-background-color: %s; }"
                widget.setStyleSheet(css)
            widget.setVisible(False)

        self.timer_video_update = QTimer()
        self.timer_video_update.timeout.connect(self.timer_video_update_timeout)

    def __init_lwdt_video_toolBtn(self):
        """初始化时生成播放列表顶部功能按键，需复用-清空列表是"""
        item = QListWidgetItem()
        item.setFont(QFont('YaHei', 10))
        item.setTextAlignment(Qt.AlignLeft)
        item.setSizeHint(QSize(120,30))
        widget = QWidget()
        glayout_widget = QGridLayout()
        glayout_widget.setSpacing(0)
        glayout_widget.setContentsMargins(0,0,0,0)
        glayout_widget.setAlignment(Qt.AlignLeft)
        widget.setLayout(glayout_widget)
        widget.setFixedHeight(30)
        css = "QPushButton:hover{background-color:%s;color:%s}QLable:hover{background-color:%s;color:%s}" \
              "*{background-color:%s;color:%s;border:0}" \
              "QPushButton:pressed{background-color:%s;color:%s}QLable:pressed{background-color:%s;color:%s}" \
              "QToolTip{background-color:%s;color:%s;font:Yahei;font-size:14px}" % (
              random_color('background'), random_color('font'), random_color('background'), random_color('font'),random_color('background'), random_color('font'),random_color('background'), random_color('font'), random_color('background'), random_color('font'),random_color('background'), random_color('font'))  # border:0px
        widget.setStyleSheet(css)
        widget.setStyleSheet(css)
        btn_alldele = QPushButton('清空')
        btn_alldele.setFixedSize(50,30)
        btn_alldele.clicked.connect(self.btn_alldele_clicked)
        btn_floder = QPushButton('本地')
        btn_floder.clicked.connect(self.lwdt_video_btn_floder_clicked)
        btn_floder.setFixedSize(50,30)
        btn_video_stop = QPushButton('停止')
        btn_video_stop.setFixedSize(50,30)
        btn_video_stop.clicked.connect(self.video_player.stop)
        glayout_widget.addWidget(btn_floder,0,0,1,1)
        glayout_widget.addWidget(btn_alldele,0,2,1,1)
        glayout_widget.addWidget(btn_video_stop,0,1,1,1)
        self.lwdt_video_info.addItem(item)
        self.lwdt_video_info.setItemWidget(item, widget)

        # 初始化界面刷新
        file = "{}\Ico\\video_back.png".format(ROOTDIR)
        item_load = QListWidgetItem()
        item_load.setText(file)
        item_load.setSizeHint(QSize(60,5))
        widhet_load = QWidget()
        widhet_load.setFixedHeight(5)
        widhet_load.setStyleSheet("*{background-color:%s}"%(random_color('background')))
        self.lwdt_video_info.addItem(item_load)
        self.lwdt_video_info.setItemWidget(item_load,widhet_load)
        media = QMediaContent(QUrl.fromLocalFile(file))
        self.video_plist.addMedia(media)


    def __init_userInfo_load(self):
        if os.path.exists(r'{}\Config\userDatas'.format(ROOTDIR)):
            with open(r'{}\Config\userDatas'.format(ROOTDIR),'rb') as video_f:
                datas = pickle.loads(video_f.read())
                if datas:
                    self.user_info_all_dict.update(datas)
                    video_userDatas = self.user_info_all_dict.get('video_userDatas')
                    if video_userDatas:
                        for data in video_userDatas:
                            self.video_plist_additem(data,False,False,True)
                        return
        self.user_info_all_dict['video_userDatas'] = []


    def timer_video_update_timeout(self,*args):
        if self.video_videowidget.isVisible():
            if self.video_plist.currentIndex() > 0:
                if self.video_player.state() == 0 and not self.lwdt_video_info.isVisible() and self.lwdt_video_info_opened and self.video_plist.mediaCount() == 1:
                    self.video_player.play()
                    self.lwdt_video_info_opened = False

                elif self.lwdt_video_info_opened and self.video_player.state() == 0:
                    self.lwdt_video_info_opened = False
                    self.video_plist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
                    self.video_plist.setCurrentIndex(0)
                    self.video_player.play()

            elif self.lwdt_video_info_opened:
                self.lwdt_video_info_opened = False
                self.video_plist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
                self.video_plist.setCurrentIndex(0)
                self.video_player.play()

            else:self.video_player.stop()


        else:
            self.timer_video_update.stop()


    def btn_alldele_clicked(self, p=None):
        """清空列表"""
        warn = QMessageBox.warning(self, '提示','确定清空播放列表？',QMessageBox.Yes|QMessageBox.Cancel,QMessageBox.Cancel)
        # print(warn)
        if warn == 16384:
            self.lwdt_video_info.clear()
            self.video_plist.clear()
            self.__init_lwdt_video_toolBtn()
            self.timer_video_update.start(2000)
            self.user_info_all_dict['video_userDatas'] = []
            with open(r'{}\Config\userDatas'.format(ROOTDIR), 'wb') as fv:
                pickle.dump(self.user_info_all_dict, fv)

    def lwdt_video_additem(self,path):
        """自定义项目添加，需要plistadd调用使用"""
        widget = MWidget(path)
        widget.filename.doubleClicked.connect(self.lwdt_video_info_item_doubleclicked)
        widget.btn_dele.clicked.connect(self.lwdt_video_info_item_dele)
        item = QListWidgetItem()
        item.setText(path)
        item.setSizeHint(QSize(500,30))
        self.lwdt_video_info.addItem(item)
        self.lwdt_video_info.setItemWidget(item, widget)


    @catch_except
    def lwdt_video_info_item_dele(self,p=None,w=True):
        """删除媒体项目"""
        if self.lwdt_video_info_dele_tips:
            warn = QMessageBox.warning(self,'提示','确定要删除?',QMessageBox.Yes|QMessageBox.YesAll|QMessageBox.Cancel)
            #cancel 4194304 yes 16384 yesall 32768
            if warn == 4194304:
                return None
            elif warn == 32768:
                self.lwdt_video_info_dele_tips = False

        index = self.lwdt_video_info.currentRow()
        self.lwdt_video_info.takeItem(index)
        self.video_plist.removeMedia(index-1)
        del self.user_info_all_dict['video_userDatas'][index-2]
        if w:
            with open(r'{}\Config\userDatas'.format(ROOTDIR),'wb') as fv:
                pickle.dump(self.user_info_all_dict,fv)

    def lwdt_video_additem2(self,path):
        """播放列表自定义添加项目，暂时不用，添加操作已在继承QpushButton的MPushButton类中实现"""
        item = QListWidgetItem()
        item.setText(path)
        widget = QWidget()
        glayout_widget = QGridLayout()
        glayout_widget.setSpacing(0)
        glayout_widget.setContentsMargins(0,0,0,0)
        widget.setLayout(glayout_widget)
        widget.setFixedHeight(30)
        btn_dele = QPushButton('删除')
        btn_dele.setFixedSize(60,30)
        btn_dele.setObjectName('dele')
        new_path = path.replace('\\','/')
        name = re.findall('.*/(.*?)$', new_path)
        if name:
            filename = QPushButton(name[0])
        else: filename = QPushButton(path)
        filename.setFixedHeight(30)
        filename.setToolTip('双击播放')
        filename.setObjectName('filename')
        filename.setContentsMargins(0,0,0,0)
        css = "QPushButton:hover{background-color:%s;color:%s}QLable:hover{background-color:%s;color:%s}" \
              "#filename{background-color:%s;color:%s;text-align:left}" \
              "QPushButton:pressed{background-color:%s;color:%s}QLable:pressed{background-color:%s;color:%s}" \
              "QToolTip{background-color:%s;color:%s;font:Yahei;font-size:14px}" % (
              random_color('background'), random_color('font'), random_color('background'), random_color('font'),random_color('background'), random_color('font'),random_color('background'), random_color('font'), random_color('background'), random_color('font'),random_color('background'), random_color('font'))  # border:0px
        widget.setStyleSheet(css)

        glayout_widget.addWidget(btn_dele,0,0,1,1)
        glayout_widget.addWidget(filename,0,1,1,1)

        self.lwdt_video_info.addItem(item)
        self.lwdt_video_info.setItemWidget(item, widget)



    @catch_except
    def lwdt_video_btn_floder_clicked(self,*args):
        """播放列表本地功能实现打开文件夹选择文件操作"""
        files = QFileDialog.getOpenFileNames(self, '选择文件', './', 'AllFile(*)')
        if files:
            files = files[0]
            for file in files:
                self.video_plist_additem(file, False)

    @catch_except
    def lwdt_video_info_item_doubleclicked(self, p=None):
        """播放列表项目双击，实现播放，第一项为永久功能暂用，index与plist相差1"""
        index = self.lwdt_video_info.currentRow()
        if index > 1:
            self.video_plist.setCurrentIndex(index - 1)
            self.video_player.play()



    @catch_except
    def btn_video_pause_clicked(self, *args):
        """暂停继续实现"""
        # self.video_player.stop()
        if self.video_player.state() == 1:
            self.btn_video_pause.setText('继续')
            self.video_player.pause()
        else:
            self.btn_video_pause.setText('暂停')
            self.video_player.play()



    def slider_video_vol_valueChanged(self, p):
        """音量控制控件控制player音量"""
        self.video_player.setVolume(p)

    @catch_except
    def slider_video_process_sliderMoved(self, p):
        """进度条拖动，控制player进度"""
        self.video_player.setPosition(p)

    @catch_except
    def label_propos_textchange(self, p):
        """显示播放进度时间,player-position驱动"""
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
        """player进度改变驱动，设置进度条显示进度和进度时间显示"""
        self.slider_video_process.setValue(p)
        if self.video_plist.currentIndex() > 0:
            self.label_propos_textchange(p)

    @catch_except
    def video_player_stateChanged(self, p):
        """player播放状态改变驱动，改变暂停按钮text，改变top_label_right滚动显示状态"""
        if p == 1:
            self.video_player_durationChanged(p=None) # 重新执行top_label_scroll
            self.btn_video_home_ok.setText('添加')  # ok按钮设置
            self.btn_video_pause.setText('暂停')
            if self.video_plist.currentIndex() > 0 and self.timer_video_update.isActive():
                self.timer_video_update.stop()


        elif self.video_player.state() == 2:
            self.label_top_right.setText('')
            self.btn_video_home_ok.setText('播放') # ok按钮设置
            self.btn_video_pause.setText('继续')
            if self.timer_video_update.isActive() and self.video_plist.currentIndex() > 0:
                self.timer_video_update.stop()

        else:
            self.label_video_proPos.clear()
            self.label_top_right.setText('')
            self.btn_video_pause.setText('')
            self.btn_video_home_ok.setText('播放')  # ok按钮设置
            self.btn_video_pause.setText('')
            self.timer_video_update.start(1000)

    @catch_except
    def video_player_durationChanged(self, p, *args):
        """修改top_label_right_text, 设置进度条范围"""
        if p:
            self.slider_video_process.setRange(0, p)
        index = self.video_plist.currentIndex()
        if index != -1:
            self.lwdt_video_info.setCurrentRow(index + 1) # 更新播放列表显示, 第一项是自定义的，要排除
            filepath = self.lwdt_video_info.currentItem().text()
            filepath = filepath.replace('/', '\\')
            name = re.findall('(.*)\\\\(.*?)$', filepath)
            if name:
                if index != 0:
                    self.label_top_right.setText(name[0][1])
        if index > 0 and self.video_plist.playbackMode() == QMediaPlaylist.CurrentItemInLoop:
            self.video_plist.setPlaybackMode(QMediaPlaylist.Sequential)
        elif index == 0:
            self.label_video_proPos.clear()

    @catch_except
    def video_player_currentMediaChanged(self,*args):
        """修改top_label_right_text"""
        index = self.video_plist.currentIndex()
        filepath = self.video_list[index]
        filepath = filepath.replace('/', '\\')
        name = re.findall('(.*)\\\\(.*?)$', filepath)
        if name:
            self.label_top_right.setText(name[0][1])

    @catch_except
    def video_player_play(self, p=None):
        self.video_player.play()

    @catch_except
    def video_plist_additem(self, p, pl=True,w=True,init=False):
        """与QVideoWidget的dropenterchanged绑定，拽入播放,所有的添加都应该使用此方法 """
        if re.sub('\s','',p):
            if os.path.isfile(p) or os.path.isdir(p):
                filepaths = self.dirs_to_files(p)
                for index, filepath in enumerate(filepaths):
                    self.lwdt_video_additem(filepath)
                    # self.lwdt_video_info.addItem(filepath)
                    self.video_plist.addMedia(QMediaContent(QUrl.fromLocalFile(filepath)))
                    if not init:
                        self.user_info_all_dict['video_userDatas'].append(filepath)
                    if index == 0 and pl:
                        self.video_plist.setCurrentIndex(self.video_plist.mediaCount()-1)
                        self.video_player_play() #E:\Programme\GIT\Python\Others\Exceise\sndn

            else:
                self.lwdt_video_additem(p)
                # self.lwdt_video_info.addItem(p)
                self.video_plist.addMedia(QMediaContent(QUrl(p)))
                if not init:
                    self.user_info_all_dict['video_userDatas'].append(p)
                if pl:
                    self.video_plist.setCurrentIndex(self.video_plist.mediaCount() - 1)
                    self.video_player_play()
            self.video_videowidget.show()
            self.lwdt_video_info.scrollToBottom()  # 滚动到底部
        elif self.video_plist.mediaCount() > 0:
            self.video_player.play()

        else:
            QMessageBox.information(self,'提示','请输入播放文件路径或URL，\n或双击播放列表播放')

        if w:
            with open(r'{}\Config\userDatas'.format(ROOTDIR),'wb') as fv:
                pickle.dump(self.user_info_all_dict,fv)





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
        if self.video_videowidget.isVisible() and not self.lwdt_video_info.isVisible():
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
            if a0.pos().x() > self.width() - 80 and a0.pos().y() > self.height() // 5:
                self.lwdt_video_info.setFixedWidth(self.width() // 4)
                self.lwdt_video_info.setVisible(True)
                self.lwdt_video_info_opened = True

            else:
                self.lwdt_video_info.setVisible(False)
                self.lwdt_video_info.hide()

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


    def mouseDoubleClickEvent_video(self, a0: QtGui.QMouseEvent) -> None:
        if self.video_videowidget.isVisible():
            if a0.button() == Qt.LeftButton:
                if not self.lwdt_video_info.isVisible():
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



    @layout_dele
    def video_home_reload(self,*args):
        """视频播放重载"""
        if func_historys[3]:self.btn_top_forward.setVisible(True)
        else:self.btn_top_forward.setVisible(False)

        for widget in self.video_home_widgets:
            widget.setVisible(True)

        # 初始化界面刷新
        self.lwdt_video_info_opened = True
        self.lwdt_video_info.setVisible(False)  # 默认隐藏播放列表

        if self.__init_video_first:
            self.__init_userInfo_load()
            self.__init_video_first = False
        self.timer_video_update.start(1000)

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


