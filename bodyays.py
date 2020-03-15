from PyQt5.QtGui import QImage

from ToolBox.main_ui import *

class Body(Ui):
    def __init__(self):
        super(Body, self).__init__()
        self.__init_body_ui()
        self.__init_dody_child_ui()
        self.btn_home_bodyays.clicked.connect(self.__body_home_reload)
        self.ApiBody = AipBodyAnalysis(self.APPID, self.APIKEY, self.SECRETKEY)

    def __init_body_ui(self,*args):
        """人体分析主页"""
        self.glayout_body_home = QGridLayout()
        self.glayout_main.addLayout(self.glayout_body_home, 2, 0, Qt.AlignCenter)
        self.glayout_body_home.setObjectName('grade_2')

        self.btn_body_home_1 = QPushButton()
        self.btn_body_home_2 = QPushButton()
        self.btn_body_home_3 = QPushButton()
        self.btn_body_home_4 = QPushButton()
        self.btn_body_home_5 = QPushButton()
        self.btn_body_home_6 = QPushButton()
        self.btn_body_home_7 = QPushButton()
        self.btn_body_home_8 = QPushButton()
        self.btn_body_home_9 = QPushButton()

        self.body_home_btns = [[self.btn_body_home_1, "人体关键点\n识别"],[self.btn_body_home_2, "人体检测和\n属性识别"],[self.btn_body_home_3, "人流量统计"],[self.btn_body_home_4, "手势识别"],[self.btn_body_home_5, "人像分割"],[self.btn_body_home_6, "驾驶行为分析"],[self.btn_body_home_7, "人流量统计\n（动态版）"],[self.btn_body_home_8, "手部关键点\n识别（邀测）"],[self.btn_body_home_9, "危险行为识别\n（邀测）"],]

        self.glayout_body_home.setSpacing(int(self.width()*0.2/6))
        self.glayout_body_home.setContentsMargins(10,10,10,10)
        h = self.height() * 0.8 / 6
        w = self.width() * 0.8 / 5
        if h > 100: h = 100
        if w > h * 1.3: w = h * 1.3
        if h > w / 1.3: h = w / 1.3
        row,col = 0,0
        for btn in self.body_home_btns:
            self.glayout_body_home.addWidget(btn[0],row,col,1,1)
            btn[0].setText(btn[1])
            css = "*{width:%dpx;height:%spx}" \
                  ":hover{background-color:%s;}" \
                  "QPushButton{background-color:%s;}" \
                  "QPushButton:pressed{background-color:%s;}" \
                  "QToolTip{color:%s;font:Yahei;font-size:14px}" %(w,h,random_color(),random_color(),random_color(),random_color()) # border:0px
            #background-color:%s; random_color(),
            btn[0].setStyleSheet(css)
            btn[0].clicked.connect(self.body_home_btn_clicked)
            btn[0].setVisible(False)
            # btn[0].setFixedSize(QSize(h*1.3,h ))

            col += 1
            if col > 3:
                col = 0
                row += 1

    @layout_dele
    def __body_home_reload(self,*args):
        for btn in self.body_home_btns:
            btn[0].setVisible(True)

        return self.glayout_body_home

    @catch_except
    def body_home_btn_clicked(self, *args):
        """人体分析主页btn点击"""
        # 监听按下的键名
        self.body_child_mode = self.sender().text()

        # 人体分析窗口重载
        self.body_child_reload()



    def __init_dody_child_ui(self,*args):
        """人体分析子窗口控件初始化"""
        self.glayout_body_child = QGridLayout()
        self.glayout_body_child.setObjectName('grade_3')
        self.glayout_main.addLayout(self.glayout_body_child, 2, 0)



        # 内容布局
        self.glayout_body_child_content = QGridLayout()
        self.glayout_body_child.addLayout(self.glayout_body_child_content,0,1)


        # 参数布局
        self.glayout_body_child_params = QGridLayout()
        self.glayout_body_child.addLayout(self.glayout_body_child_params,0,0,Qt.AlignTop)
        self.label_body_child_title = QLabel() # 0
        self.btn_body_child_ok = QPushButton()
        self.btn_body_child_ok.setText('提交') # 1
        self.btn_body_child_ok.clicked.connect(self.btn_body_child_ok_clicked)
        self.btn_body_child_floder = QPushButton()
        self.btn_body_child_floder.setText('图片')
        self.btn_body_child_floder.clicked.connect(self.btn_body_child_floder_clicked)
        self.btn_body_child_floder.setIcon(QIcon('{}/Ico/floder.png'.format(ROOTDIR))) #2
        self.lnedit_body_child_img = MLineEdit()
        self.label_body_child_option = QLabel()
        self.label_body_child_option.setText('可选参数') # 3
        self.label_body_child_type = QLabel()
        self.label_body_child_type.setText('类型') #4
        self.lnedit_body_child_type = MLineEdit()
        self.lnedit_body_child_type.setToolTip('labelmap: 二值图像 ,scoremap:人像前景灰度图 ,foreground:人像前景抠图,多选逗号分隔')
        self.label_body_child_area = QLabel()
        self.label_body_child_area.setText('区域') # 5
        self.lnedit_body_child_area = MLineEdit()
        self.label_body_child_show = QLabel()
        self.label_body_child_show.setText('输出图片') # 6
        self.cmbox_body_child_show = QComboBox()
        self.cmbox_body_child_show.addItems(['false','true'])
        self.label_body_child_dynamic = QLabel()
        self.label_body_child_dynamic.setText('动态人流量') #7
        self.cmbox_body_child_dynamic = QComboBox()
        self.cmbox_body_child_dynamic.addItems(['false','true'])
        self.label_body_child_case_id = QLabel()
        self.label_body_child_case_id.setText('任务ID') # 8
        self.lnedit_body_child_case_id = MLineEdit()
        self.label_body_child_case_init = QLabel()
        self.label_body_child_case_init.setText('初始化信号') # 9
        self.cmbox_body_child_case_init = QComboBox()
        self.cmbox_body_child_case_init.addItems(['true','false'])
        self.btn_body_child_floderdata = QPushButton()
        self.btn_body_child_floderdata.setText('视频')
        self.btn_body_child_floderdata.clicked.connect(self.btn_body_child_floderdata_clicked)
        self.btn_body_child_floderdata.setIcon(QIcon('{}/Ico/floder.png'.format(ROOTDIR))) #10
        self.lnedit_body_child_data = MLineEdit()





        self.body_child_widgets = [[self.label_body_child_title],[self.btn_body_child_ok],[self.btn_body_child_floder,self.lnedit_body_child_img],
                                   [self.label_body_child_option],[self.label_body_child_type,self.lnedit_body_child_type],
                                   [self.label_body_child_area,self.lnedit_body_child_area],[self.label_body_child_show,self.cmbox_body_child_show],
                                   [self.label_body_child_dynamic,self.cmbox_body_child_dynamic],[self.label_body_child_case_id,self.lnedit_body_child_case_id],
                                   [self.label_body_child_case_init,self.cmbox_body_child_case_init],[self.btn_body_child_floderdata,self.lnedit_body_child_data]]

        for widgets in self.body_child_widgets:
            for widget in widgets:

                widget.setVisible(False)

    @layout_dele
    def body_child_reload(self,*args):
        """人体分析子窗口布局管理"""

        # 更新forward btn
        if func_historys[4]:
            self.btn_top_forward.setVisible(True)
        else:
            self.btn_top_forward.setVisible(False)

        mode = self.body_child_mode.replace('\n','')
        # 加载窗口参数
        self.body_child_params = None
        if mode == '人像分割':
            self.label_body_child_title.setText(mode)
            self.body_child_params = [0,2,4,1]
            self.lnedit_body_child_type.setText('labelmap,scoremap,foreground')
        elif mode == '驾驶行为分析':
            self.label_body_child_title.setText(mode)
            self.body_child_params = [0,2,4,1]
            self.lnedit_body_child_type.setText('smoke,cellphone,not_buckling_up,both_hands_leaving_wheel,not_facing_front')
        elif mode == '人流量统计':
            self.label_body_child_title.setText(mode)
            self.body_child_params = [0,2,5,6,1]

        elif mode == '人流量统计（动态版）':
            self.label_body_child_title.setText(mode)
            self.body_child_params = [0,2,7,8,9,5,6,1]

        elif mode in ['人体关键点识别', '手势识别','手部关键点识别（邀测）']:
            self.label_body_child_title.setText(mode)
            self.body_child_params = [0,2,1]

        elif mode == '人体检测和属性识别':
            self.label_body_child_title.setText(mode)
            self.body_child_params = [0,2,1]
            self.lnedit_body_child_type.setText('gender,age,lower_wear,upper_wear,headwear,glasses,upper_color,lower_color,cellphone,upper_wear_fg,upper_wear_texture,lower_wear_texture,orientation,umbrella,bag,smoke,vehicle,carrying_item,upper_cut,lower_cut,occlusion,is_human')
        elif mode == '危险行为识别（邀测）':
            self.label_body_child_title.setText(mode)
            self.body_child_params = [0,10,1]

        else:
            QMessageBox.warning(self,'提示','尚未开发...')
            return self.glayout_body_child

        # 子窗口控件重载
        if self.body_child_params:
            for index,i in enumerate(self.body_child_params):
                widget = self.body_child_widgets[i]
                widget[0].setVisible(True)
                # 文字居中
                if widget[0].__doc__.startswith('QLabel'):
                    widget[0].setAlignment(Qt.AlignCenter)

                if widget[0] == self.btn_body_child_ok:
                    self.glayout_body_child_params.addWidget(widget[0],index,0,1,2)
                    widget[0].setStyleSheet(
                        "*{background-color:%s;color:%s;border:0;height:25px;font:YaHei;} :pressed{background-color:%s;color:%s;}" % (
                        random_color(mode='background'), random_color(mode='font'), random_color(mode='background'),
                        random_color(mode='font')))
                    continue
                if widget[0] in [self.label_body_child_title,self.label_body_child_option]:
                    self.glayout_body_child_params.addWidget(widget[0],index,0,1,2)
                    widget[0].setStyleSheet("*{background-color:%s;color:%s;border:0;font:YaHei;} :pressed{background-color:%s;color:%s;}"%(random_color(mode='background'),random_color(mode='font'),random_color(mode='background'),random_color(mode='font')))
                    widget[0].setFixedHeight(25)
                    continue
                self.glayout_body_child_params.addWidget(widget[0],index,0,1,1)
                widget[0].setFixedWidth(80)
                widget[0].setStyleSheet("*{background-color:%s;color:%s;border:0;height:25px;font:YaHei;} :pressed{background-color:%s;color:%s;}"%(random_color(mode='background'),random_color(mode='font'),random_color(mode='background'),random_color(mode='font')))
                if widget[0].__doc__.startswith('QLabel'):

                    widget[0].setWordWrap(True)
                if len(widget) > 1:
                    widget[1].setVisible(True)

                    widget[1].setStyleSheet("*{background-color:%s;color:%s;border:0;height:25px;width:80px;font:YaHei;} :pressed{background-color:%s;color:%s;}"%(random_color(mode='background'),random_color(mode='font'),random_color(mode='background'),random_color(mode='font')))
                    self.glayout_body_child_params.addWidget(widget[1],index,1,1,1)
                    w = self.width() // 3
                    if w > 300: w = 300
                    widget[1].setFixedWidth(w)

                if widget[1].__doc__.startswith('MLineEdit'):
                    widget[1].setClearButtonEnabled(True)

        self.txedit_body_child_content = QTextEdit()
        self.glayout_body_child_content.addWidget(self.txedit_body_child_content,0,0,1,3)
        self.txedit_body_child_content.setStyleSheet(
            "*{background-color:%s;color:%s;border:0;height:25px;width:80px;font:YaHei;} :pressed{background-color:%s;color:%s;}" % (
            random_color(mode='background'), random_color(mode='font'), random_color(mode='background'),
            random_color(mode='font')))


        return self.glayout_body_child

    @catch_except
    def btn_body_child_ok_clicked(self,*args):
        """人体分析数据获取，访问API"""

        mode = self.body_child_mode.replace('\n','')
        result = None

        if mode == '人像分割':
            image = self.lnedit_body_child_img.text()
            if not os.path.isfile(image):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(image), 'rb').read()
            type_ = self.lnedit_body_child_type.text()
            option = {'type':type_} if type_ else None

            result = self.ApiBody.bodySeg(image, option)

        elif mode == '驾驶行为分析':
            image = self.lnedit_body_child_img.text()
            if not os.path.isfile(image):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(image), 'rb').read()
            type_ = self.lnedit_body_child_type.text()
            option = {'type':type_} if type_ else None

            result = self.ApiBody.driverBehavior(image, option)

        elif mode == '人流量统计':
            image = self.lnedit_body_child_img.text()
            if not os.path.isfile(image):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(image), 'rb').read()
            area = self.lnedit_body_child_area.text()
            show = self.cmbox_body_child_show.currentText()
            option = {}
            if area :option.update({'area':area})
            if show: option.update({'show':show})

            result = self.ApiBody.bodyNum(image, option)

        elif mode == '人流量统计（动态版）':
            image = self.lnedit_body_child_img.text()
            if not os.path.isfile(image):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(image), 'rb').read()

            dynamic = self.cmbox_body_child_dynamic.currentText()
            case_id = self.lnedit_body_child_case_id.text()
            case_init = self.cmbox_body_child_case_init.currentText()
            if dynamic == 'true':
                if not case_id:
                    QMessageBox.warning(self,'提示','请输入任务ID')
                    return None

            area = self.lnedit_body_child_area.text()
            show = self.cmbox_body_child_show.currentText()
            option = {}
            if area :option.update({'area':area})
            if show: option.update({'show':show})
            if case_id:option.update({'case_id':case_id})
            option.update({'case_init':case_init})

            result = self.ApiBody.bodyTracking(image, dynamic, option)

        elif mode in ['人体关键点识别','人体检测和属性识别','手部关键点识别（邀测）','手势识别']:
            image = self.lnedit_body_child_img.text()
            if not os.path.isfile(image):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(image), 'rb').read()
            if mode == '人体检测和属性识别':
                result = self.ApiBody.bodyAttr(image)
            elif mode == '人体关键点识别':
                result = self.ApiBody.bodyAnalysis(image)
            elif mode == '手势识别':
                result = self.ApiBody.gesture(image)
            elif mode == '手部关键点识别（邀测）':
                result = self.ApiBody.hand_analysis(image)

        elif mode == '危险行为识别（邀测）':
            data = self.lnedit_body_child_data.text()
            if not os.path.isfile(data):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            data = open(r'{}'.format(data), 'rb').read()
            result = self.ApiBody.body_danger(data)


        self.body_child_result_deal(mode, result)

    @catch_except
    def body_child_result_deal(self, mode, datas, *args):
        """数据处理"""
        # print(datas)
        if mode == '人像分割':
            labelmap = datas.get('labelmap')
            scoremap = datas.get('scoremap')
            foreground = datas.get('foreground')
            content = '人像分割完成\n结果路径:\n'
            images = []
            name = time.strftime('%H%M%S', time.localtime())
            if foreground:
                _path = r'{}/Record/Img/BodySeg/foreground{}.png'.format(ROOTDIR,name)
                open(_path,'wb').write(base64.b64decode(foreground))
                images.append(_path)

            if scoremap:
                _path = r'{}/Record/Img/BodySeg/scoremap{}.png'.format(ROOTDIR,name)
                open(_path,'wb').write(base64.b64decode(scoremap))
                images.append(_path)
            if labelmap:
                _path = r'{}/Record/Img/BodySeg/labelmap{}.png'.format(ROOTDIR,name)
                open(_path,'wb').write(base64.b64decode(labelmap))
                images.append(_path)

            for image in images:
                content += '  ' + image + '\n'

            self.txedit_body_child_content.setText(content)


        else:
            content = '{} --> 完成\n'.format(mode)
            content = self.dict_get_value(datas,content)
            self.txedit_body_child_content.setText(str(content))


    def btn_body_child_floder_clicked(self,*args):
        file = QFileDialog.getOpenFileName(self,'选择图片',"./","All File(*);;png(*.png);;jpeg(*.jpeg);;jpg(*.jpg);;bmp(*.bmp)")
        if file[0]:
            self.lnedit_body_child_img.setText(file[0])

    def btn_body_child_floderdata_clicked(self, *args):
        file = QFileDialog.getOpenFileName(self,'选择视频',"./","All File(*)")
        if file[0]:
            self.lnedit_body_child_data.setText(file[0])

    def resizeEvent_body(self, a0: QtGui.QResizeEvent) -> None:
        value = int(self.width()*0.2 /6)
        self.glayout_body_home.setSpacing(value)
        pass
