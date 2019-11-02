from ToolBox.main_ui import *


class Ocr(Ui):
    def __init__(self):
        super(Ocr,self).__init__()
        self.__ocr_home_ui()
        self.__ocr_child_ui()

        # 票据识别
        self.__init_ocr_child_invoice_ui()
        self.__ocr_invoice_child_ui() # 票据识别子窗口

        # 其他文字识别
        self.__init_ocr_child_other_ui()
        self.__ocr_other_child_ui()
        # 子功能
        self.ocr_child_mode = None
        # 子功能参数
        self.ocr_child_params = []
        # API
        self.Apiocr = AipOcr(self.APPID,self.APIKEY,self.SECRETKEY)

        self.btn_home_ocr.clicked.connect(self.ocr_home_reload)

    def __ocr_home_ui(self,*args):

        self.glayout_ocr_home = QGridLayout()
        self.glayout_main.addLayout(self.glayout_ocr_home, 2, 0, Qt.AlignCenter)
        self.glayout_ocr_home.setObjectName('grade_2')

        self.btn_ocr_home_1 = QPushButton("通用文字识别")
        self.btn_ocr_home_2 = QPushButton("通用文字识别\n（含位置版）")
        self.btn_ocr_home_3 = QPushButton("通用文字识别\n（高精度版）")
        self.btn_ocr_home_4 = QPushButton("通用文字识别\n（高精度含位置版）")
        self.btn_ocr_home_5 = QPushButton("通用文字识别\n（含生僻字版）")
        self.btn_ocr_home_6 = QPushButton("身份证识别")
        self.btn_ocr_home_7 = QPushButton("银行卡识别")
        self.btn_ocr_home_8 = QPushButton("营业执照识别")
        self.btn_ocr_home_9 = QPushButton("名片识别")
        self.btn_ocr_home_10 = QPushButton("护照识别")
        self.btn_ocr_home_11 = QPushButton("港澳通行证\n识别")
        self.btn_ocr_home_12 = QPushButton("台湾通行证\n识别")
        self.btn_ocr_home_13 = QPushButton("户口本识别")
        self.btn_ocr_home_14 = QPushButton("出生医学证明\n识别")
        self.btn_ocr_home_15 = QPushButton("票据车牌文字\n识别")
        self.btn_ocr_home_16 = QPushButton("其他文字识别")
        
        self.ocr_home_btns = [self.btn_ocr_home_1,self.btn_ocr_home_2,self.btn_ocr_home_3,self.btn_ocr_home_4,self.btn_ocr_home_5,self.btn_ocr_home_6,self.btn_ocr_home_7,self.btn_ocr_home_8,self.btn_ocr_home_9,self.btn_ocr_home_10,self.btn_ocr_home_11,self.btn_ocr_home_12,self.btn_ocr_home_13,self.btn_ocr_home_14,self.btn_ocr_home_15,self.btn_ocr_home_16]
        
        self.glayout_ocr_home.setSpacing(int(self.width()*0.2/6))
        self.glayout_ocr_home.setContentsMargins(10,10,10,10)
        h = self.height() * 0.8 / 6
        w = self.width() * 0.8 / 5
        if h > 100: h = 100
        if w > h * 1.3: w = h * 1.3
        if h > w / 1.3: h = w / 1.3
        row,col = 0,0
        for btn in self.ocr_home_btns:
            self.glayout_ocr_home.addWidget(btn,row,col,1,1)
            css = "*{width:%dpx;height:%spx}" \
                  ":hover{background-color:%s;}" \
                  "QPushButton{background-color:%s;}" \
                  "QPushButton:pressed{background-color:%s;}" \
                  "QToolTip{color:%s;font:Yahei;font-size:14px}" %(w,h,random_color(),random_color(),random_color(),random_color()) # border:0px
            btn.setStyleSheet(css)
            btn.clicked.connect(self.ocr_home_btns_clicked)
            btn.setVisible(False)
            col += 1
            if col > 4:
                col = 0
                row += 1

    @layout_dele
    def ocr_home_reload(self,*args):
        """文字识别主页重载"""
        if func_historys[3]:
            self.btn_top_forward.setVisible(True)
        else:
            self.btn_top_forward.setVisible(False)

        for btn in self.ocr_home_btns:
            btn.setVisible(True)

        return self.glayout_ocr_home

    def ocr_home_btns_clicked(self,*args):
        """主页btn点击，进入对应子功能界面，监听主页按键name,设置子窗口功能参数,调用子窗口重载函数"""
        # 更新forward btn
        if func_historys[4]:
            self.btn_top_forward.setVisible(True)
        else:
            self.btn_top_forward.setVisible(False)
        self.ocr_child_mode = self.sender().text().replace('\n','')
        if self.ocr_child_mode == '票据车牌文字识别':
            self.ocr_invoice_home_reload()
        elif self.ocr_child_mode == '其他文字识别':
            self.ocr_other_home_reload()
        else:
            self.ocr_child_reload()




    def __ocr_child_ui(self, *args):
        """功能窗口控件初始化"""
        self.glayout_ocr_child = QGridLayout()
        self.glayout_ocr_child.setObjectName('grade_3')
        self.glayout_main.addLayout(self.glayout_ocr_child, 2, 0)

        # 参数
        self.glayout_ocr_child_params = QGridLayout()
        self.glayout_ocr_child.addLayout(self.glayout_ocr_child_params,0,0,Qt.AlignTop)

        # 结果
        self.glayout_ocr_child_content = QGridLayout()
        self.glayout_ocr_child.addLayout(self.glayout_ocr_child_content,0,1)

        self.label_ocr_child_title = QLabel() #0
        self.btn_ocr_child_ok = QPushButton('提交')#1
        self.btn_ocr_child_ok.clicked.connect(self.btn_ocr_child_ok_clicked)
        self.label_ocr_child_option = QLabel('可选参数')#2
        self.btn_ocr_child_img = QPushButton('图片')#3
        self.btn_ocr_child_img.clicked.connect(self.btn_ocr_child_img_clicked)
        self.lnedit_ocr_child_img = MLineEdit()
        self.label_ocr_child_lan = QLabel('语言')# 4
        self.cmbox_ocr_child_lan = QComboBox()
        lans = ['中英','英文','葡萄牙语','法语','德语','意大利语','西班牙语','俄语','日语','韩语']
        self.ocr_child_lan_dict = {'中英':'CHN_ENG','英文':'ENG','葡萄牙语':"POR",'法语':"FRE",'德语':"GER",'意大利语':"ITA",'西班牙语':"SPA",'俄语':"RUS",'日语':"JAP",'韩语':"KOR"}
        self.cmbox_ocr_child_lan.addItems(lans)
        self.label_ocr_child_detect_direction = QLabel('朝向检测')#5
        self.cmbox_ocr_child_detect_direction = QComboBox()
        self.cmbox_ocr_child_detect_direction.addItems(['false','true'])
        self.label_ocr_child_detect_lan = QLabel('语言检测')#6
        self.cmbox_ocr_child_detect_lan = QComboBox()
        self.cmbox_ocr_child_detect_lan.addItems(['false','true'])
        self.label_ocr_child_probability = QLabel('返回置信度') # 7
        self.cmbox_ocr_child_probability = QComboBox()
        self.cmbox_ocr_child_probability.addItems(['false','true'])
        self.label_ocr_child_rec_gran = QLabel('字符位置') #8
        self.cmbox_ocr_child_rec_gran = QComboBox()
        self.cmbox_ocr_child_rec_gran.addItems(['false','true'])
        self.label_ocr_child_vertexes_location = QLabel('外接多边形') #9
        self.cmbox_ocr_child_vertexes_location = QComboBox()
        self.cmbox_ocr_child_vertexes_location.addItems(['false','true'])
        self.label_ocr_child_return_type = QLabel('返回类型')# 10
        self.cmbox_ocr_child_return_type = QComboBox()
        self.cmbox_ocr_child_return_type.addItems(['DESC','TEXT','ALL'])
        self.label_ocr_child_id_card_side = QLabel('正反面')#11
        self.cmbox_ocr_child_id_card_side = QComboBox()
        self.cmbox_ocr_child_id_card_side.addItems(['front','back'])
        self.label_ocr_child_detect_risk = QLabel("风险类型")#12
        self.cmbox_ocr_child_detect_risk = QComboBox()
        self.cmbox_ocr_child_detect_risk.addItems(['false','true'])
        self.label_ocr_child_accuracy = QLabel('精度')#13
        self.cmbox_ocr_child_accuracy = QComboBox()
        self.cmbox_ocr_child_accuracy.addItems(['normal','high'])


        

        self.ocr_child_widgets = [[self.label_ocr_child_title], [self.btn_ocr_child_ok], [self.label_ocr_child_option],
                                [self.btn_ocr_child_img,self.lnedit_ocr_child_img], [self.label_ocr_child_lan,self.cmbox_ocr_child_lan],
                                [self.label_ocr_child_detect_direction,self.cmbox_ocr_child_detect_direction], [self.label_ocr_child_detect_lan,self.cmbox_ocr_child_detect_lan],
                                [self.label_ocr_child_probability,self.cmbox_ocr_child_probability],[self.label_ocr_child_rec_gran,self.cmbox_ocr_child_rec_gran],
                                [self.label_ocr_child_vertexes_location,self.cmbox_ocr_child_vertexes_location],[self.label_ocr_child_return_type,self.cmbox_ocr_child_return_type],
                                [self.label_ocr_child_id_card_side,self.cmbox_ocr_child_id_card_side],[self.label_ocr_child_detect_risk,self.cmbox_ocr_child_detect_risk],
                                [self.label_ocr_child_accuracy,self.cmbox_ocr_child_accuracy]]
        


    @layout_dele
    def ocr_child_reload(self,*args):
        """子窗口重载，返回子窗口布局"""
        # print(self.ocr_child_mode)
        mode = self.ocr_child_mode
        self.label_ocr_child_title.setText(mode)
        # 重置
        self.lnedit_ocr_child_img.clear()

        if mode in ['通用文字识别']:
            self.lnedit_ocr_child_img.setPlaceholderText('image or url')
            self.ocr_child_params = [3, 4, 5, 6, 7,10]
        elif mode in ['通用文字识别（含位置版）','通用文字识别（高精度含位置版）','通用文字识别（含生僻字版）']:
            self.lnedit_ocr_child_img.setPlaceholderText('image or url')
            self.ocr_child_params = [3,4,5,6,7,8,9,10]
        elif mode in ['通用文字识别（高精度版）']:
            self.ocr_child_params = [3,5,7,10]
        elif mode in ['身份证识别']:
            self.ocr_child_params = [3,11,5,12]
        elif mode in ['营业执照识别']:
            self.ocr_child_params = [3,5,13]

        elif mode in ['银行卡识别','名片识别','护照识别','港澳通行证识别','台湾通行证识别','户口本识别','出生医学证明识别']:
            self.ocr_child_params = [3]

        # 添加标题和提交按钮
        self.ocr_child_params.insert(0, 0)
        self.ocr_child_params.append(1)
        if self.ocr_child_params:
            for index, i in enumerate(self.ocr_child_params):
                widgets = self.ocr_child_widgets[i]
                for j, widget in enumerate(widgets):
                    widget.setVisible(True)
                    css = "*{background-color:%s;color:%s;border:0;height:25px;font:YaHei;} :pressed{background-color:%s;color:%s;}" % (
                        random_color(mode='background'), random_color(mode='font'), random_color(mode='background'),
                        random_color(mode='font'))
                    widget.setStyleSheet(css)
                    if widget.__doc__.startswith('QLabel'):
                        widget.setAlignment(Qt.AlignCenter)
                    elif widget.__doc__.startswith('MLineEdit'):
                        widget.setClearButtonEnabled(True)
                    if len(widgets) == 1:
                        widget.setFixedHeight(25)
                        self.glayout_ocr_child_params.addWidget(widget, index, 0, 1, 2)
                        continue
                    elif j == 0:
                        widget.setFixedWidth(80)
                    else:
                        w = self.width() // 3
                        if w > 300: w = 300
                        widget.setFixedWidth(w)

                    self.glayout_ocr_child_params.addWidget(widget, index, j, 1, 1)

        # 结果显示控件加载
        self.txedit_ocr_child_content = QTextEdit()
        self.glayout_ocr_child_content.addWidget(self.txedit_ocr_child_content,0,0,1,1)
        css = "*{background-color:%s;color:%s;border:0;height:25px;font:YaHei;} :pressed{background-color:%s;color:%s;}" % (
            random_color(mode='background'), random_color(mode='font'), random_color(mode='background'),
            random_color(mode='font'))
        self.txedit_ocr_child_content.setStyleSheet(css)
        self.txedit_ocr_child_content.setVisible(True)

        return self.glayout_ocr_child


    @catch_except
    def btn_ocr_child_ok_clicked(self,*args):
        """文字识别子窗口提交按钮点击，进入数据获取，回调数据处理函数"""
        mode = self.ocr_child_mode
        result = {}
        others = {}
        if mode in ['通用文字识别']:
            filepath = self.lnedit_ocr_child_img.text()
            image = self.file_to_bytes(filepath,False)
            if image:option = {'image':base64.b64encode(image).decode()}
            else:option = {'url':filepath}
            language_type = self.ocr_child_lan_dict.get(self.cmbox_ocr_child_lan.currentText())
            detect_direction = self.cmbox_ocr_child_detect_direction.currentText()
            detect_language = self.cmbox_ocr_child_detect_lan.currentText()
            probability = self.cmbox_ocr_child_probability.currentText()
            option.update({"language_type":language_type,"detect_direction":detect_direction,"detect_language":detect_language,"probability":probability})
            result = self.Apiocr.basicGeneral(option)
            return_type = self.cmbox_ocr_child_return_type.currentText()
            others.update({'return_type':return_type})

        elif mode in ['通用文字识别（含位置版）','通用文字识别（高精度含位置版）','通用文字识别（含生僻字版）']:
            filepath = self.lnedit_ocr_child_img.text()
            image = self.file_to_bytes(filepath,False)
            if image:option = {'image':base64.b64encode(image).decode()}
            else:
                option = {'url':filepath}
                if mode == '通用文字识别（高精度含位置版）':
                    QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                    return None
            language_type = self.ocr_child_lan_dict.get(self.cmbox_ocr_child_lan.currentText())
            detect_direction = self.cmbox_ocr_child_detect_direction.currentText()
            detect_language = self.cmbox_ocr_child_detect_lan.currentText()
            probability = self.cmbox_ocr_child_probability.currentText()
            recognize_granularity = self.cmbox_ocr_child_rec_gran.currentText()
            vertexes_location = self.cmbox_ocr_child_vertexes_location.currentText()
            option.update({'vertexes_location':vertexes_location,'recognize_granularity':recognize_granularity,"language_type":language_type,"detect_direction":detect_direction,"detect_language":detect_language,"probability":probability})
            if mode == '通用文字识别（高精度含位置版）':
                result = self.Apiocr.accurate(option)
            elif mode == '通用文字识别（含位置版）':
                result = self.Apiocr.general(option)
            elif mode == '通用文字识别（含生僻字版）':
                result = self.Apiocr.enhancedGeneral(option)
            return_type = self.cmbox_ocr_child_return_type.currentText()
            others.update({'return_type':return_type})


        elif mode in ['通用文字识别（高精度版）']:
            filepath = self.lnedit_ocr_child_img.text()
            image = self.file_to_bytes(filepath)
            if image:
                option = {'image':base64.b64encode(image).decode()}
                detect_direction = self.cmbox_ocr_child_detect_direction.currentText()
                probability = self.cmbox_ocr_child_probability.currentText()
                option.update({"detect_direction":detect_direction,"probability":probability})
                result = self.Apiocr.basicAccurate(option)
                return_type = self.cmbox_ocr_child_return_type.currentText()
                others.update({'return_type':return_type})

        elif mode in ['身份证识别']:
            filepath = self.lnedit_ocr_child_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()
            id_card_side = self.cmbox_ocr_child_id_card_side.currentText()
            detect_direction = self.cmbox_ocr_child_detect_direction.currentText()
            detect_risk = self.cmbox_ocr_child_detect_risk.currentText()
            option = {'detect_direction':detect_direction,'detect_risk':detect_risk}
            result = self.Apiocr.idcard(image,id_card_side,option)

        elif mode in ['银行卡识别','名片识别','护照识别','港澳通行证识别','台湾通行证识别','户口本识别','出生医学证明识别']:
            filepath = self.lnedit_ocr_child_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()
            if mode == '银行卡识别':
                result = self.Apiocr.bankcard(image)
            elif mode == '名片识别':
                result = self.Apiocr.businessCard(image)
            elif mode == '护照识别':
                result = self.Apiocr.passport(image)
            elif mode == '港澳特别通行证识别':
                result = self.Apiocr.HKMacauExitentrypermit(image)
            elif mode == '台湾通行证识别':
                result = self.Apiocr.taiwanExitentrypermit(image)
            elif mode == '户口本识别':
                result = self.Apiocr.householdRegister(image)
            elif mode == '出生医学证明识别':
                result = self.Apiocr.birthCertificate(image)
        elif mode in ['营业执照识别']:
            filepath = self.lnedit_ocr_child_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()

            detect_direction = self.cmbox_ocr_child_detect_direction.currentText()
            accuracy = self.cmbox_ocr_child_accuracy.currentText()
            option = {'detect_direction':detect_direction,'accuracy':accuracy}
            result = self.Apiocr.businessLicense(image,option)

        # 调用数据处理函数
        if result:
            self.ocr_child_result_deal(mode,result,others)


    def ocr_child_result_deal(self,mode, datas, option=None,*args):
        """文字识别结果处理"""
        if mode.startswith('通用文字识别'):
            return_type = option.get('return_type')
            if return_type in ['DESC']:
                content = self.dict_get_value(datas,'')
            elif return_type == 'TEXT':
                content = self.dict_get_value_by_key(datas,'words','')
            else:
                content = "{0} TEXT {0}\n\n{1}\n\n\n{2} DESCRIBE {2}\n\n{3}".format('='*12, self.dict_get_value_by_key(datas,'words','') ,'='*10, self.dict_get_value(datas,''))

            self.txedit_ocr_child_content.setText(content)

        else:
            content = '{} --> 完成\n'.format(mode)
            content = self.dict_get_value(datas,content)
            self.txedit_ocr_child_content.setText(content)



    @catch_except
    def __init_ocr_child_invoice_ui(self,*args):
        """文字识别 --> 票据识别"-->主页初始化"""

        # 主页布局
        self.glayout_ocr_invoice_home = QGridLayout()
        self.glayout_ocr_invoice_home.setObjectName('grade_3')
        self.glayout_main.addLayout(self.glayout_ocr_invoice_home, 2, 0, Qt.AlignCenter)


        self.btn_ocr_invoice_home_1 = QPushButton("增值税发票\n识别")
        self.btn_ocr_invoice_home_2 = QPushButton("定额发票\n识别")
        self.btn_ocr_invoice_home_3 = QPushButton("通用机打发票\n识别")
        self.btn_ocr_invoice_home_4 = QPushButton("火车票识别")
        self.btn_ocr_invoice_home_5 = QPushButton("出租车票\n识别")
        self.btn_ocr_invoice_home_6 = QPushButton("行程单识别")
        self.btn_ocr_invoice_home_7 = QPushButton("通用票据\n识别")
        self.btn_ocr_invoice_home_8 = QPushButton("保险单识别")
        self.btn_ocr_invoice_home_9 = QPushButton("彩票识别")
        self.btn_ocr_invoice_btn_10 = QPushButton('行驶证识别')
        self.btn_ocr_invoice_btn_11 = QPushButton('驾驶证识别')
        self.btn_ocr_invoice_btn_12 = QPushButton('车牌识别')
        self.btn_ocr_invoice_btn_13 = QPushButton('VIN码识别')
        self.btn_ocr_invoice_btn_14 = QPushButton('机动车销售\n发票识别')
        self.btn_ocr_invoice_btn_15 = QPushButton('车辆合格证\n识别')

        self.ocr_invoice_home_btns = [self.btn_ocr_invoice_home_1,self.btn_ocr_invoice_home_2,self.btn_ocr_invoice_home_3,self.btn_ocr_invoice_home_4,self.btn_ocr_invoice_home_5,self.btn_ocr_invoice_home_6,self.btn_ocr_invoice_home_7,self.btn_ocr_invoice_home_8,self.btn_ocr_invoice_home_9,self.btn_ocr_invoice_btn_10,self.btn_ocr_invoice_btn_11,self.btn_ocr_invoice_btn_12,self.btn_ocr_invoice_btn_13,self.btn_ocr_invoice_btn_14,self.btn_ocr_invoice_btn_15]


        h = self.height() * 0.8 / 6
        w = self.width() * 0.8 / 5
        if h > 100: h = 100
        if w > h * 1.3: w = h * 1.3
        if h > w / 1.3: h = w / 1.3
        row,col = 0,0
        for btn in self.ocr_invoice_home_btns:
            self.glayout_ocr_invoice_home.addWidget(btn,row,col,1,1)
            # btn.setFixedSize(w,h)
            css = "*{width:%d;height:%d;}" \
                  ":hover{background-color:%s;}" \
                  "QPushButton{background-color:%s;}" \
                  "QPushButton:pressed{background-color:%s;}" \
                  "QToolTip{color:%s;font:Yahei;font-size:14px;}" %(w,h,random_color(),random_color(),random_color(),random_color()) # border:0px
            btn.setStyleSheet(css)
            btn.setFixedSize(QSize(w, h))
            btn.clicked.connect(self.ocr_invoice_home_btns_clicked)
            btn.setVisible(False)
            col += 1
            if col > 3:
                col = 0
                row += 1
        self.glayout_ocr_invoice_home.setSpacing(int(self.width()*0.2/6))
        self.glayout_ocr_invoice_home.setContentsMargins(10,10,10,10)

    @layout_dele
    def ocr_invoice_home_reload(self,*args):
        """forward调用，主页按钮调用ocr_invoice_home_btns_clicked"""
        # 更新forward btn
        if func_historys[4]:
            self.btn_top_forward.setVisible(True)
        else:
            self.btn_top_forward.setVisible(False)

        for btn in self.ocr_invoice_home_btns:
            btn.setVisible(True)

        return self.glayout_ocr_invoice_home


    @catch_except
    def ocr_invoice_home_btns_clicked(self,*args):
        """invoice窗口按键监听，调用窗口重载"""
        self.ocr_invoice_mode = self.sender().text().replace('\n','')

        self.ocr_invoice_child_reload()


    @catch_except
    def __ocr_invoice_child_ui(self,*args):
        """invoice子窗口布局初始化"""
        # invoice main
        self.glayout_ocr_invoice_child = QGridLayout()
        self.glayout_ocr_invoice_child.setObjectName('grade_4')
        self.glayout_main.addLayout(self.glayout_ocr_invoice_child, 2, 0)
        # 参数
        self.glayout_ocr_invoice_params = QGridLayout()
        # 内容 显示结果
        self.glayout_ocr_invoice_content = QGridLayout()
        self.glayout_ocr_invoice_child.addLayout(self.glayout_ocr_invoice_params, 0, 0, Qt.AlignTop)
        self.glayout_ocr_invoice_child.addLayout(self.glayout_ocr_invoice_content, 0, 1)


        # invoice子窗口所需参数
        self.ocr_invoice_params = []

        self.label_ocr_invoice_title = QLabel()  # 0
        self.btn_ocr_invoice_ok = QPushButton('提交')  # 1
        self.btn_ocr_invoice_ok.clicked.connect(self.btn_ocr_invoice_ok_clicked)
        self.label_ocr_invoice_option = QLabel('可选参数')  # 2
        self.btn_ocr_invoice_img = QPushButton('图片')  # 3
        self.btn_ocr_invoice_img.clicked.connect(self.btn_ocr_invoice_img_clicked)
        self.lnedit_ocr_invoice_img = MLineEdit()
        self.label_ocr_invoice_accuracy = QLabel('精度')  # 4
        self.cmbox_ocr_invoice_accuracy = QComboBox()
        self.cmbox_ocr_invoice_accuracy.addItems(['normal', 'high'])

        self.label_ocr_invoice_detect_direction = QLabel('朝向检测')#5
        self.cmbox_ocr_invoice_detect_direction = QComboBox()
        self.cmbox_ocr_invoice_detect_direction.addItems(['false','true'])

        self.label_ocr_invoice_probability = QLabel('返回置信度') # 6
        self.cmbox_ocr_invoice_probability = QComboBox()
        self.cmbox_ocr_invoice_probability.addItems(['false','true'])
        self.label_ocr_invoice_rec_gran = QLabel('字符位置') #7
        self.cmbox_ocr_invoice_rec_gran = QComboBox()
        self.cmbox_ocr_invoice_rec_gran.addItems(['false','true'])

        self.label_ocr_invoice_kv_business = QLabel('商业逻辑处理')#8
        self.cmbox_ocr_invoice_kv_business = QComboBox()
        self.cmbox_ocr_invoice_kv_business.addItems(['true','false'])

        self.label_ocr_invoice_vehicle_license_side = QLabel('正反面')#9
        self.cmbox_ocr_invoice_vehicle_license_side = QComboBox()
        self.cmbox_ocr_invoice_vehicle_license_side.addItems(['front','back'])
        self.label_ocr_invoice_multi_detect = QLabel('多车牌检测') #10
        self.cmbox_ocr_invoice_multi_detect = QComboBox()
        self.cmbox_ocr_invoice_multi_detect.addItems(['false','true'])


        self.ocr_invoice_widgets = [[self.label_ocr_invoice_title], [self.btn_ocr_invoice_ok],[self.label_ocr_invoice_option],
                                    [self.btn_ocr_invoice_img, self.lnedit_ocr_invoice_img],[self.label_ocr_invoice_accuracy, self.cmbox_ocr_invoice_accuracy],
                                    [self.label_ocr_invoice_detect_direction,self.cmbox_ocr_invoice_detect_direction],[self.label_ocr_invoice_probability,self.cmbox_ocr_invoice_probability],
                                    [self.label_ocr_invoice_rec_gran,self.cmbox_ocr_invoice_rec_gran],[self.label_ocr_invoice_kv_business,self.cmbox_ocr_invoice_kv_business],
                                    [self.label_ocr_invoice_vehicle_license_side,self.cmbox_ocr_invoice_vehicle_license_side],[self.label_ocr_invoice_multi_detect,self.cmbox_ocr_invoice_multi_detect],
                                    ]

    @layout_dele
    def ocr_invoice_child_reload(self, *args):
        """invoice子窗口重载"""
        if func_historys[5]:self.btn_top_forward.setVisible(True)
        else:self.btn_top_forward.setVisible(False)

        mode = self.ocr_invoice_mode
        self.label_ocr_invoice_title.setText(mode)

        self.ocr_invoice_params = []
        if mode in ['增值税发票识别']:
            self.ocr_invoice_params = [3,4]
        elif mode in ['定额发票识别','通用机打发票识别','火车票识别','出租车票识别','行程单识别','VIN码识别','机动车销售发票识别','车辆合格证识别']:
            self.ocr_invoice_params = [3]
        elif mode in ['通用票据识别']:
            self.ocr_invoice_params = [3,4,5,6,7]
        elif mode in ['保险单识别']:
            self.ocr_invoice_params = [3,8]
        elif mode in ['彩票识别']:
            self.ocr_invoice_params = [3,7]
        elif mode in ['行驶证识别','驾驶证识别']:
            self.ocr_invoice_params = [3,5,4,9]
        elif mode in ['车牌识别']:
            self.ocr_invoice_params = [3,10]


        if self.ocr_invoice_params:
            self.ocr_invoice_params.insert(0,0)
            self.ocr_invoice_params.append(1)
            for index, i in enumerate(self.ocr_invoice_params):
                widgets = self.ocr_invoice_widgets[i]
                for j, widget in enumerate(widgets):
                    widget.setVisible(True)
                    css = "*{background-color:%s;color:%s;border:0;height:25px;font:YaHei;} :pressed{background-color:%s;color:%s;}" % (
                        random_color(mode='background'), random_color(mode='font'), random_color(mode='background'),
                        random_color(mode='font'))
                    widget.setStyleSheet(css)
                    if widget.__doc__.startswith('QLabel'):
                        widget.setAlignment(Qt.AlignCenter)
                    elif widget.__doc__.startswith('MLineEdit'):
                        widget.setClearButtonEnabled(True)
                    if len(widgets) == 1:
                        widget.setFixedHeight(25)
                        self.glayout_ocr_invoice_params.addWidget(widget, index, 0, 1, 2)
                        continue
                    elif j == 0:
                        widget.setFixedWidth(80)
                    else:
                        w = self.width() // 3
                        if w > 300: w = 300
                        widget.setFixedWidth(w)

                    self.glayout_ocr_invoice_params.addWidget(widget, index, j, 1, 1)

        # 结果显示控件加载
        self.txedit_ocr_invoice_content = QTextEdit()
        self.glayout_ocr_invoice_content.addWidget(self.txedit_ocr_invoice_content,0,0,1,1)
        css = "*{background-color:%s;color:%s;border:0;height:25px;font:YaHei;} :pressed{background-color:%s;color:%s;}" % (
            random_color(mode='background'), random_color(mode='font'), random_color(mode='background'),
            random_color(mode='font'))
        self.txedit_ocr_invoice_content.setStyleSheet(css)
        self.txedit_ocr_invoice_content.setVisible(True)

        return self.glayout_ocr_invoice_child


    def btn_ocr_invoice_ok_clicked(self, *args):
        """访问API"""
        mode = self.ocr_invoice_mode

        result = {}
        others = {}
        if mode in ['增值税发票识别']:
            filepath = self.lnedit_ocr_invoice_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()
            accuracy = self.cmbox_ocr_invoice_accuracy.currentText()
            option = {"accuracy":accuracy}
            result = self.Apiocr.vatInvoice(image,option)
        elif mode in ['定额发票识别', '通用机打发票识别', '火车票识别', '出租车票识别', '行程单识别','VIN码识别','机动车销售发票识别','车辆合格证识别']:
            filepath = self.lnedit_ocr_invoice_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()
            if mode == '定额发票识别':
                result = self.Apiocr.quotaInvoice(image)
            elif mode == '通用机打发票识别':
                result = self.Apiocr.invoice(image)
            elif mode == '火车票识别':
                result = self.Apiocr.trainTicket(image)
            elif mode == '出租车票识别':
                result = self.Apiocr.taxiReceipt(image)
            elif mode == '行程单识别':
                result = self.Apiocr.airTicket(image)
            elif mode == 'VIN码识别':
                result = self.Apiocr.vinCode(image)
            elif mode == '机动车销售发票识别':
                result = self.Apiocr.vehicleInvoice(image)
            elif mode == '车辆合格证识别':
                result = self.Apiocr.vehicleCertificate(image)

        elif mode in ['行驶证识别','驾驶证识别']:
            filepath = self.lnedit_ocr_invoice_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()
            accuracy = self.cmbox_ocr_invoice_accuracy.currentText()
            detect_direction = self.cmbox_ocr_invoice_detect_direction.currentText()
            vehicle_license_side = self.cmbox_ocr_invoice_vehicle_license_side.currentText()
            option = {"vehicle_license_side": vehicle_license_side, "accuracy": accuracy,
                      'detect_direction': detect_direction}

            if mode == '驾驶证识别':
                result = self.Apiocr.drivingLicense(image)
            elif mode == '行驶证识别':
                result = self.Apiocr.vehicleLicense(image)

        elif mode in ['车牌识别']:
            filepath = self.lnedit_ocr_invoice_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()
            multi_detect = self.cmbox_ocr_invoice_multi_detect.currentText()
            option = {'multi_detect':multi_detect}
            result = self.Apiocr.licensePlate(image,option)
        elif mode in ['通用票据识别']:
            filepath = self.lnedit_ocr_invoice_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()
            accuracy = self.cmbox_ocr_invoice_accuracy.currentText()
            recognize_granularity = self.cmbox_ocr_invoice_rec_gran.currentText()
            probability = self.cmbox_ocr_invoice_probability.currentText()
            detect_direction = self.cmbox_ocr_invoice_detect_direction.currentText()
            option = {"accuracy":accuracy,'recognize_granularity':recognize_granularity,'probability':probability,'detect_direction':detect_direction}

            result = self.Apiocr.receipt(image,option)

        elif mode in ['保险单识别']:
            filepath = self.lnedit_ocr_invoice_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()
            result = self.Apiocr.insuranceDocuments(image)

        elif mode in ['彩票识别']:
            filepath = self.lnedit_ocr_invoice_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()
            recognize_granularity = self.cmbox_ocr_invoice_rec_gran.currentText()
            option = {'recognize_granularity':recognize_granularity}
            result = self.Apiocr.lottery(image,option)

        if result:
            self.ocr_invoice_result_deal(mode,result)


    def ocr_invoice_result_deal(self,mode,datas,option=None,*args):
        """票据文字识别结果处理"""

        content = '{} --> 完成\n'.format(mode)
        content = self.dict_get_value(datas,content)
        self.txedit_ocr_invoice_content.setText(content)

    @catch_except
    def __init_ocr_child_other_ui(self, *args):
        """文字识别 --> 其他识别"-->主页初始化"""

        # 主页布局
        self.glayout_ocr_other_home = QGridLayout()
        self.glayout_ocr_other_home.setObjectName('grade_3')
        self.glayout_main.addLayout(self.glayout_ocr_other_home, 2, 0, Qt.AlignCenter)

        self.btn_ocr_other_home_1 = QPushButton("网络图片文字\n识别")
        self.btn_ocr_other_home_2 = QPushButton("公式识别")
        self.btn_ocr_other_home_3 = QPushButton("手写文字识别")
        self.btn_ocr_other_home_4 = QPushButton("表格文字识别\n（异步接口）")
        self.btn_ocr_other_home_9 = QPushButton("表格文字识别\n（异步获取）")
        self.btn_ocr_other_home_5 = QPushButton("表格文字识别\n（同步）")
        self.btn_ocr_other_home_6 = QPushButton("数字识别")
        self.btn_ocr_other_home_7 = QPushButton("二维码识别")
        self.btn_ocr_other_home_8 = QPushButton("印章检测")

        self.ocr_other_home_btns = [self.btn_ocr_other_home_1, self.btn_ocr_other_home_2, self.btn_ocr_other_home_3,
                                    self.btn_ocr_other_home_4, self.btn_ocr_other_home_9, self.btn_ocr_other_home_5,
                                    self.btn_ocr_other_home_6,
                                    self.btn_ocr_other_home_7, self.btn_ocr_other_home_8]

        h = self.height() * 0.8 / 5
        w = self.width() * 0.8 / 4
        if h > 100: h = 100
        if w > h * 1.3: w = h * 1.3
        if h > w / 1.3: h = w / 1.3
        row, col = 0, 0
        for btn in self.ocr_other_home_btns:
            self.glayout_ocr_other_home.addWidget(btn, row, col, 1, 1)
            # btn.setFixedSize(w,h)
            css = "*{width:%d;height:%d;}" \
                  ":hover{background-color:%s;}" \
                  "QPushButton{background-color:%s;}" \
                  "QPushButton:pressed{background-color:%s;}" \
                  "QToolTip{color:%s;font:Yahei;font-size:14px;}" % (
                      w, h, random_color(), random_color(), random_color(), random_color())  # border:0px
            btn.setStyleSheet(css)
            btn.setFixedSize(QSize(w, h))
            btn.clicked.connect(self.ocr_other_home_btns_clicked)
            btn.setVisible(False)
            col += 1
            if col > 3:
                col = 0
                row += 1
        self.glayout_ocr_other_home.setSpacing(int(self.width() * 0.2 / 6))
        self.glayout_ocr_other_home.setContentsMargins(10, 10, 10, 10)

    @layout_dele
    def ocr_other_home_reload(self, *args):
        """forward调用，主页按钮调用ocr_other_home_btns_clicked"""
        # 更新forward btn
        if func_historys[4]:
            self.btn_top_forward.setVisible(True)
        else:
            self.btn_top_forward.setVisible(False)

        for btn in self.ocr_other_home_btns:
            btn.setVisible(True)

        return self.glayout_ocr_other_home

    @catch_except
    def ocr_other_home_btns_clicked(self, *args):
        """other窗口按键监听，调用窗口重载"""
        self.ocr_other_mode = self.sender().text().replace('\n', '')

        self.ocr_other_child_reload()

    @catch_except
    def __ocr_other_child_ui(self, *args):
        """other子窗口布局初始化"""
        # other main
        self.glayout_ocr_other_child = QGridLayout()
        self.glayout_ocr_other_child.setObjectName('grade_4')
        self.glayout_main.addLayout(self.glayout_ocr_other_child, 2, 0)
        # 参数
        self.glayout_ocr_other_params = QGridLayout()
        # 内容 显示结果
        self.glayout_ocr_other_content = QGridLayout()
        self.glayout_ocr_other_child.addLayout(self.glayout_ocr_other_params, 0, 0, Qt.AlignTop)
        self.glayout_ocr_other_child.addLayout(self.glayout_ocr_other_content, 0, 1)

        # other子窗口所需参数
        self.ocr_other_params = []

        self.label_ocr_other_title = QLabel()  # 0
        self.btn_ocr_other_ok = QPushButton('提交')  # 1
        self.btn_ocr_other_ok.clicked.connect(self.btn_ocr_other_ok_clicked)
        self.label_ocr_other_option = QLabel('可选参数')  # 2
        self.btn_ocr_other_img = QPushButton('图片')  # 3
        self.btn_ocr_other_img.clicked.connect(self.btn_ocr_other_img_clicked)
        self.lnedit_ocr_other_img = MLineEdit()
        self.label_ocr_other_accuracy = QLabel('精度')  # 4
        self.cmbox_ocr_other_accuracy = QComboBox()
        self.cmbox_ocr_other_accuracy.addItems(['normal', 'high'])

        self.label_ocr_other_detect_direction = QLabel('朝向检测')  # 5
        self.cmbox_ocr_other_detect_direction = QComboBox()
        self.cmbox_ocr_other_detect_direction.addItems(['false', 'true'])

        self.label_ocr_other_probability = QLabel('返回置信度')  # 6
        self.cmbox_ocr_other_probability = QComboBox()
        self.cmbox_ocr_other_probability.addItems(['false', 'true'])
        self.label_ocr_other_rec_gran = QLabel('字符位置')  # 7
        self.cmbox_ocr_other_rec_gran = QComboBox()
        self.cmbox_ocr_other_rec_gran.addItems(['false', 'true'])

        self.label_ocr_other_kv_business = QLabel('商业逻辑处理')  # 8
        self.cmbox_ocr_other_kv_business = QComboBox()
        self.cmbox_ocr_other_kv_business.addItems(['true', 'false'])

        self.label_ocr_other_vehicle_license_side = QLabel('正反面')  # 9
        self.cmbox_ocr_other_vehicle_license_side = QComboBox()
        self.cmbox_ocr_other_vehicle_license_side.addItems(['front', 'back'])
        self.label_ocr_other_multi_detect = QLabel('多车牌检测')  # 10
        self.cmbox_ocr_other_multi_detect = QComboBox()
        self.cmbox_ocr_other_multi_detect.addItems(['false', 'true'])

        self.label_ocr_other_detect_lan = QLabel('语言检测')  # 11
        self.cmbox_ocr_other_detect_lan = QComboBox()
        self.cmbox_ocr_other_detect_lan.addItems(['false', 'true'])
        self.label_ocr_other_words_type = QLabel('类型')  # 12
        self.cmbox_ocr_other_words_type = QComboBox()
        self.cmbox_ocr_other_words_type.addItems(['normal', 'number'])
        self.label_ocr_other_disp_formula = QLabel('单独输出公式')  # 13
        self.cmbox_ocr_other_disp_formula = QComboBox()
        self.cmbox_ocr_other_disp_formula.addItems(['true', 'false'])
        self.label_ocr_other_is_sync = QLabel('异步获取')  # 14
        self.cmbox_ocr_other_is_sync = QComboBox()
        self.cmbox_ocr_other_is_sync.addItems(['false', 'true'])
        self.label_ocr_other_request_type = QLabel('异步结果类型')  # 15
        self.cmbox_ocr_other_request_type = QComboBox()
        self.cmbox_ocr_other_request_type.addItems(['json', 'excel'])
        self.label_ocr_other_table_border = QLabel('框线')  # 16
        self.cmbox_ocr_other_table_border = QComboBox()
        self.cmbox_ocr_other_table_border.addItems(['normal', 'none'])
        self.label_ocr_other_request_id = QLabel('请求ID')  # 17
        self.lnedit_ocr_other_request_id = MLineEdit()
        # self.cmbox_ocr_other_sync_type = QComboBox()
        # self.cmbox_ocr_other_sync_type.addItems(['异步发送','异步获取'])

        self.ocr_other_widgets = [[self.label_ocr_other_title], [self.btn_ocr_other_ok],
                                  [self.label_ocr_other_option],
                                  [self.btn_ocr_other_img, self.lnedit_ocr_other_img],
                                  [self.label_ocr_other_accuracy, self.cmbox_ocr_other_accuracy],
                                  [self.label_ocr_other_detect_direction, self.cmbox_ocr_other_detect_direction],
                                  [self.label_ocr_other_probability, self.cmbox_ocr_other_probability],
                                  [self.label_ocr_other_rec_gran, self.cmbox_ocr_other_rec_gran],
                                  [self.label_ocr_other_kv_business, self.cmbox_ocr_other_kv_business],
                                  [self.label_ocr_other_vehicle_license_side,
                                   self.cmbox_ocr_other_vehicle_license_side],
                                  [self.label_ocr_other_multi_detect, self.cmbox_ocr_other_multi_detect],
                                  [self.label_ocr_other_detect_lan, self.cmbox_ocr_other_detect_lan],
                                  [self.cmbox_ocr_other_words_type, self.cmbox_ocr_other_words_type],
                                  [self.label_ocr_other_disp_formula, self.cmbox_ocr_other_disp_formula],
                                  [self.label_ocr_other_is_sync, self.cmbox_ocr_other_is_sync],
                                  [self.label_ocr_other_request_type, self.cmbox_ocr_other_request_type],
                                  [self.label_ocr_other_table_border, self.cmbox_ocr_other_table_border],
                                  [self.label_ocr_other_request_id, self.lnedit_ocr_other_request_id]]

    @layout_dele
    def ocr_other_child_reload(self, *args):
        """other子窗口重载"""
        if func_historys[5]:
            self.btn_top_forward.setVisible(True)
        else:
            self.btn_top_forward.setVisible(False)

        mode = self.ocr_other_mode
        self.label_ocr_other_title.setText(mode)
        # 内容重置
        self.lnedit_ocr_other_img.clear()

        self.ocr_other_params = []
        if mode in ['网络图片文字识别']:
            self.ocr_other_params = [3, 5, 11]
            self.lnedit_ocr_other_img.setPlaceholderText('image or url')
        elif mode in ['数字识别']:
            self.ocr_other_params = [3, 7, 5]
        elif mode in ['二维码识别', '印章检测']:
            self.ocr_other_params = [3]
        elif mode in ['手写文字识别']:
            self.ocr_other_params = [3, 7, 12]
        elif mode in ['公式识别']:
            self.ocr_other_params = [3, 7, 5, 13]
        elif mode in ['表格文字识别（异步接口）']:
            self.ocr_other_params = [3, 14, 15]
        elif mode in ['表格文字识别（同步）']:
            self.ocr_other_params = [3, 16]
        elif mode in ['表格文字识别（异步获取）']:
            self.ocr_other_params = [17]

        if self.ocr_other_params:
            self.ocr_other_params.insert(0, 0)
            self.ocr_other_params.append(1)
            for index, i in enumerate(self.ocr_other_params):
                widgets = self.ocr_other_widgets[i]
                for j, widget in enumerate(widgets):
                    widget.setVisible(True)
                    css = "*{background-color:%s;color:%s;border:0;height:25px;font:YaHei;} :pressed{background-color:%s;color:%s;}" % (
                        random_color(mode='background'), random_color(mode='font'), random_color(mode='background'),
                        random_color(mode='font'))
                    widget.setStyleSheet(css)
                    if widget.__doc__.startswith('QLabel'):
                        widget.setAlignment(Qt.AlignCenter)
                    elif widget.__doc__.startswith('MLineEdit'):
                        widget.setClearButtonEnabled(True)
                    if len(widgets) == 1:
                        widget.setFixedHeight(25)
                        self.glayout_ocr_other_params.addWidget(widget, index, 0, 1, 2)
                        continue
                    elif j == 0:
                        widget.setFixedWidth(80)
                    else:
                        w = self.width() // 3
                        if w > 300: w = 300
                        widget.setFixedWidth(w)

                    self.glayout_ocr_other_params.addWidget(widget, index, j, 1, 1)

        # 结果显示控件加载
        self.txedit_ocr_other_content = QTextEdit()
        self.glayout_ocr_other_content.addWidget(self.txedit_ocr_other_content, 0, 0, 1, 1)
        css = "*{background-color:%s;color:%s;border:0;height:25px;font:YaHei;} :pressed{background-color:%s;color:%s;}" % (
            random_color(mode='background'), random_color(mode='font'), random_color(mode='background'),
            random_color(mode='font'))
        self.txedit_ocr_other_content.setStyleSheet(css)
        self.txedit_ocr_other_content.setVisible(True)

        return self.glayout_ocr_other_child

    @catch_except
    def btn_ocr_other_ok_clicked(self, *args):
        """访问API"""
        mode = self.ocr_other_mode

        result = {}
        others = {}

        if mode in ['二维码识别']:
            filepath = self.lnedit_ocr_other_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()
            result = self.Apiocr.qrcode(image)
        elif mode in ['表格文字识别（异步获取）']:
            request_id = self.lnedit_ocr_other_request_id.text()
            result = self.Apiocr.getTableRecognitionResult(request_id)

        elif mode in ['表格文字识别（异步接口）']:
            filepath = self.lnedit_ocr_other_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()
            is_sync = self.cmbox_ocr_other_is_sync.currentText()
            request_type = self.cmbox_ocr_other_request_type.currentText()
            option = {'is_sync': is_sync, 'request_type': request_type}
            result = self.Apiocr.tableRecognitionAsync(image, option)

        elif mode in ['表格文字识别（同步）']:
            filepath = self.lnedit_ocr_other_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()
            table_border = self.cmbox_ocr_other_table_border.currentText()
            option = {'table_border': table_border}
            result = self.Apiocr.form(image, option)


        elif mode in ['手写文字识别']:
            filepath = self.lnedit_ocr_other_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()
            recognize_granularity = self.cmbox_ocr_other_rec_gran.currentText()
            words_type = self.cmbox_ocr_other_words_type.currentText()
            option = {'recognize_granularity': recognize_granularity, 'words_type': words_type}
            result = self.Apiocr.handwriting(image, option)

        elif mode in ['数字识别']:
            filepath = self.lnedit_ocr_other_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()
            recognize_granularity = self.cmbox_ocr_other_rec_gran.currentText()
            detect_direction = self.cmbox_ocr_other_detect_direction.currentText()
            option = {'recognize_granularity': recognize_granularity, 'detect_direction': detect_direction}
            result = self.Apiocr.numbers(image, option)

        elif mode in ['公式识别']:
            filepath = self.lnedit_ocr_other_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()
            recognize_granularity = self.cmbox_ocr_other_rec_gran.currentText()
            detect_direction = self.cmbox_ocr_other_detect_direction.currentText()
            disp_formula = self.cmbox_ocr_other_disp_formula.currentText()
            option = {'disp_formula': disp_formula, 'recognize_granularity': recognize_granularity,
                      'detect_direction': detect_direction}
            result = self.Apiocr.formula(image, option)

        elif mode in ['网络图片文字识别']:
            filepath = self.lnedit_ocr_other_img.text()
            if os.path.isfile(filepath):
                image = open(r'{}'.format(filepath), 'rb').read()
                option = {'image': base64.b64encode(image).decode()}
            else:
                option = {'url': filepath}
            detect_language = self.cmbox_ocr_other_detect_lan.currentText()
            detect_direction = self.cmbox_ocr_other_detect_direction.currentText()
            option.update({'detect_language': detect_language, 'detect_direction': detect_direction})
            result = self.Apiocr.webImage(option)

        if result:
            self.ocr_other_result_deal(mode, result)

    def ocr_other_result_deal(self, mode, datas, option=None, *args):
        """票据文字识别结果处理"""

        print(mode, datas)
        if mode in ['网络图片文字识别']:
            content = '{}-->完成\n'.format(mode)
            content = self.dict_get_value(datas, content)
            self.txedit_ocr_other_content.setText(content)


        else:
            content = '{}-->完成\n'.format(mode)
            content = self.dict_get_value(datas, content)
            self.txedit_ocr_other_content.setText(content)

    def file_to_bytes(self, file, err=True):
        """传入文件路径，返回文件流"""
        if not os.path.isfile(file):
            if err:
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
            return None
        image = open(r'{}'.format(file), 'rb').read()
        return image

    def btn_ocr_other_img_clicked(self,*args):
        file = QFileDialog.getOpenFileName(self,'图片','./','AllFile (*)')
        if file[0]:
            self.lnedit_ocr_other_img.setText(file[0])

    def btn_ocr_child_img_clicked(self,*args):
        file = QFileDialog.getOpenFileName(self,'图片','./','AllFile (*)')
        if file[0]:
            self.lnedit_ocr_child_img.setText(file[0])

    def btn_ocr_invoice_img_clicked(self,*args):
        file = QFileDialog.getOpenFileName(self,'图片','./','AllFile (*)')
        if file[0]:
            self.lnedit_ocr_invoice_img.setText(file[0])

    def resizeEvent_ocr(self, a0: QtGui.QResizeEvent) -> None:
        value = int(self.width()*0.2 /6)
        self.glayout_ocr_home.setSpacing(value)


