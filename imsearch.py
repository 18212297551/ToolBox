from ToolBox.main_ui import *

class Imsearch(Ui):
    def __init__(self):
        super(Imsearch, self).__init__()
        self.ApiImsearch = AipImageSearch(self.APPID,self.APIKEY,self.SECRETKEY)

        self.__init_imsearch_home_ui()
        self.__imsearch_child_ui()
        self.btn_home_imgsearch.clicked.connect(self.imsearch_home_reload)


    @catch_except
    def __init_imsearch_home_ui(self,*args):

        self.glayout_imsearch_home = QGridLayout()
        self.glayout_main.addLayout(self.glayout_imsearch_home,2,0,Qt.AlignCenter)
        self.glayout_imsearch_home.setObjectName('grade_2')

        self.btn_imsearch_home_1 = QPushButton("相同图片搜索\n入库")
        self.btn_imsearch_home_2 = QPushButton("相同图片搜索\n检索")
        self.btn_imsearch_home_3 = QPushButton("相同图片搜索\n删除")
        self.btn_imsearch_home_4 = QPushButton("相同图片搜索\n更新")
        self.btn_imsearch_home_5 = QPushButton("相似图片搜索\n入库")
        self.btn_imsearch_home_6 = QPushButton("相似图片搜索\n检索")
        self.btn_imsearch_home_7 = QPushButton("相似图片搜索\n删除")
        self.btn_imsearch_home_8 = QPushButton("相似图片搜索\n更新")
        self.btn_imsearch_home_9 = QPushButton("商品图片搜索\n入库")
        self.btn_imsearch_home_10 = QPushButton("商品图片搜索\n检索")
        self.btn_imsearch_home_11 = QPushButton("商品图片搜索\n删除")
        self.btn_imsearch_home_12 = QPushButton("商品图片搜索\n更新")

        self.imsearch_home_btns = [self.btn_imsearch_home_1,self.btn_imsearch_home_2,self.btn_imsearch_home_3,self.btn_imsearch_home_4,self.btn_imsearch_home_5,self.btn_imsearch_home_6,self.btn_imsearch_home_7,self.btn_imsearch_home_8,self.btn_imsearch_home_9,self.btn_imsearch_home_10,self.btn_imsearch_home_11,self.btn_imsearch_home_12]

        self.glayout_imsearch_home.setSpacing(int(self.width()*0.2/6))
        self.glayout_imsearch_home.setContentsMargins(10,10,10,10)

        h = self.height() * 0.8 / 5
        w = self.width() * 0.8 / 4
        if h > 100: h = 100
        if w > h * 1.3: w = h * 1.3
        if h > w / 1.3: h = w / 1.3
        row,col = 0,0
        for btn in self.imsearch_home_btns:
            self.glayout_imsearch_home.addWidget(btn,row,col,1,1)
            # btn.setFixedSize(w,h)
            css = "*{width:%d;height:%d;}" \
                  ":hover{background-color:%s;}" \
                  "QPushButton{background-color:%s;}" \
                  "QPushButton:pressed{background-color:%s;}" \
                  "QToolTip{color:%s;font:Yahei;font-size:14px;}" %(w,h,random_color(),random_color(),random_color(),random_color()) # border:0px
            btn.setStyleSheet(css)
            btn.setFixedSize(QSize(w, h))
            btn.clicked.connect(self.imsearch_home_btn_clicked)
            btn.setVisible(False)
            col += 1
            if col > 3:
                col = 0
                row += 1


    @layout_dele
    def imsearch_home_reload(self,*args):
        """文字识别主页重载"""
        if func_historys[3]:
            self.btn_top_forward.setVisible(True)
        else:
            self.btn_top_forward.setVisible(False)

        for btn in self.imsearch_home_btns:
            btn.setVisible(True)

        return self.glayout_imsearch_home

    def imsearch_home_btn_clicked(self,*args):
        self.imsearch_child_mode = self.sender().text().replace('\n','')
        self.imsearch_child_reload()

    def __imsearch_child_ui(self):
        """图片搜索子窗口初始化"""
        self.glayout_imsearch_child = QGridLayout()
        self.glayout_imsearch_child.setObjectName('grade_3')
        self.glayout_main.addLayout(self.glayout_imsearch_child,2,0)

        self.glayout_imsearch_child_params = QGridLayout()
        self.glayout_imsearch_child_content = QGridLayout()

        self.glayout_imsearch_child.addLayout(self.glayout_imsearch_child_params,0,0,Qt.AlignTop)
        self.glayout_imsearch_child.addLayout(self.glayout_imsearch_child_content,0,1)

        self.cmbox_imsearch_child_action = QComboBox()

        self.label_imsearch_child_title = QLabel()#0
        self.btn_imsearch_child_ok = QPushButton('提交')#1
        self.btn_imsearch_child_ok.clicked.connect(self.imsearch_child_ok_clicked)
        self.label_imsearch_child_option = QLabel('可选参数')#2
        self.btn_imsearch_child_img = QPushButton('图片')#3
        self.btn_imsearch_child_img.clicked.connect(self.btn_imsearch_child_img_clicked)
        self.lnedit_imsearch_child_img = MLineEdit()
        self.lnedit_imsearch_child_img.setClearButtonEnabled(True)
        self.label_imsearch_child_brief = QLabel('ID')#4
        self.lnedit_imsearch_child_brief = MLineEdit()
        self.label_imsearch_child_tags = QLabel('标签')#5
        self.lnedit_imsearch_child_tags = MLineEdit()
        self.lnedit_imsearch_child_tags.setValidator(QtGui.QIntValidator())
        self.label_imsearch_child_tag_logic = QLabel('检索逻辑')#6
        self.cmbox_imsearch_child_tag_logic = QComboBox()
        self.cmbox_imsearch_child_tag_logic.addItems(['0','1'])
        self.label_imsearch_child_pn = QLabel('起始位置')#7
        self.spb_imsearch_child_pn = QSpinBox()
        self.spb_imsearch_child_pn.setRange(1,1000)
        self.spb_imsearch_child_pn.setValue(1)
        self.label_imsearch_child_rn = QLabel('截取条数')#8
        self.spb_imsearch_child_rn = QSpinBox()
        self.spb_imsearch_child_rn.setValue(300)
        self.spb_imsearch_child_rn.setRange(1,10000)
        self.label_imsearch_child_class_id1 = QLabel('分类1') #9
        self.lnedit_imsearch_child_class_id1 = MLineEdit()
        self.label_imsearch_child_class_id2 = QLabel('分类2')#10
        self.lnedit_imsearch_child_class_id2 = MLineEdit()


        self.imsearch_child_widgets = [[self.label_imsearch_child_title],[self.btn_imsearch_child_ok],[self.label_imsearch_child_option],
                                 [self.btn_imsearch_child_img,self.lnedit_imsearch_child_img],[self.label_imsearch_child_brief,self.lnedit_imsearch_child_brief],
                                 [self.label_imsearch_child_tags,self.lnedit_imsearch_child_tags],[self.label_imsearch_child_tag_logic,self.cmbox_imsearch_child_tag_logic],[self.label_imsearch_child_pn,self.spb_imsearch_child_pn],
                                       [self.label_imsearch_child_rn,self.spb_imsearch_child_rn],[self.label_imsearch_child_class_id1,self.lnedit_imsearch_child_class_id1],
                                       [self.label_imsearch_child_class_id2,self.lnedit_imsearch_child_class_id2]]



    @layout_dele
    def imsearch_child_reload(self,*args):
        """子窗口重载"""
        mode = self.imsearch_child_mode
        self.label_imsearch_child_title.setText(mode)
        # print(mode)
        self.imsearch_child_params = []
        self.lnedit_imsearch_child_img.setPlaceholderText('image or url')
        if mode in ['相同图片搜索入库','相同图片搜索更新','相似图片搜索入库','相似图片搜索更新']:
            self.imsearch_child_params = [3,4,5]
        elif mode in ['相同图片搜索检索','相似图片搜索检索']:
            self.imsearch_child_params = [3,5,6,7,8]
        elif mode in ['相同图片搜索删除','相似图片搜索删除','商品图片搜索删除']:
            self.imsearch_child_params = [3]
            self.lnedit_imsearch_child_img.setPlaceholderText('image or url or cont_sign')
        elif mode in ['商品图片搜索入库','商品图片搜索更新']:
            self.imsearch_child_params = [3,4,9,10]
        elif mode in ['商品图片搜索检索']:
            self.imsearch_child_params = [3,6,7,8,9,10]



        
        if self.imsearch_child_params:
            self.imsearch_child_params.insert(0, 0)
            self.imsearch_child_params.append(1)
            for index, i in enumerate(self.imsearch_child_params):
                widgets = self.imsearch_child_widgets[i]
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
                        self.glayout_imsearch_child_params.addWidget(widget, index, 0, 1, 2)
                        continue
                    elif j == 0:
                        widget.setFixedWidth(80)
                    else:
                        w = self.width() // 3
                        if w > 300: w = 300
                        widget.setFixedWidth(w)

                    self.glayout_imsearch_child_params.addWidget(widget, index, j, 1, 1)

        # 结果显示控件加载
        self.txedit_imsearch_child_content = QTextEdit()
        self.glayout_imsearch_child_content.addWidget(self.txedit_imsearch_child_content, 0, 0, 1, 1)
        css = "*{background-color:%s;color:%s;border:0;height:25px;font:YaHei;} :pressed{background-color:%s;color:%s;}" % (
            random_color(mode='background'), random_color(mode='font'), random_color(mode='background'),
            random_color(mode='font'))
        self.txedit_imsearch_child_content.setStyleSheet(css)
        self.txedit_imsearch_child_content.setVisible(True)

        return self.glayout_imsearch_child

    @catch_except
    def imsearch_child_ok_clicked(self,*args):
        """访问API"""
        mode = self.imsearch_child_mode
        result = {}
        others = {}
        if mode in ['相同图片搜索入库','相同图片搜索更新','相似图片搜索入库','相似图片搜索更新']:
            filepath = self.lnedit_imsearch_child_img.text()
            if os.path.isfile(filepath):
                image = open(r'{}'.format(filepath), 'rb').read()
                option = {'image': base64.b64encode(image).decode()}
            else:
                option = {'url': filepath}
            brief = self.lnedit_imsearch_child_brief.text()
            tags = self.lnedit_imsearch_child_tags.text()
            option.update({'tags': tags, 'brief': brief})
            if mode == '相同图片搜索入库':
                result = self.ApiImsearch.sameHqAdd(option)
            elif mode == '相同图片搜索更新':
                result = self.ApiImsearch.sameHqUpdate(option)
            elif mode == '相似图片搜索入库':
                result = self.ApiImsearch.similarAdd(option)
            elif mode == '相似图片搜索更新':
                result = self.ApiImsearch.similarUpdate(option)
        elif mode in ['相同图片搜索检索','相似图片搜索检索']:
            filepath = self.lnedit_imsearch_child_img.text()
            if os.path.isfile(filepath):
                image = open(r'{}'.format(filepath), 'rb').read()
                option = {'image': base64.b64encode(image).decode()}
            else:
                option = {'url': filepath}
            brief = self.lnedit_imsearch_child_brief.text()
            tags = self.lnedit_imsearch_child_tags.text()
            class_id1 = self.lnedit_imsearch_child_class_id1.text()
            class_id2 = self.lnedit_imsearch_child_class_id2.text()
            tag_logic = self.cmbox_imsearch_child_tag_logic.currentText()
            pn = self.spb_imsearch_child_pn.text()
            rn = self.spb_imsearch_child_rn.text()

            option.update({'tags': tags, 'brief': brief,'class_id1':class_id1,'class_id2':class_id2,'tag_logic':tag_logic,'pn':pn,'rn':rn})
            if mode == '相同图片搜索检索':
                result = self.ApiImsearch.sameHqSearch(option)
            elif mode == '相似图片搜索检索':
                result = self.ApiImsearch.similarSearch(option)

        elif mode in ['相同图片搜索删除','相似图片搜索删除','商品图片搜索删除']:
            filepath = self.lnedit_imsearch_child_img.text()
            if os.path.isfile(filepath):
                image = open(r'{}'.format(filepath), 'rb').read()
                option = {'image': base64.b64encode(image).decode()}
            else:
                if 'http' in filepath or 'www.' in filepath:
                    option = {'url': filepath}
                else: option = {'cont_sign':filepath}
            if mode == '相同图片搜索删除':
                result = self.ApiImsearch.sameHqDelete(option)
            elif mode == '相似图片搜索删除':
                result = self.ApiImsearch.similarDelete(option)
            elif mode == '商品图片搜索删除':
                result = self.ApiImsearch.productDelete(option)

        elif mode in ['商品图片搜索入库','商品图片搜索更新']:
            filepath = self.lnedit_imsearch_child_img.text()
            if os.path.isfile(filepath):
                image = open(r'{}'.format(filepath), 'rb').read()
                option = {'image': base64.b64encode(image).decode()}
            else:
                option = {'url': filepath}
            brief = self.lnedit_imsearch_child_brief.text()
            class_id1 = self.lnedit_imsearch_child_class_id1.text()
            class_id2 = self.lnedit_imsearch_child_class_id2.text()

            option.update({'class_id1': class_id1,'class_id2':class_id2,'brief': brief})
            if mode == '商品图片搜索入库':
                result = self.ApiImsearch.productAdd(option)
            elif mode == '商品图片搜索更新':
                result = self.ApiImsearch.sameHqUpdate(option)

        elif mode in ['商品图片搜索检索']:
            filepath = self.lnedit_imsearch_child_img.text()
            if os.path.isfile(filepath):
                image = open(r'{}'.format(filepath), 'rb').read()
                option = {'image': base64.b64encode(image).decode()}
            else:
                option = {'url': filepath}
            brief = self.lnedit_imsearch_child_brief.text()
            tags = self.lnedit_imsearch_child_tags.text()
            class_id1 = self.lnedit_imsearch_child_class_id1.text()
            class_id2 = self.lnedit_imsearch_child_class_id2.text()
            tag_logic = self.cmbox_imsearch_child_tag_logic.currentText()
            pn = self.spb_imsearch_child_pn.text()
            rn = self.spb_imsearch_child_rn.text()

            option.update({'tags': tags, 'brief': brief,'class_id1':class_id1,'class_id2':class_id2,'tag_logic':tag_logic,'pn':pn,'rn':rn})
            result = self.ApiImsearch.productSearch(option)

        self.imsearch_child_result_deal(mode,result,others)

    def imsearch_child_result_deal(self,mode,datas,option,*args):
        """结果处理"""
        content = '{}-->完成\n'.format(mode)
        content = self.dict_get_value(datas,content)
        self.txedit_imsearch_child_content.setText(content)
        
        
        

    def resizeEvent_imsearch(self, a0: QtGui.QResizeEvent) -> None:
        value = int(self.width()*0.2 /6)
        self.glayout_imsearch_home.setSpacing(value)
        self.glayout_imsearch_home.setSpacing(value)



    def btn_imsearch_child_img_clicked(self,*args):
        file = QFileDialog.getOpenFileName(self,'图片','./','AllFile (*)')
        if file[0]:
            self.lnedit_imsearch_child_img.setText(file[0])