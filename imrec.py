
from ToolBox.main_ui import *

class Imrec(Ui):
    def __init__(self):
        super(Imrec, self).__init__()

        self.__init_imrec_home()
        self.__init_imrec_child_ui()

        # API实例化
        self.ApiImrec = AipImageClassify(self.APPID, self.APIKEY, self.SECRETKEY)
        # 绑定主页重载函数
        self.btn_home_imgrec.clicked.connect(self.imrec_home_reload)

    def __init_imrec_home(self):
        """图像识别窗口主页"""

        self.glayout_imrec_home = QGridLayout()
        self.glayout_imrec_home.setObjectName('grade_2')
        self.glayout_main.addLayout(self.glayout_imrec_home,2,0,Qt.AlignCenter)
        self.glayout_imrec_home.setSpacing(int(self.width()*0.2/6))
        self.glayout_imrec_home.setContentsMargins(10,10,10,10)

        self.btn_imrec_1 = QPushButton("图像主体检测")
        self.btn_imrec_2 = QPushButton("通用物体和场\n景识别高级版")
        self.btn_imrec_3 = QPushButton("菜品识别")
        self.btn_imrec_4 = QPushButton("自定义菜品\n识别")
        self.btn_imrec_5 = QPushButton("logo商标识别")
        self.btn_imrec_6 = QPushButton("动物识别")
        self.btn_imrec_7 = QPushButton("植物识别")
        self.btn_imrec_8 = QPushButton("果蔬食材识别")
        self.btn_imrec_9 = QPushButton("地标识别")
        self.btn_imrec_10 = QPushButton("红酒识别")
        self.btn_imrec_11 = QPushButton("货币识别")

        self.imrec_home_btns = [self.btn_imrec_1,self.btn_imrec_2,self.btn_imrec_3,self.btn_imrec_4,self.btn_imrec_5,self.btn_imrec_6,self.btn_imrec_7,self.btn_imrec_8,self.btn_imrec_9,self.btn_imrec_10,self.btn_imrec_11]
        h = self.height() * 0.8 / 5
        w = self.width() * 0.8 / 4
        if h > 100: h = 100
        if w > h * 1.3: w = h * 1.3
        if h > w / 1.3: h = w / 1.3
        row, col = 0, 0
        for btn in self.imrec_home_btns:
            css = "*{width:%dpx;height:%spx}" \
                  ":hover{background-color:%s;}" \
                  "QPushButton{background-color:%s;}" \
                  "QPushButton:pressed{background-color:%s;}" \
                  "QToolTip{color:%s;font:Yahei;font-size:14px}" %(w,h,random_color(),random_color(),random_color(),random_color()) # border:0px
            btn.setStyleSheet(css)
            btn.setFixedSize(QSize(w,h ))
            self.glayout_imrec_home.addWidget(btn,row, col ,1, 1)
            btn.setVisible(False)
            col += 1
            if col > 3:
                col = 0
                row += 1

            # 绑定窗口重载
            btn.clicked.connect(self.btn_imrec_home_clicked)


    @layout_dele
    def imrec_home_reload(self,*args):
        """图像识别主页重载"""
        if func_historys[3]:
            self.btn_top_forward.setVisible(True)
        else:
            self.btn_top_forward.setVisible(False)

        for btn in self.imrec_home_btns:
            btn.setVisible(True)

        return self.glayout_imrec_home


    def __init_imrec_child_ui(self, *args):
        """图像识别子窗口布局初始化"""

        self.glayout_imrec_child = QGridLayout()
        self.glayout_imrec_child.setObjectName('grade_3')
        self.glayout_main.addLayout(self.glayout_imrec_child,2,0)

        # 参数区域
        self.glayout_imrec_child_paramms = QGridLayout()
        self.glayout_imrec_child.addLayout(self.glayout_imrec_child_paramms,0,0,Qt.AlignTop)

        # 结果区域
        self.glayout_imrec_child_content = QGridLayout()
        self.glayout_imrec_child.addLayout(self.glayout_imrec_child_content,0,1)

        # 子窗口功能
        self.imrec_child_mode = None
        # 子窗口功能所需参数
        self.imrec_child_params = None

        self.label_imrec_child_title = QLabel() #0
        self.btn_imrec_child_ok = QPushButton("提交") # 1
        self.btn_imrec_child_ok.clicked.connect(self.btn_imrec_child_ok_clicked)
        self.label_imrec_child_option = QLabel('可选参数')# 2
        self.label_imrec_child_option.setAlignment(Qt.AlignCenter)
        self.btn_imrec_child_img = QPushButton('图片') # 3
        self.btn_imrec_child_img.clicked.connect(self.btn_imrec_child_img_clicked)
        self.btn_imrec_child_img.setIcon(QIcon('{}/Ico/floder.png'.format(ROOTDIR)))
        self.lnedit_child_imrec_img = QLineEdit()
        self.label_imrec_child_baike_num = QLabel('百科结果数') #4
        self.spb_imrec_child_baike_num = QSpinBox()
        self.spb_imrec_child_baike_num.setRange(0,10)
        self.label_imrec_child_top_num = QLabel('结果数') #5
        self.spb_imrec_child_top_num = QSpinBox()
        self.spb_imrec_child_top_num.setValue(5)
        self.label_imrec_child_filter_threshold = QLabel('精度') #6
        self.spb_imrec_child_filter_threshold = QSpinBox()
        self.spb_imrec_child_filter_threshold.setRange(0,100)
        self.spb_imrec_child_filter_threshold.setValue(95)
        self.label_imrec_child_with_face = QLabel('是否带人脸')#7
        self.spb_imrec_child_with_face = QSpinBox()
        self.spb_imrec_child_with_face.setRange(0,1)
        self.label_imrec_child_userdef = QLabel('操作')#8
        self.cmbox_imrec_child_userdef = QComboBox()
        userdef = ['自定义菜品-入库','自定义菜品-检索','自定义菜品-删除']
        self.cmbox_imrec_child_userdef.addItems(userdef)
        self.cmbox_imrec_child_userdef.currentTextChanged.connect(self.cmbox_imrec_child_userdef_changed)
        self.label_imrec_child_brief = QLabel('摘要信息')#9
        self.lnedit_imrec_child_brief = QLineEdit()
        self.label_imrec_child_area = QLabel('区域') # 10
        self.lnedit_imrec_child_area = QLineEdit()
        self.label_imrec_child_logo = QLabel('操作')#11
        self.cmbox_imrec_child_logo = QComboBox()
        logo = ['logo商标识别','logo商标识别—添加','logo商标识别—删除']
        self.cmbox_imrec_child_logo.addItems(logo)
        self.cmbox_imrec_child_logo.currentTextChanged.connect(self.cmbox_imrec_child_logo_changed)
        self.label_imrec_child_custom_lib = QLabel('只检索子库') #12
        self.cmbox_imrec_child_custom_lib = QComboBox()
        self.cmbox_imrec_child_custom_lib.addItems(['false','true'])




        self.imrec_child_widgets = [[self.label_imrec_child_title], [self.btn_imrec_child_ok], [self.label_imrec_child_option],
                                    [self.btn_imrec_child_img,self.lnedit_child_imrec_img], [self.label_imrec_child_baike_num,self.spb_imrec_child_baike_num],
                                    [self.label_imrec_child_top_num,self.spb_imrec_child_top_num],[self.label_imrec_child_filter_threshold,self.spb_imrec_child_filter_threshold],
                                    [self.label_imrec_child_with_face,self.spb_imrec_child_with_face],[self.label_imrec_child_userdef,self.cmbox_imrec_child_userdef],
                                    [self.label_imrec_child_brief,self.lnedit_imrec_child_brief],[self.label_imrec_child_area,self.lnedit_imrec_child_area],
                                    [self.label_imrec_child_logo,self.cmbox_imrec_child_logo],[self.label_imrec_child_custom_lib,self.cmbox_imrec_child_custom_lib],
                                    ]




    def btn_imrec_home_clicked(self, *args):
        """主页按钮点击触发子窗口重载函数，与FORWARB调用函数分离，防止sender重写，导致forward失效"""
        self.imrec_child_mode = self.sender().text().replace('\n', '')
        self.imrec_child_reload()


    @layout_dele
    def imrec_child_reload(self, *args):
        """图像识别子窗口重载"""

        # 更新forward btn
        if func_historys[4]:
            self.btn_top_forward.setVisible(True)
        else:
            self.btn_top_forward.setVisible(False)

        mode = self.imrec_child_mode
        self.label_imrec_child_title.setText(mode)

        self.imrec_child_params = []
        if mode in ['通用物体和场景识别高级版','植物识别','果蔬食材识别']:
            self.imrec_child_params = [0,3,4,1]

        elif mode == 'logo商标识别':
            self.imrec_child_params = [0,11,3,9,12,1]

        elif mode == '菜品识别':
            self.imrec_child_params = [0,3,5,6,4,1]

        elif mode in ['图像主体检测']:
            self.imrec_child_params = [0,3,7,1]
        elif mode == '自定义菜品识别':
            self.imrec_child_params = [0,8,3,2,9,1]
        elif mode in ['动物识别','车型识别']:
            self.imrec_child_params = [0,3,5,4,1]
        elif mode in ['地标识别','红酒识别','货币识别']:
            self.imrec_child_params = [0,3,1]

        elif mode in ['车辆检测']:
            self.imrec_child_params = [0,3,10,1]

        if self.imrec_child_params:
            for index, i in enumerate(self.imrec_child_params):
                widgets = self.imrec_child_widgets[i]
                for j, widget in enumerate(widgets):
                    widget.setVisible(True)
                    css = "*{background-color:%s;color:%s;border:0;height:25px;font:YaHei;} :pressed{background-color:%s;color:%s;}" % (
                            random_color(mode='background'), random_color(mode='font'), random_color(mode='background'),
                            random_color(mode='font'))
                    widget.setStyleSheet(css)
                    if widget.__doc__.startswith('QLabel'):
                        widget.setAlignment(Qt.AlignCenter)
                    elif widget.__doc__.startswith('QLineEdit'):
                        widget.setClearButtonEnabled(True)
                    if len(widgets) == 1:
                        widget.setFixedHeight(25)
                        self.glayout_imrec_child_paramms.addWidget(widget, index, 0, 1, 2)
                        continue
                    elif j == 0:
                        widget.setFixedWidth(80)
                    else:
                        w = self.width() // 3
                        if w > 300: w = 300
                        widget.setFixedWidth(w)



                    self.glayout_imrec_child_paramms.addWidget(widget, index, j, 1, 1)


        self.txedit_imrec_child_content = QTextEdit()
        self.glayout_imrec_child_content.addWidget(self.txedit_imrec_child_content, 0, 0, 1, 1)
        self.txedit_imrec_child_content.setStyleSheet(
            "*{background-color:%s;color:%s;border:0;height:25px;width:80px;font:YaHei;} :pressed{background-color:%s;color:%s;}" % (
                random_color(mode='background'), random_color(mode='font'), random_color(mode='background'),
                random_color(mode='font')))

        if mode == 'logo商标识别':
            self.label_imrec_child_brief.setVisible(False)
            self.lnedit_imrec_child_brief.setVisible(False)

        return self.glayout_imrec_child

    @catch_except
    def btn_imrec_child_ok_clicked(self,*args):
        """获取参数，访问接口，调用结果处理函数"""

        mode = self.imrec_child_mode
        self.label_status_left.setText(mode)

        result = None
        others = {}

        if mode in ['通用物体和场景识别高级版','植物识别','果蔬食材识别']:
            filepath = self.lnedit_child_imrec_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self,'提示','图片不存在',QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath),'rb').read()
            baike_num = str(self.spb_imrec_child_baike_num.value())
            option = {'baike_num':baike_num}
            if mode == '通用物体和场景识别高级版':
                result = self.ApiImrec.advancedGeneral(image, option)
            elif mode == '植物识别':
                result = self.ApiImrec.plantDetect(image, option)
            elif mode == '果蔬食材识别':
                result = self.ApiImrec.ingredient(image, option)

        elif mode in ['菜品识别']:
            filepath = self.lnedit_child_imrec_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()
            baike_num = str(self.spb_imrec_child_baike_num.value())
            top_num = str(self.spb_imrec_child_top_num.value())
            filter_threshold = str(self.spb_imrec_child_filter_threshold.value()/100)
            option = {'baike_num': baike_num, 'filter_threshold':filter_threshold, 'top_num':top_num}
            result = self.ApiImrec.dishDetect(image, option)
        elif mode in ['图像主体检测']:
            filepath = self.lnedit_child_imrec_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()
            with_face = self.spb_imrec_child_with_face.text()
            option = {"with_face":with_face}
            result = self.ApiImrec.objectDetect(image, option)

        elif mode == '自定义菜品识别':
            action = self.cmbox_imrec_child_userdef.currentText()
            if action == '自定义菜品-入库':
                filepath = self.lnedit_child_imrec_img.text()
                if not filepath.endswith(','):filepath += ','
                brief = self.lnedit_imrec_child_brief.text()
                if brief:
                    if not brief.endswith(','): brief += ','
                    briefs = re.findall('(.*?),', brief)
                else:briefs = []
                filepaths = re.findall('(.*?),',filepath)
                while len(briefs) < len(filepaths):
                    # 补全BRIEF
                    rand = time.strftime('%Y%m%d%H%M%S', time.localtime()) + str(random.randint(11,99))
                    briefs.append(rand)
                result = []
                for brief, filepath in zip(briefs, filepaths):
                    if not os.path.isfile(filepath):
                        QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                        return None
                    image = open(r'{}'.format(filepath), 'rb').read()
                    option = {}
                    if brief: option = {'brief':brief}
                    result.append(self.ApiImrec.dishadd(image, option))
                    result.append('\n')
            elif action == '自定义菜品-检索':
                filepath = self.lnedit_child_imrec_img.text()
                if not filepath.endswith(','): filepath += ','
                filepaths = re.findall('(.*?),', filepath)
                result = []
                for filepath in filepaths:
                    if not os.path.isfile(filepath):
                        QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                        return None
                    image = open(r'{}'.format(filepath), 'rb').read()
                    result.append(self.ApiImrec.dishsearch(image))
                    result.append('\n')
            elif action == '自定义菜品-删除':
                filepath = self.lnedit_child_imrec_img.text()
                if not filepath.endswith(','):filepath += ','
                filepaths = re.findall('(.*?),',filepath)
                result = []
                for filepath in filepaths:
                    if os.path.isfile(filepath):
                        image = base64.b64encode(open(r'{}'.format(filepath), 'rb').read()).decode()
                        option = {'image':image}
                    else:
                        cont_sign = filepath
                        option = {'cont_sign':cont_sign}
                    result.append(self.ApiImrec.dishdelete(option))
                    result.append('\n')

        elif mode in ['动物识别','车型识别']:
            filepath = self.lnedit_child_imrec_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()
            baike_num = str(self.spb_imrec_child_baike_num.value())
            top_num = str(self.spb_imrec_child_top_num.value())
            option = {'baike_num': baike_num, 'top_num':top_num}
            if mode == '动物识别':
                result = self.ApiImrec.animalDetect(image, option)
            elif mode == '车型识别':
                result = self.ApiImrec.carDetect(image, option)


        elif mode in ['地标识别','红酒识别','货币识别']:
            filepath = self.lnedit_child_imrec_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()
            if mode == '地标识别':
                result = self.ApiImrec.landmark(image)
            elif mode == '红酒识别':
                result = self.ApiImrec.redwine(image)
            elif mode == '货币识别':
                result = self.ApiImrec.currency(image)

        elif mode in ['车辆检测']:
            filepath = self.lnedit_child_imrec_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()
            area = self.lnedit_imrec_child_area.text()
            option = {'area': area}
            result = self.ApiImrec.carDetect(image, option)

        elif mode == 'logo商标识别': # 未授权
            action = self.cmbox_imrec_child_logo.currentText()

            if action == 'logo商标识别':
                filepath = self.lnedit_child_imrec_img.text()
                if not os.path.isfile(filepath):
                    QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                    return None
                image = open(r'{}'.format(filepath), 'rb').read()
                custom_lib = self.cmbox_imrec_child_custom_lib.currentText()
                option = {'custom_lib': custom_lib}
                result = self.ApiImrec.logoSearch(image, option)
            elif action == 'logo商标识别—添加':
                filepath = self.lnedit_child_imrec_img.text()
                if not os.path.isfile(filepath):
                    QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                    return None
                image = open(r'{}'.format(filepath), 'rb').read()
                brief = self.lnedit_imrec_child_brief.text()
                option = {'brief': brief}
                result = self.ApiImrec.logoAdd(image, option)
            elif action == 'logo商标识别—删除':
                filepath = self.lnedit_child_imrec_img.text()
                option = {}
                if os.path.isfile(filepath):
                    image = base64.b64encode(open(r'{}'.format(filepath), 'rb').read()).decode()
                    option = {'image':image}
                else:
                    option = {'cont_sign': filepath}
                result = self.ApiImrec.logoDelete(option)

        self.imrec_child_result_deal(mode,result, others)

    def imrec_child_result_deal(self, mode, datas, option=None, *args):
        """数据处理"""
        content = '{} --> 完成\n'.format(mode)
        content = self.dict_get_value(datas,content)
        self.txedit_imrec_child_content.setText(content)


    def cmbox_imrec_child_logo_changed(self,*args):
        action = self.cmbox_imrec_child_logo.currentText()
        if action == 'logo商标识别':
            self.cmbox_imrec_child_custom_lib.setVisible(True)
            self.label_imrec_child_custom_lib.setVisible(True)
        else:
            self.cmbox_imrec_child_custom_lib.setVisible(False)
            self.label_imrec_child_custom_lib.setVisible(False)
        if action == 'logo商标识别—添加':
            self.lnedit_imrec_child_brief.setVisible(True)
            self.label_imrec_child_brief.setVisible(True)
        else:
            self.lnedit_imrec_child_brief.setVisible(False)
            self.label_imrec_child_brief.setVisible(False)
        if action == 'logo商标识别-删除':
            if not self.lnedit_child_imrec_img.text():
                self.lnedit_child_imrec_img.setText('图片或者图片签名(cont_sign)')



    def btn_imrec_child_img_clicked(self, *args):
        file = QFileDialog.getOpenFileName(self,'选择图片',"./","All File(*);;png(*.png);;jpeg(*.jpeg);;jpg(*.jpg);;bmp(*.bmp)")
        if file[0]:
            self.lnedit_child_imrec_img.setText(file[0])


    def cmbox_imrec_child_userdef_changed(self, *args):
        name = self.cmbox_imrec_child_userdef.currentText()
        if name == '自定义菜品-删除':
            if not self.lnedit_child_imrec_img.text():
                self.lnedit_child_imrec_img.setText('图片或者图片签名(cont_sign)')
        else:
            if self.lnedit_child_imrec_img.text() == '图片或者图片签名(cont_sign)':
                self.lnedit_child_imrec_img.setText("")
        if name == '自定义菜品-入库':
            self.lnedit_imrec_child_brief.setVisible(True)
            self.label_imrec_child_brief.setVisible(True)
            self.label_imrec_child_option.setVisible(True)
        else:
            self.lnedit_imrec_child_brief.setVisible(False)
            self.label_imrec_child_brief.setVisible(False)
            self.label_imrec_child_option.setVisible(False)

    def resizeEvent_imrec(self, a0: QtGui.QResizeEvent) -> None:
        value = int(self.width()*0.2 /6)
        self.glayout_imrec_home.setSpacing(value)
        pass