from ToolBox.main_ui import *

class ImgUp(Ui):
    def __init__(self):
        super(ImgUp, self).__init__()
        self.__init_imup_home_ui()
        self.__init_imup_child_ui()

        self.ApiImup = imageprocess.AipImageProcess(self.APPID,self.APIKEY,self.SECRETKEY)

        self.btn_home_imgup.clicked.connect(self.imup_home_reload)

    def __init_imup_home_ui(self):
        self.glayout_imup_home = QGridLayout()
        self.glayout_imup_home.setObjectName('grade_2')
        self.glayout_main.addLayout(self.glayout_imup_home,2,0,Qt.AlignCenter)
        self.btn_imup_home_1 = QPushButton("图像去雾")
        self.btn_imup_home_2 = QPushButton("图像对比度增加")
        self.btn_imup_home_3 = QPushButton("图像无损放大")
        self.btn_imup_home_4 = QPushButton("黑白图像上色")
        self.btn_imup_home_5 = QPushButton("拉伸图像恢复")
        self.btn_imup_home_6 = QPushButton("图像风格转换")
        self.btn_imup_home_7 = QPushButton("图像修复")
        
        self.imup_home_btns = [self.btn_imup_home_1,self.btn_imup_home_2,self.btn_imup_home_3,self.btn_imup_home_4,self.btn_imup_home_5,self.btn_imup_home_6,self.btn_imup_home_7]
        
        h = self.height() * 0.8 / 5
        w = self.width() * 0.8 / 4
        if h > 100: h = 100
        if w > h * 1.3: w = h * 1.3
        if h > w / 1.3: h = w / 1.3
        row,col = 0,0
        for btn in self.imup_home_btns:
            self.glayout_imup_home.addWidget(btn,row,col,1,1)
            # btn.setFixedSize(w,h)
            css = "*{width:%d;height:%d;}" \
                  ":hover{background-color:%s;}" \
                  "QPushButton{background-color:%s;}" \
                  "QPushButton:pressed{background-color:%s;}" \
                  "QToolTip{color:%s;font:Yahei;font-size:14px;}" %(w,h,random_color(),random_color(),random_color(),random_color()) # border:0px
            btn.setStyleSheet(css)
            btn.setFixedSize(QSize(w, h))
            btn.clicked.connect(self.imup_home_btns_clicked)
            btn.setVisible(False)
            col += 1
            if col > 2:
                col = 0
                row += 1
        self.glayout_imup_home.setSpacing(int(self.width()*0.2/6))
        self.glayout_imup_home.setContentsMargins(10,10,10,10)


    @layout_dele
    def imup_home_reload(self,*args):

        if func_historys[3]:
            self.btn_top_forward.setVisible(True)
        else:self.btn_top_forward.setVisible(False)


        for btn in self.imup_home_btns:
            btn.setVisible(True)

        return self.glayout_imup_home

    def imup_home_btns_clicked(self,*args):
        self.imup_child_mode = self.sender().text().replace('\n','')
        # print(self.imup_child_mode)
        self.imup_child_ui_reload()

    def __init_imup_child_ui(self,*args):

        self.glayout_imup_child = QGridLayout()
        self.glayout_main.addLayout(self.glayout_imup_child,2,0)
        self.glayout_imup_child.setObjectName('grade_3')

        self.glayout_imup_child_params = QGridLayout()
        self.glayout_imup_child.addLayout(self.glayout_imup_child_params,0,0,Qt.AlignTop)

        self.glayout_imup_child_content = QGridLayout()
        self.glayout_imup_child.addLayout(self.glayout_imup_child_content,0,1)

        self.label_imup_child_title = QLabel() #0
        self.btn_imup_child_ok = QPushButton('提交')#1
        self.btn_imup_child_ok.clicked.connect(self.imup_child_ok_clicked)
        self.label_imup_child_option = QLabel('可选参数')#2
        self.btn_imup_child_img = QPushButton('图片')#3
        self.btn_imup_child_img.clicked.connect(self.imup_child_img_clicked)
        self.lnedit_imup_child_img = MLineEdit()
        self.lnedit_imup_child_img.setClearButtonEnabled(True)
        self.label_imup_child_img_option = QLabel('风格')#4
        self.cmbox_imup_child_img_option = QComboBox()
        self.cmbox_imup_child_img_option.addItems(['cartoon','pencil','painting'])

        self.imup_child_widgets = [[self.label_imup_child_title],[self.btn_imup_child_ok],[self.label_imup_child_option],
                                   [self.btn_imup_child_img,self.lnedit_imup_child_img],[self.label_imup_child_img_option,self.cmbox_imup_child_img_option],
                                   ]

    @layout_dele
    def imup_child_ui_reload(self,*args):
        """子窗口重载"""
        self.imup_child_params = []
        mode = self.imup_child_mode
        self.label_imup_child_title.setText(mode)
        if mode in ["图像去雾","图像对比度增加","图像无损放大","黑白图像上色","拉伸图像恢复"]:
            self.imup_child_params = [3]
        elif mode in ["图像风格转换"]:
            self.imup_child_params = [3,4]


        
        if self.imup_child_params:
            self.imup_child_params.insert(0,0)
            self.imup_child_params.append(1)
            for index, i in enumerate(self.imup_child_params):
                widgets = self.imup_child_widgets[i]
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
                        self.glayout_imup_child_params.addWidget(widget, index, 0, 1, 2)
                        continue
                    elif j == 0:
                        widget.setFixedWidth(80)
                    else:
                        w = self.width() // 3
                        if w > 300: w = 300
                        widget.setFixedWidth(w)

                    self.glayout_imup_child_params.addWidget(widget, index, j, 1, 1)

                # 结果显示控件加载
            self.txedit_imup_child_content = QTextEdit()
            self.glayout_imup_child_content.addWidget(self.txedit_imup_child_content, 0, 0, 1, 1)
            css = "*{background-color:%s;color:%s;border:0;height:25px;font:YaHei;} :pressed{background-color:%s;color:%s;}" % (
                random_color(mode='background'), random_color(mode='font'), random_color(mode='background'),
                random_color(mode='font'))
            self.txedit_imup_child_content.setStyleSheet(css)
            self.txedit_imup_child_content.setVisible(True)

        return self.glayout_imup_child


    def imup_child_ok_clicked(self,*args):
        mode = self.imup_child_mode
        result = {}
        others = {}
        if mode in ["图像去雾","图像对比度增加","图像无损放大","黑白图像上色","拉伸图像恢复"]:
            filepath = self.lnedit_imup_child_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()
            if mode == '图像去雾':
                result = self.ApiImup.dehaze(image)
            elif mode == '图像对比度增加':
                result = self.ApiImup.stretch_restore(image)
            elif mode == '图像无损放大':
                result = self.ApiImup.imageQualityEnhance(image)
            elif mode == '黑白图像上色':
                result = self.ApiImup.colourize(image)
            elif mode == '拉伸图像恢复':
                result = self.ApiImup.stretch_restore(image)
            others.update({'filepath':filepath})
        elif mode == '图像风格转换':
            filepath = self.lnedit_imup_child_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self, '提示', '图片不存在', QMessageBox.Cancel)
                return None
            image = open(r'{}'.format(filepath), 'rb').read()
            option = self.cmbox_imup_child_img_option.currentText()
            options = {'option':option}
            result = self.ApiImup.style_trans(image,options)

        self.imup_child_result_deal(mode,result,others)

    @catch_except
    def imup_child_result_deal(self,mode,datas,option=None,*args):
        """结果处理"""
        if datas.get('log_id'):
            _session_id = time.strftime('%m%d%H%M%S', time.localtime()) + str(random.randint(0, 9))
            filepath = option.get('filepath')
            if filepath:
                filepath = filepath.replace('\\','/')
                name = re.findall('(.*)/(.*)\.(.*?)$',filepath)
                name = name[0][1] if name else _session_id
            else:name = _session_id
            path = r'{}\Record\Img\Imgup\{}.png'.format(ROOTDIR,name)
            if os.path.isfile(path):path = r'{}\Record\Img\Imgup\{}.png'.format(ROOTDIR,_session_id)
            with open(path,'wb') as f:
                f.write(base64.b64decode(datas.get('image')))
            content = '{} --> 完成\n'.format(mode)
            content += 'log_id:{}\n保存在：{}'.format(datas.get('log_id'),path)
            self.txedit_imup_child_content.setText(content)
        else:
            content = '{}\n'.format(mode)
            content = self.dict_get_value(datas,content)
            self.txedit_imup_child_content.setText(content)

    def imup_child_img_clicked(self,*args):
        file = QFileDialog().getOpenFileName(self,'图片',ROOTDIR,'AllFile(*)')
        if file[0]:self.lnedit_imup_child_img.setText(file[0])

    def resizeEvent_imup(self, a0: QtGui.QResizeEvent) -> None:
        value = int(self.width()*0.2 /6)
        self.glayout_imup_home.setSpacing(value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    UI = ImgUp()
    UI.show()
    sys.exit(app.exec_())