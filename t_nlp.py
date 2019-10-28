from ToolBox.main_ui import *


class Nlp(Ui):
    def __init__(self):
        super(Nlp, self).__init__()
        self.__init_nlp_home_ui()
        self.__nlp_child_ui()
        self.btn_home_nlp.clicked.connect(self.nlp_home_reload)
        self.Apinlp = AipNlp(self.APPID,self.APIKEY,self.SECRETKEY)

    def __init_nlp_home_ui(self,*args):
        """自然语言处理主页初始化"""
        self.glayout_nlp_home = QGridLayout()
        self.glayout_main.addLayout(self.glayout_nlp_home,2,0,Qt.AlignCenter)
        self.glayout_nlp_home.setObjectName('grade_2')

        self.btn_nlp_home_1 = QPushButton("词法分析")
        self.btn_nlp_home_2 = QPushButton("词法分析\n（定制版）")
        self.btn_nlp_home_3 = QPushButton("词向量表示")
        self.btn_nlp_home_4 = QPushButton("DNN语言模型")
        self.btn_nlp_home_5 = QPushButton("词义相似度")
        self.btn_nlp_home_6 = QPushButton("短文本相似度")
        self.btn_nlp_home_7 = QPushButton("评论观点抽取")
        self.btn_nlp_home_8 = QPushButton("情感倾向分析")
        self.btn_nlp_home_9 = QPushButton("文章标签")
        self.btn_nlp_home_10 = QPushButton("文本纠错")
        self.btn_nlp_home_11 = QPushButton("对话情绪\n识别接口")
        self.btn_nlp_home_12 = QPushButton("新闻摘要接口")
        self.btn_nlp_home_13 = QPushButton('文章分类')
        self.btn_nlp_home_14 = QPushButton('依存词法分析')

        self.nlp_home_btns = [self.btn_nlp_home_1,self.btn_nlp_home_2,self.btn_nlp_home_14,self.btn_nlp_home_3,self.btn_nlp_home_4,self.btn_nlp_home_5,self.btn_nlp_home_6,self.btn_nlp_home_7,self.btn_nlp_home_8,self.btn_nlp_home_9,self.btn_nlp_home_13,self.btn_nlp_home_10,self.btn_nlp_home_11,self.btn_nlp_home_12]
        
        self.glayout_nlp_home.setSpacing(int(self.width()*0.2/6))
        self.glayout_nlp_home.setContentsMargins(10,10,10,10)
        h = self.height() * 0.8 / 6
        w = self.width() * 0.8 / 5
        if h > 100: h = 100
        if w > h * 1.3: w = h * 1.3
        if h > w / 1.3: h = w / 1.3
        row,col = 0,0
        for btn in self.nlp_home_btns:
            self.glayout_nlp_home.addWidget(btn,row,col,1,1)
            css = "*{width:%dpx;height:%spx}" \
                  ":hover{background-color:%s;}" \
                  "QPushButton{background-color:%s;}" \
                  "QPushButton:pressed{background-color:%s;}" \
                  "QToolTip{color:%s;font:Yahei;font-size:14px}" %(w,h,random_color(),random_color(),random_color(),random_color()) # border:0px
            btn.setStyleSheet(css)
            btn.clicked.connect(self.nlp_home_btns_clicked)
            btn.setVisible(False)
            col += 1
            if col > 3:
                col = 0
                row += 1

    @layout_dele
    def nlp_home_reload(self,*args):
        if func_historys[3]:
            self.btn_top_forward.setVisible(True)
        else:self.btn_top_forward.setVisible(False)

        for btn in self.nlp_home_btns:
            btn.setVisible(True)

        return self.glayout_nlp_home

    def nlp_home_btns_clicked(self,*args):
        """nlp主页btn点击，监听点击btn调用子窗口重载函数"""
        if func_historys[4]:
            self.btn_top_forward.setVisible(True)
        else:self.btn_top_forward.setVisible(False)
        self.nlp_child_mode = self.sender().text().replace('\n','')
        self.nlp_child_reload()

    def __nlp_child_ui(self,*args):
        self.glayout_nlp_child = QGridLayout()
        self.glayout_main.addLayout(self.glayout_nlp_child,2,0)
        self.glayout_nlp_child.setObjectName('grade_3')

        self.glayout_nlp_child_params = QGridLayout()
        self.glayout_nlp_child.addLayout(self.glayout_nlp_child_params,0,0)

        self.galyout_nlp_child_content = QGridLayout()
        self.glayout_nlp_child.addLayout(self.galyout_nlp_child_content,0,1)

        self.label_nlp_child_title = QLabel()#0
        self.btn_nlp_child_ok = QPushButton('提交')#1
        self.btn_nlp_child_ok.clicked.connect(self.btn_nlp_child_ok_clicked)
        self.label_nlp_child_option = QLabel('可选参数')#2

        self.label_nlp_child_text = QLabel('文本')#3
        self.lnedit_nlp_child_text = QLineEdit()
        self.label_nlp_child_mode = QLabel('模型')
        self.cmbox_nlp_child_mode = QComboBox()
        self.cmbox_nlp_child_mode.addItems(['0','1'])#4
        self.label_nlp_child_estitle = QLabel('标题')#5
        self.lnedit_nlp_child_estitle = QLineEdit()
        self.txedit_nlp_child_escontent = QTextEdit()#6
        self.txedit_nlp_child_escontent.setPlaceholderText('文本')
        self.txedit_nlp_child_escontent2 = QTextEdit()
        self.txedit_nlp_child_escontent2.setPlaceholderText('文本2')#7
        self.label_nlp_child_model = QLabel('模型')#8
        self.cmbox_nlp_child_model = QComboBox()
        self.cmbox_nlp_child_model.addItems(['BOW','CNN','GRNN'])
        self.label_nlp_child_max_summary_len = QLabel('摘要长度')#9
        self.spb_nlp_child_max_summary_len = QSpinBox()
        self.spb_nlp_child_max_summary_len.setRange(1,10000)
        self.spb_nlp_child_max_summary_len.setValue(300)

        self.nlp_child_widgets = [[self.label_nlp_child_title],[self.btn_nlp_child_ok],[self.label_nlp_child_option],
                                  [self.label_nlp_child_text,self.lnedit_nlp_child_text],[self.label_nlp_child_mode,self.cmbox_nlp_child_mode],
                                  [self.label_nlp_child_estitle,self.lnedit_nlp_child_estitle],[self.txedit_nlp_child_escontent],
                                  [self.txedit_nlp_child_escontent2],[self.label_nlp_child_model,self.cmbox_nlp_child_model],
                                  [self.label_nlp_child_max_summary_len,self.spb_nlp_child_max_summary_len]]


    @layout_dele
    def nlp_child_reload(self,*args):
        """nlp子窗口重载"""
        if func_historys[4]:self.btn_top_forward.setVisible(True)
        else:self.btn_top_forward.setVisible(False)
        mode = self.nlp_child_mode
        self.label_nlp_child_title.setText(mode)
        self.txedit_nlp_child_escontent.setPlaceholderText('文本')
        self.txedit_nlp_child_escontent2.setPlaceholderText('文本2')
        self.nlp_child_params = []
        if mode in ['词法分析','词法分析（定制版）','词向量表示','DNN语言模型','评论观点抽取','情感倾向分析','文本纠错','对话情绪识别接口']:
            self.nlp_child_params = [6]
        elif mode in ['依存词法分析']:
            self.nlp_child_params = [4,6]
        elif mode in ['文章标签','文章分类']:
            self.nlp_child_params = [5,6]
        elif mode in ['词义相似度']:
            self.txedit_nlp_child_escontent.setPlaceholderText('词1')
            self.txedit_nlp_child_escontent2.setPlaceholderText('词2')
            self.nlp_child_params = [6,7]
        elif mode in ['短文本相似度']:
            self.nlp_child_params = [8,6,7]
        elif mode in ['新闻摘要接口']:
            self.txedit_nlp_child_escontent.setPlaceholderText('标题')
            self.nlp_child_params = [6,7,9]
        
        if self.nlp_child_params:
            # 添加标题和提交按钮
            self.nlp_child_params.insert(0, 0)
            self.nlp_child_params.append(1)
            for index, i in enumerate(self.nlp_child_params):
                widgets = self.nlp_child_widgets[i]
                for j, widget in enumerate(widgets):
                    widget.setVisible(True)
                    css = "*{background-color:%s;color:%s;border:0;height:25px;font:YaHei;} :pressed{background-color:%s;color:%s;}" % (
                        random_color(mode='background'), random_color(mode='font'), random_color(mode='background'),
                        random_color(mode='font'))
                    widget.setStyleSheet(css)
                    if widget.__doc__.startswith('QLabel'):
                        widget.setFixedHeight(25)
                        widget.setAlignment(Qt.AlignCenter)
                    elif widget.__doc__.startswith('QLineEdit'):
                        widget.setClearButtonEnabled(True)
                    elif widget.__doc__.startswith('QTextEdit'):
                        # widget.setMinimumHeight(60)
                        pass
                    if len(widgets) == 1:
                        self.glayout_nlp_child_params.addWidget(widget, index, 0, 1, 2)
                        # w = self.width() // 2
                        # h = self.height() // 2
                        # widget.resize(w,h)
                        continue
                    # elif j == 0:
                        # widget.setFixedWidth(80)
                    self.glayout_nlp_child_params.addWidget(widget, index, j, 1, 1)

        # 结果显示控件加载
        self.txedit_nlp_child_content = QTextEdit()
        self.galyout_nlp_child_content.addWidget(self.txedit_nlp_child_content, 0, 0, 1, 1)
        css = "*{background-color:%s;color:%s;border:0;height:25px;font:YaHei;} :pressed{background-color:%s;color:%s;}" % (
            random_color(mode='background'), random_color(mode='font'), random_color(mode='background'),
            random_color(mode='font'))
        self.txedit_nlp_child_content.setStyleSheet(css)
        self.txedit_nlp_child_content.setVisible(True)
        self.txedit_nlp_child_content.setMaximumWidth(500)

        return self.glayout_nlp_child

    @catch_except
    def btn_nlp_child_ok_clicked(self,*args):
        """访问API"""

        mode = self.nlp_child_mode
        result = {}
        others = {}
        if mode in ['词法分析','词法分析（定制版）','词向量表示','DNN语言模型','评论观点抽取','情感倾向分析','文本纠错','对话情绪识别接口']:
            text = self.txedit_nlp_child_escontent.toPlainText()
            if mode == '词法分析':
                result = self.Apinlp.lexer(text)
            elif mode == '词法分析（定制版）':
                result = self.Apinlp.lexerCustom(text)
            elif mode == '词向量表示':
                text = re.sub('\s','',text)
                result = self.Apinlp.wordEmbedding(text)
            elif mode == 'DNN语言模型':
                result = self.Apinlp.dnnlm(text)
            elif mode == '评论观点抽取':
                result = self.Apinlp.commentTag(text)
            elif mode == '情感倾向分析':
                result = self.Apinlp.sentimentClassify(text)
            elif mode == '文本纠错':
                result = self.Apinlp.ecnet(text)
            elif mode == '对话情绪识别接口':
                result = self.Apinlp.emotion(text)

        elif mode == '新闻摘要接口':
            content = self.txedit_nlp_child_escontent2.toPlainText()
            max_summary_len = self.spb_nlp_child_max_summary_len.text()
            title = self.txedit_nlp_child_escontent.toPlainText()
            option = {'title':title}
            result = self.Apinlp.newsSummary(content,max_summary_len,option)

        elif mode in ['文章标签','文章分类']:
            content = self.txedit_nlp_child_escontent.toPlainText()
            title = self.lnedit_nlp_child_estitle.text()
            if mode == '文章标签':
                result = self.Apinlp.keyword(title,content)
            elif mode == '文章分类':
                result = self.Apinlp.topic(title,content)


        elif mode in ['词义相似度','短文本相似度']:
            word_1 = self.txedit_nlp_child_escontent.toPlainText()
            word_2 = self.txedit_nlp_child_escontent2.toPlainText()
            model = self.cmbox_nlp_child_model.currentText()
            if mode == '词义相似度':
                result = self.Apinlp.wordSimEmbedding(word_1,word_2)
            elif mode == '短文本相似度':
                option = {'model': model}
                result = self.Apinlp.simnet(word_1,word_2,option)
        elif mode in ['依存词法分析']:
            word = self.txedit_nlp_child_escontent.toPlainText()
            mode = self.cmbox_nlp_child_mode.currentText()
            option = {'mode':mode}
            result = self.Apinlp.depParser(word,option)
            
        self.nlp_child_result_deal(mode,result,others)
    
    def nlp_child_result_deal(self,mode,datas,options=None,*args):
        content = '{} --> 完成\n'.format(mode)
        content = self.dict_get_value(datas,content)
        self.txedit_nlp_child_content.setText(content)


    def resizeEvent_nlp(self, a0: QtGui.QResizeEvent) -> None:
        value = int(self.width()*0.2 /6)
        self.glayout_nlp_home.setSpacing(value)