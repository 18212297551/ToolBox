# coding: utf-8
from PyQt5.QtGui import QPen

from ToolBox.main_ui import *

class Face(Ui):
    """
    人脸相关模块
    """
    @catch_except
    def __init__(self):
        super(Face,self).__init__()
        # 人脸主窗口
        self.glayout_face_home = QGridLayout()
        self.glayout_main.addLayout(self.glayout_face_home,2,0,Qt.AlignCenter)
        self.glayout_face_home.setObjectName('grade_2')
        self.btn_home_face.clicked.connect(self.face_home_reload)

        # 人脸子窗口
        self.glayout_face_child = QGridLayout()
        self.glayout_face_child.setObjectName('grade_3')
        self.glayout_main.addLayout(self.glayout_face_child,2,0)


        self.ApiFace = AipFace(self.APPID, self.APIKEY, self.SECRETKEY)

        # 当前人脸模块
        self.face_child_mode = None
        # 参数
        self.face_child_params = None

        self._init_face_ui_()
        self._init_face_child()


    def _init_face_ui_(self,*args):
        """人脸主页"""

        self.btn_face_home_detect = QPushButton()
        self.btn_face_home_match = QPushButton()
        self.btn_face_home_search = QPushButton()
        self.btn_face_home_multi_search = QPushButton()
        self.btn_face_home_merge = QPushButton()
        # 人脸库
        self.btn_face_home_delete = QPushButton()
        self.btn_face_home_user_add = QPushButton()
        self.btn_face_home_user_update = QPushButton()
        self.btn_face_home_user_delete = QPushButton()
        self.btn_face_home_user_get = QPushButton()
        self.btn_face_home_group_getlist = QPushButton()
        self.btn_face_home_group_getusers = QPushButton()
        self.btn_face_home_user_copy = QPushButton()
        self.btn_face_home_getlist = QPushButton() # 获取用户列表

        self.btn_face_home_group_add = QPushButton()
        self.btn_face_home_group_delete = QPushButton()

        self.btn_face_home_faceverify = QPushButton()
        self.btn_face_home_verify = QPushButton()
        self.btn_face_home_sessioncode = QPushButton()
        self.btn_face_home_rpc = QPushButton() # 视频监控

        self.btn_face_home_btns = [[self.btn_face_home_detect,'人脸检测'], [self.btn_face_home_match,'人脸对比'],
                                   [self.btn_face_home_search,'人脸搜素'],[self.btn_face_home_multi_search,'人脸搜索M:N'],
                                   [self.btn_face_home_merge,'人脸融合'],[self.btn_face_home_user_add,'人脸注册'],
                                   [self.btn_face_home_user_update,'人脸更新'],[self.btn_face_home_user_copy,'复制用户'],
                                   [self.btn_face_home_user_get,'用户信息查询'],[self.btn_face_home_getlist,'用户人脸列表'],
                                   [self.btn_face_home_group_getusers,'组用户列表'],
                                   [self.btn_face_home_group_getlist,'获取组列表'],[self.btn_face_home_group_add,'创建用户组'],
                                   [self.btn_face_home_delete,'删除人脸'],[self.btn_face_home_user_delete,'删除用户'],
                                   [self.btn_face_home_group_delete,'删除用户组'],[self.btn_face_home_faceverify,'在线活体检测'],
                                   [self.btn_face_home_verify,'活体视频分析'], [self.btn_face_home_sessioncode,'语音验证码']]
        # [self.btn_face_home_rpc,'智能视频监控'],
        #                                    [self.btn_face_home_sessioncode,'语音验证码']

        self.glayout_face_home.setSpacing(int(self.width()*0.2/6))
        self.glayout_face_home.setContentsMargins(10,10,10,10)
        h = self.height() * 0.8 / 6
        w = self.width() * 0.8 / 5
        if h > 100: h = 100
        if w > h * 1.3: w = h * 1.3
        if h > w / 1.3: h = w / 1.3
        row,col = 0,0
        for btn in self.btn_face_home_btns:
            self.glayout_face_home.addWidget(btn[0],row,col,1,1)
            btn[0].setText(btn[1])
            css = "*{width:%dpx;height:%spx}" \
                  ":hover{background-color:%s;}" \
                  "QPushButton{background-color:%s;}" \
                  "QPushButton:pressed{background-color:%s;}" \
                  "QToolTip{color:%s;font:Yahei;font-size:14px}" %(w,h,random_color(),random_color(),random_color(),random_color()) # border:0px
            #background-color:%s; random_color(),
            btn[0].setStyleSheet(css)
            btn[0].clicked.connect(self.face_home_btns_clicked)
            btn[0].setVisible(False)
            # btn[0].setFixedSize(QSize(h*1.3,h ))

            col += 1
            if col > 4:
                col = 0
                row += 1



    @layout_dele
    def face_home_reload(self, *args):
        """人脸主页重载"""
        # 更新forward btn
        if func_historys[3]:
            self.btn_top_forward.setVisible(True)
        else:
            self.btn_top_forward.setVisible(False)

        for btn in self.btn_face_home_btns:
            btn[0].setVisible(True)

        return self.glayout_face_home

    @catch_except
    def face_home_btns_clicked(self,*args):
        """人脸主页子控件点击"""
        sender = self.sender()
        # print(sender.text())
        self.face_child_mode = sender.text()
        self.face_child_reload()



    @catch_except
    def _init_face_child(self,*args):
        """child控件初始化"""


        self.glayout_face_child_param = QGridLayout() # 参数列表
        self.glayout_face_child.addLayout(self.glayout_face_child_param,0,0,Qt.AlignTop) # ,Qt.AlignTop

        self.glayout_face_child_content = QGridLayout()
        self.glayout_face_child.addLayout(self.glayout_face_child_content,0,1)

        self.btn_face_child_folder = QPushButton()
        self.btn_face_child_folder.setText('图片') # 0
        self.btn_face_child_folder.setIcon(QIcon('{}/Ico/floder.png'.format(ROOTDIR)))
        self.btn_face_child_folder.clicked.connect(self.btn_face_child_folder_clicked)
        self.lnedit_face_child_img = QLineEdit()
        self.lnedit_face_child_img.setPlaceholderText('图片路径(BASE64)、URL、人脸唯一标识')
        self.label_face_child_imgtype = QLabel()
        self.label_face_child_imgtype.setText('图片类型') # 1
        self.cmbox_face_child_imgtype = QComboBox()
        imgtype = ['BASE64', 'URL', 'FACE_TOKEN']
        self.cmbox_face_child_imgtype.addItems(imgtype)
        self.label_face_child_facetype = QLabel()
        self.label_face_child_facetype.setText('人脸类型') # 2
        self.cmbox_face_child_facetype = QComboBox()
        ftype = ['LIVE', 'IDCARD', 'WATERMARK', 'CERT']
        self.cmbox_face_child_facetype.addItems(ftype)
        self.label_face_child_liveness_control = QLabel()
        self.label_face_child_liveness_control.setText('活体检测') # 3
        self.cmbox_face_child_liveness_control = QComboBox()
        liveness = ['NONE', 'LOW', 'NORMAL', 'HIGH']
        self.cmbox_face_child_liveness_control.addItems(liveness)

        self.label_face_child_userid = QLabel()
        self.label_face_child_userid.setText('用户ID') # 4
        self.lnedit_face_child_userid = QLineEdit()
        self.label_face_child_groupid = QLabel()
        self.label_face_child_groupid.setText('用户组ID') # 5
        self.lnedit_face_child_groupid = QLineEdit()
        self.label_face_child_facefield = QLabel()
        self.label_face_child_facefield.setText('获取字段') # 6
        self.lnedit_face_child_facefield = QLineEdit()
        self.label_face_child_maxface = QLabel()
        self.label_face_child_maxface.setText('最多人脸数') # 7
        self.spb_face_child_maxface = QSpinBox()
        self.spb_face_child_maxface.setRange(1,10)
        self.btn_face_child_folder2 = QPushButton() # 8
        self.btn_face_child_folder2.setText('图片2')
        self.btn_face_child_folder2.clicked.connect(self.btn_face_child_folder2_clicked)

        self.btn_face_child_folder2.setIcon(QIcon('{}/Ico/floder.png'.format(ROOTDIR)))
        self.lnedit_face_child_img2 = QLineEdit()
        self.lnedit_face_child_img2.setPlaceholderText('图片路径(BASE64)、URL、人脸唯一标识')
        self.label_face_child_imgtype2 = QLabel()
        self.label_face_child_imgtype2.setText('图片类型2') # 9
        self.cmbox_face_child_imgtype2 = QComboBox()
        imgtype = ['BASE64', 'URL', 'FACE_TOKEN']
        self.cmbox_face_child_imgtype2.addItems(imgtype)


        self.btn_face_child_ok = QPushButton() #确认 10
        self.btn_face_child_ok.setText('提交')

        self.label_face_child_quality = QLabel()
        self.label_face_child_quality.setText('图片质量') # 11
        self.cmbox_face_child_quality = QComboBox()
        quality = ['NONE','LOW','NORMAL','HIGH']
        self.cmbox_face_child_quality.addItems(quality)

        self.label_face_child_threshold = QLabel()
        self.label_face_child_threshold.setText('匹配阈值') # 12
        self.spb_face_child_threshold = QSpinBox()
        self.spb_face_child_threshold.setRange(0,100)
        self.spb_face_child_threshold.setValue(80)
        self.label_face_child_maxuser = QLabel()
        self.label_face_child_maxuser.setText('返回用户数量') # 13
        self.spb_face_child_maxuser = QSpinBox()
        self.spb_face_child_maxuser.setRange(1,50)
        self.label_face_child_actiontype = QLabel()
        self.label_face_child_actiontype.setText('操作方式') # 14
        self.cmbox_face_child_actiontype = QComboBox()
        actiontype = ['APPEND','REPLACE ']
        self.cmbox_face_child_actiontype.addItems(actiontype)
        self.label_face_child_user_info = QLabel()
        self.label_face_child_user_info.setText('用户资料') #15
        self.lnedit_face_child_user_info = QLineEdit()
        self.label_face_child_option = QLabel()
        self.label_face_child_option.setText('可选参数') # 16
        #age,beauty,expression,face_shape,gender,glasses,landmark,landmark150,race,quality,eye_status,emotion,face_type信息
        self.label_face_child_option.setAlignment(Qt.AlignCenter)
        self.label_face_child_title = QLabel() #顶部标题 17
        self.label_face_child_title.setAlignment(Qt.AlignCenter)
        self.label_face_child_mergedegree = QLabel()
        self.label_face_child_mergedegree.setText('融合度') # 18
        self.cmbox_face_child_mergedegree = QComboBox()
        mergedegree = ['NORMAL','LOW','HIGH','COMPLETE']
        self.cmbox_face_child_mergedegree.addItems(mergedegree)
        self.label_face_child_optioninfo = QLabel()
        self.label_face_child_optioninfo.setText('场景信息') # 19
        self.cmbox_face_child_optioninfo = QComboBox()
        optioninfo = ['COMMON','OLD_PHOTO']
        self.cmbox_face_child_optioninfo.addItems(optioninfo)
        self.label_face_child_facelocation = QLabel()
        self.label_face_child_facelocation.setText('模板人脸位置') # 20
        self.lnedit_face_child_facelocation = QLineEdit()
        self.label_face_child_facelocation2 = QLabel()
        self.label_face_child_facelocation2.setText('目标人脸位置') # 21
        self.lnedit_face_child_facelocation2 = QLineEdit()
        self.label_face_child_user_info = QLabel()
        self.label_face_child_user_info.setText('用户信息') # 22
        self.lnedit_face_child_user_info = QLineEdit()
        self.label_face_child_groupid2 = QLabel()
        self.label_face_child_groupid2.setText('目标用户组ID') # 23
        self.lnedit_face_child_groupid2 = QLineEdit()
        self.label_face_index_start = QLabel()
        self.label_face_index_start.setText('起始序号') # 24
        self.spb_face_child_index_start = QSpinBox()
        self.spb_face_child_index_start.setValue(0)
        self.label_face_child_length = QLabel()
        self.label_face_child_length.setText('返回数量') # 25
        self.spb_face_child_length = QSpinBox()
        self.spb_face_child_length.setRange(0,1000)
        self.spb_face_child_length.setValue(100)
        self.label_face_child_face_token = QLabel()
        self.label_face_child_face_token.setText('人脸token') # 26
        self.lnedit_face_child_face_token = QLineEdit()
        self.btn_face_child_folder3 = QPushButton()
        self.btn_face_child_folder3.setText('视频')
        self.btn_face_child_folder3.clicked.connect(self.btn_face_child_folder3_clicked)
        self.btn_face_child_folder3.setIcon(QIcon('{}/Ico/floder.png'.format(ROOTDIR))) # 27
        self.lnedit_face_child_video = QLineEdit()
        self.lnedit_face_child_video.setToolTip('视频路径')
        self.label_face_child_imgcut = QLabel('生成人脸图') # 28
        self.cmbox_face_child_imgcut = QComboBox()
        self.cmbox_face_child_imgcut.addItems(['NONE','CROP','DRAW','ALL'])
        self.label_face_child_changepos = QLabel('人脸位置调整')# 29
        self.lnedit_face_child_changepos = QLineEdit()
        self.label_face_child_deal_type = QLabel('处理途径') #30
        self.cmbox_face_child_deal_type = QComboBox()
        self.cmbox_face_child_deal_type.addItems(['NET','LOCAL','ALL'])




        self.face_child_widgets = [[self.btn_face_child_folder,self.lnedit_face_child_img],[self.label_face_child_imgtype,self.cmbox_face_child_imgtype],
                                   [self.label_face_child_facetype,self.cmbox_face_child_facetype],[self.label_face_child_liveness_control,self.cmbox_face_child_liveness_control],
                                   [self.label_face_child_userid,self.lnedit_face_child_userid],[self.label_face_child_groupid,self.lnedit_face_child_groupid],
                                   [self.label_face_child_facefield,self.lnedit_face_child_facefield],[self.label_face_child_maxface,self.spb_face_child_maxface],
                                   [self.btn_face_child_folder2,self.lnedit_face_child_img2],[self.label_face_child_imgtype2,self.cmbox_face_child_imgtype2],
                                   [self.btn_face_child_ok], [self.label_face_child_quality,self.cmbox_face_child_quality],
                                   [self.label_face_child_threshold,self.spb_face_child_threshold],[self.label_face_child_maxuser,self.spb_face_child_maxuser],
                                   [self.label_face_child_actiontype,self.cmbox_face_child_actiontype],[self.label_face_child_user_info,self.lnedit_face_child_user_info],
                                   [self.label_face_child_option],[self.label_face_child_title],[self.label_face_child_mergedegree,self.cmbox_face_child_mergedegree],
                                   [self.label_face_child_optioninfo,self.cmbox_face_child_optioninfo],[self.label_face_child_facelocation,self.lnedit_face_child_facelocation],
                                   [self.label_face_child_facelocation2,self.lnedit_face_child_facelocation2],[self.label_face_child_user_info,self.lnedit_face_child_user_info],
                                   [self.label_face_child_groupid2,self.lnedit_face_child_groupid2],[self.label_face_index_start,self.spb_face_child_index_start],
                                   [self.label_face_child_length,self.spb_face_child_length],[self.label_face_child_face_token,self.lnedit_face_child_face_token],
                                   [self.btn_face_child_folder3,self.lnedit_face_child_video],[self.label_face_child_imgcut,self.cmbox_face_child_imgcut],
                                   [self.label_face_child_changepos,self.lnedit_face_child_changepos],[self.cmbox_face_child_deal_type,self.cmbox_face_child_deal_type],
                                   ]

        for widgets in self.face_child_widgets:
            for widget in widgets:
                widget.setVisible(False)

        # 事件关联
        self.btn_face_child_ok.clicked.connect(self.btn_face_child_ok_clicked)

    @layout_dele
    def face_child_reload(self, *args):
        """窗体布局实现"""

        # 更新forward btn
        if func_historys[4]:
            self.btn_top_forward.setVisible(True)
        else:
            self.btn_top_forward.setVisible(False)

        optioninfo = ['COMMON', 'OLD_PHOTO']
        self.cmbox_face_child_optioninfo.clear()
        self.cmbox_face_child_optioninfo.addItems(optioninfo)
        # 模块参数 title 17, option 16, ok 10, img 0, imgt 1, live 3, userid 4,groupid 5,field 6,maxface 7,
        # img2 8,imgt2 9,quality 11,faceloaction 20 faceloaction2 21 userinfo 22, 目标用户组ID 23
        # 阈值 12， maxuser 13, action 14, userinfo 15,融合度 18,,optioninfo 19, start 24,length 25 ,video27
        if self.face_child_mode == '人脸检测':
            self.label_face_child_title.setText('人脸检测')
            self.face_child_params = [17,0,1,2,7,3,28,16,6,29,10]
        elif self.face_child_mode == '语音验证码':
            self.face_child_params = [17,16,4,10]

        elif self.face_child_mode == '活体视频分析':
            self.label_face_child_title.setText(self.face_child_mode)
            self.face_child_params = [17,27,10]
        elif self.face_child_mode == '在线活体检测':
            self.label_face_child_title.setText(self.face_child_mode)
            self.face_child_params = [17,0,1,19,16,6,10]
            optioninfo = ['COMMON', 'GATE']
            self.cmbox_face_child_optioninfo.clear()
            self.cmbox_face_child_optioninfo.addItems(optioninfo)

        elif self.face_child_mode == '获取组列表':
            self.label_face_child_title.setText(self.face_child_mode)
            self.face_child_params = [17,24,25,10]

        elif self.face_child_mode == '删除用户组':
            self.label_face_child_title.setText(self.face_child_mode)
            self.face_child_params = [17,5,10]

        elif self.face_child_mode == '删除人脸':
            self.label_face_child_title.setText(self.face_child_mode)
            self.face_child_params = [17,4,5,26,10]

        elif self.face_child_mode == '创建用户组':
            self.label_face_child_title.setText(self.face_child_mode)
            self.face_child_params = [17,5,10]

        elif self.face_child_mode == '组用户列表':
            self.label_face_child_title.setText(self.face_child_mode)
            self.face_child_params = [17,5,24,25,10]

        elif self.face_child_mode in ['用户信息查询','用户人脸列表','删除用户']:
            self.label_face_child_title.setText(self.face_child_mode)
            self.face_child_params = [17,4,5,10]

        elif self.face_child_mode == '复制用户':
            self.label_face_child_title.setText('复制用户')
            self.face_child_params = [17,4,5,23,10]

        elif self.face_child_mode in ['人脸更新', '人脸注册']:
            self.label_face_child_title.setText(self.face_child_mode)
            self.face_child_params = [17,0,1,5,4,11,3,14,16,22,10]
            if self.face_child_mode == '人脸更新':
                self.cmbox_face_child_actiontype.removeItem(0)
                self.cmbox_face_child_actiontype.insertItem(0,'UPDATE')
                self.cmbox_face_child_actiontype.setCurrentIndex(0)
            elif self.face_child_mode == '人脸注册':
                self.cmbox_face_child_actiontype.removeItem(0)
                self.cmbox_face_child_actiontype.insertItem(0, 'APPEND')
                self.cmbox_face_child_actiontype.setCurrentIndex(0)



        elif self.face_child_mode == '人脸融合':
            self.label_face_child_title.setText('人脸融合')
            self.face_child_params = [17,0,1,8,9,11,18,16,20,21,10]
            self.btn_face_child_folder.setText('模板图')
            self.btn_face_child_folder2.setText('目标图')
        elif self.face_child_mode == '人脸对比':
            self.label_face_child_title.setText('人脸对比')
            self.face_child_params = [17,0,1,8,9,11,2,3,10]

        elif self.face_child_mode == '用户人脸列表':
            self.label_face_child_title.setText('用户人脸列表')
            self.face_child_params = [17,4,5,10]

        elif self.face_child_mode == '人脸搜素':
            self.label_face_child_title.setText('人脸搜素')
            self.face_child_params = [17,0,1,5,11,13,3,16,4,10]

        elif self.face_child_mode == '人脸搜索M:N':
            self.label_face_child_title.setText('人脸搜索M:N')
            self.face_child_params = [17,0,1,5,7,13,12,11,3,10]
        else:
            self.face_child_params = None

        for index, widgets in enumerate(self.face_child_widgets):
            if self.face_child_params:
                if index in self.face_child_params:
                    continue
            for widget in widgets:
                widget.setVisible(False)



        if self.face_child_params:
            for index,i in enumerate(self.face_child_params):
                widget = self.face_child_widgets[i]
                widget[0].setVisible(True)

                if widget[0] == self.btn_face_child_ok:
                    self.glayout_face_child_param.addWidget(widget[0],index,0,1,2)
                    widget[0].setStyleSheet(
                        "*{background-color:%s;color:%s;border:0;height:25px;font:YaHei;} :pressed{background-color:%s;color:%s;}" % (
                        random_color(mode='background'), random_color(mode='font'), random_color(mode='background'),
                        random_color(mode='font')))
                    continue
                if widget[0] in [self.label_face_child_title,self.label_face_child_option]:
                    self.glayout_face_child_param.addWidget(widget[0],index,0,1,2)
                    widget[0].setStyleSheet("*{background-color:%s;color:%s;border:0;font:YaHei;} :pressed{background-color:%s;color:%s;}"%(random_color(mode='background'),random_color(mode='font'),random_color(mode='background'),random_color(mode='font')))
                    widget[0].setFixedHeight(25)
                    continue

                widget[1].setVisible(True)

                widget[0].setStyleSheet("*{background-color:%s;color:%s;border:0;height:25px;font:YaHei;} :pressed{background-color:%s;color:%s;}"%(random_color(mode='background'),random_color(mode='font'),random_color(mode='background'),random_color(mode='font')))

                widget[1].setStyleSheet("*{background-color:%s;color:%s;border:0;height:25px;width:80px;font:YaHei;} :pressed{background-color:%s;color:%s;}"%(random_color(mode='background'),random_color(mode='font'),random_color(mode='background'),random_color(mode='font')))
                self.glayout_face_child_param.addWidget(widget[0],index,0,1,1)
                self.glayout_face_child_param.addWidget(widget[1],index,1,1,1)
                w = self.width() // 3
                if w > 300: w = 300
                widget[1].setFixedWidth(w)
                widget[0].setFixedWidth(80)
                # 文字居中
                if widget[0].__doc__.startswith('QLabel'):
                    widget[0].setAlignment(Qt.AlignCenter)

                if widget[1].__doc__.startswith('QLineEdit'):
                    widget[1].setClearButtonEnabled(True)


        self.txedit_face_child_content = QTextEdit()
        self.glayout_face_child_content.addWidget(self.txedit_face_child_content,0,0,1,1)
        self.txedit_face_child_content.setStyleSheet(
            "*{background-color:%s;color:%s;border:0;height:25px;width:80px;font:YaHei;} :pressed{background-color:%s;color:%s;}" % (
                random_color(mode='background'), random_color(mode='font'), random_color(mode='background'),
                random_color(mode='font')))


        # 返回布局以便退出隐藏
        return self.glayout_face_child

    @catch_except
    def btn_face_child_ok_clicked(self,*args):
        """API访问实现"""

        # 局部变量代替全局变量
        current_mode = self.face_child_mode
        self.label_status_left.setText(current_mode)
        self.pbar_bottom.setValue(1)
        self.label_status_right.setText('正在处理...')

        result = None
        others = {} # 传入处理函数的可选参数
        self.label_status_left.setText(current_mode)
        self.pbar_bottom.setValue(5) # 进度条更新
        if current_mode == '人脸检测':
            filepath = self.lnedit_face_child_img.text()

            if not os.path.isfile(filepath):
                QMessageBox.warning(self,'提示','图片不存在',QMessageBox.Cancel)
                return None
            image = base64.b64encode(open(r'{}'.format(filepath),'rb').read()).decode()


            image_type = self.cmbox_face_child_imgtype.currentText()
            face_type = self.cmbox_face_child_facetype.currentText()
            face_field = self.lnedit_face_child_facefield.text()
            max_face_num = self.spb_face_child_maxface.text()
            liveness_control = self.cmbox_face_child_liveness_control.currentText()

            option = {}
            if face_field: option['face_field'] = face_field
            if max_face_num: option['max_face_num'] = max_face_num
            if liveness_control: option['liveness_control'] = liveness_control
            if face_type: option['face_type'] = face_type
            result = self.ApiFace.detect(image, image_type, options=option)
            imgcrop = self.cmbox_face_child_imgcut.currentText()
            changepos = self.lnedit_face_child_changepos.text()
            if imgcrop != 'NONE':
                others.update({'filepath':filepath})
                others.update({'action':imgcrop})
                if changepos: others.update({'changepos':changepos})

        elif current_mode == '活体视频分析': # 测试失败
            video = self.lnedit_face_child_video.text()
            if not os.path.isfile(video):
                QMessageBox.warning(self,'提示','视频不存在',QMessageBox.Cancel)
                return None
            video = base64.b64encode(open(r'{}'.format(video),'rb').read()).decode()
            option = {'video_base64':video} #video_base64
            result = self.ApiFace.verify(option)

        elif current_mode == '在线活体检测':
            filepath = self.lnedit_face_child_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self,'提示','图片不存在',QMessageBox.Cancel)
                return None
            image = base64.b64encode(open(r'{}'.format(filepath),'rb').read()).decode()
            image_type = self.cmbox_face_child_imgtype.currentText()
            face_field = self.lnedit_face_child_facefield.text()
            option = self.cmbox_face_child_optioninfo.currentText()
            images = [{'image':image, 'image_type':image_type, 'face_field':face_field, 'option':option}]
            result = self.ApiFace.faceverify(images)

        elif current_mode == '获取组列表':
            start = str(self.spb_face_child_index_start.value())
            length = str(self.spb_face_child_length.value())
            option = {"start":start, 'length':length}
            result = self.ApiFace.getGroupList(option)

        elif current_mode == '删除用户组':
            group_id = self.lnedit_face_child_groupid.text()

            result = self.ApiFace.groupDelete(group_id)

        elif current_mode == '删除人脸':
            user_id = self.lnedit_face_child_userid.text()
            group_id = self.lnedit_face_child_groupid.text()
            face_token = self.lnedit_face_child_face_token.text()

            result = self.ApiFace.faceDelete(user_id, group_id, face_token)

        elif current_mode == '创建用户组':
            group_id = self.lnedit_face_child_groupid.text()

            result = self.ApiFace.groupAdd(group_id)

        elif current_mode == '组用户列表':
            group_id = self.lnedit_face_child_groupid.text()
            start = str(self.spb_face_child_index_start.value())
            length = str(self.spb_face_child_length.value())
            option = {"start":start, 'length':length}
            result = self.ApiFace.getGroupUsers(group_id, option)

        elif current_mode in ['用户信息查询','用户人脸列表','删除用户']:
            user_id = self.lnedit_face_child_userid.text()
            group_id = self.lnedit_face_child_groupid.text()
            if current_mode == '用户信息查询':
                result = self.ApiFace.getUser(user_id, group_id)
            elif current_mode == '用户人脸列表':
                result = self.ApiFace.faceGetlist(user_id, group_id)
            elif current_mode == '删除用户':
                result = self.ApiFace.deleteUser(group_id, user_id)

        elif current_mode == '复制用户':
            user_id = self.lnedit_face_child_userid.text()
            src_group_id = self.lnedit_face_child_groupid.text()
            dst_group_id = self.lnedit_face_child_groupid2.text()
            option = {'src_group_id':src_group_id,'dst_group_id':dst_group_id}
            result = self.ApiFace.userCopy(user_id, option)

        elif current_mode in ['人脸更新', '人脸注册']:
            filepath = self.lnedit_face_child_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self,'提示','图片不存在',QMessageBox.Cancel)
                return None
            image = base64.b64encode(open(r'{}'.format(filepath),'rb').read()).decode()
            image_type = self.cmbox_face_child_imgtype.currentText()
            group_id = self.lnedit_face_child_groupid.text()
            user_id = self.lnedit_face_child_userid.text()

            quality_control = self.cmbox_face_child_quality.currentText()
            liveness_control = self.cmbox_face_child_liveness_control.currentText()
            userinfo = self.lnedit_face_child_user_info.text()
            action_type = self.cmbox_face_child_actiontype.currentText()
            option = {}

            if userinfo: option['userinfo'] = userinfo
            if liveness_control: option['liveness_control'] = liveness_control
            if quality_control: option['quality_control'] = quality_control
            if action_type: option['action_type'] = action_type

            if current_mode == '人脸注册':
                result = self.ApiFace.addUser(image, image_type, group_id, user_id, option)
            elif current_mode == '人脸更新':
                result = self.ApiFace.updateUser(image, image_type, group_id, user_id, option)

        elif current_mode == '人脸融合':
            filepath = self.lnedit_face_child_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self,'提示','模板图片不存在',QMessageBox.Cancel)
                return None
            image = base64.b64encode(open(r'{}'.format(filepath),'rb').read()).decode()

            filepath2 = self.lnedit_face_child_img2.text()
            if not os.path.isfile(filepath2):
                QMessageBox.warning(self,'提示','目标图片不存在',QMessageBox.Cancel)
                return None
            image2 = base64.b64encode(open(r'{}'.format(filepath2),'rb').read()).decode()
            face_location = self.lnedit_face_child_facelocation.text()
            face_location2 = self.lnedit_face_child_facelocation2.text()

            image_type = self.cmbox_face_child_imgtype.currentText()
            image_type2 = self.cmbox_face_child_imgtype2.currentText()
            quality_control = self.cmbox_face_child_quality.currentText()

            images = {'image_template':{'image':image, 'image_type':image_type,"quality_control":quality_control},
                      "image_target":{'image':image2, 'image_type':image_type2,"quality_control":quality_control}}

            if face_location:images['image_template']['face_location'] = face_location

            if face_location2:images['image_target']['face_location'] = face_location2

            result = self.ApiFace.merge(images)


        elif current_mode == '人脸对比':
            filepath = self.lnedit_face_child_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self,'提示','图片不存在',QMessageBox.Cancel)
                return None
            image = base64.b64encode(open(r'{}'.format(filepath),'rb').read()).decode()

            filepath2 = self.lnedit_face_child_img2.text()
            if not os.path.isfile(filepath2):
                QMessageBox.warning(self,'提示','图片2不存在',QMessageBox.Cancel)
                return None
            image2 = base64.b64encode(open(r'{}'.format(filepath2),'rb').read()).decode()

            image_type = self.cmbox_face_child_imgtype.currentText()
            image_type2 = self.cmbox_face_child_imgtype2.currentText()
            face_type = self.cmbox_face_child_facetype.currentText()
            quality_control = self.cmbox_face_child_quality.currentText()
            liveness_control = self.cmbox_face_child_liveness_control.currentText()


            images = [{'image':image, 'image_type':image_type,'face_type':face_type,"quality_control":quality_control,'liveness_control':liveness_control},
                      {'image':image2, 'image_type':image_type2,'face_type':face_type,"quality_control":quality_control,'liveness_control':liveness_control}]

            result = self.ApiFace.match(images)

        elif current_mode == '人脸搜素':
            filepath = self.lnedit_face_child_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self,'提示','图片不存在',QMessageBox.Cancel)
                return None
            image = base64.b64encode(open(r'{}'.format(filepath),'rb').read()).decode()
            image_type = self.cmbox_face_child_imgtype.currentText()
            group_id = self.lnedit_face_child_groupid.text()

            max_face_num = str(self.spb_face_child_maxface.value())
            quality_control = self.cmbox_face_child_quality.currentText()
            liveness_control = self.cmbox_face_child_liveness_control.currentText()
            user_id = self.lnedit_face_child_userid.text()
            option = {}

            if max_face_num: option['max_face_num'] = max_face_num
            if liveness_control: option['liveness_control'] = liveness_control
            if user_id: option['user_id'] = user_id
            if quality_control: option['quality_control'] = quality_control

            result = self.ApiFace.search(image, image_type, group_id, option)


        elif current_mode == '人脸搜索M:N':
            filepath = self.lnedit_face_child_img.text()
            if not os.path.isfile(filepath):
                QMessageBox.warning(self,'提示','图片不存在',QMessageBox.Cancel)
                return None
            image = base64.b64encode(open(r'{}'.format(filepath), 'rb').read()).decode()
            image_type = self.cmbox_face_child_imgtype.currentText()
            group_id = self.lnedit_face_child_groupid.text()

            max_face_num = str(self.spb_face_child_maxface.value())
            match_threshold = str(self.spb_face_child_threshold.value())
            quality_control = self.cmbox_face_child_quality.currentText()
            max_user_num = str(self.spb_face_child_maxuser.value())
            liveness_control = self.cmbox_face_child_liveness_control.currentText()
            user_id = self.lnedit_face_child_userid.text()
            option = {}

            if max_face_num: option['max_face_num'] = max_face_num
            if liveness_control: option['liveness_control'] = liveness_control
            if user_id: option['user_id'] = user_id
            if match_threshold: option['match_threshold'] = match_threshold
            if quality_control: option['quality_control'] = quality_control
            if max_user_num: option['max_user_num'] = max_user_num

            result = self.ApiFace.multiSearch(image, image_type, group_id, option)

        elif current_mode == '用户人脸列表':
            user_id = self.lnedit_face_child_userid.text()
            group_id = self.lnedit_face_child_groupid.text()

            result = self.ApiFace.faceGetlist(user_id, group_id)

        elif current_mode == '语音验证码':
            user_id = self.lnedit_face_child_userid.text()
            option = {'user_id':user_id}
            result = self.ApiFace.videoSessioncode(option)



        self.label_status_left.setText(current_mode)
        self.pbar_bottom.setValue(60) # 进度条更新
        # 进入数据处理函数
        fina = self.face_child_result_deal(current_mode,result,others)
        if fina:
            self.label_status_left.setText(current_mode)
            self.pbar_bottom.setValue(100)
            self.label_status_right.setText('完成！')
        else:
            self.label_status_left.setText(current_mode)
            self.pbar_bottom.reset()
            self.label_status_right.setText('失败！')


    @catch_except
    def face_child_result_deal(self, mode, result,options=None):
        if not result:
            print(str(result))
            content = '{} --> 失败'.format(mode)
            self.txedit_face_child_content.setText(content)
            return False
        elif mode == '人脸检测':
            content = '人脸检测完成\n'
            content = self.dict_get_value(result,content)
            self.txedit_face_child_content.setText(content)
            datas = result.get('result')
            multi_pos = []
            if datas:
                faces = datas.get('face_list')
                for index,face in enumerate(faces):
                    index += 1
                    face_token = face.get('face_token')
                    left = face.get('location')['left']
                    top = face.get('location')['top']
                    width = face.get('location')['width']
                    height = face.get('location')['height']
                    angle = face.get('angle')

                    if options:
                        # 人脸位置
                        x, y, x2, y2 = left, top, left + width, top + height

                        changepos = options.get('changepos')
                        if changepos:  # 人脸位置调整
                            if not changepos.endswith(','): changepos += ','
                            changes = re.findall('(.*?),',changepos)

                            for i, change in enumerate(changes):
                                if change:
                                    if i == 0:x += float(change)
                                    elif i == 1:y += float(change)
                                    elif i == 2:x2 += float(change)
                                    elif i == 3:y2 += float(change)

                        face_pos = (x,y,x2,y2)
                        multi_pos.append(face_pos)

                if options:
                    img = options.get('filepath')
                    action = options.get('action')
                    if action in ['CROP', 'ALL']:  # 裁切
                        for i,pos in enumerate(multi_pos):
                            i += 1
                            img2 = img.replace('\\', '/')
                            newname = re.findall('(.*)/(.*)\.(.*?)$', img2)[0][1] + str(i)
                            self.face_crop(img, pos, newname)

                    if action in ['DRAW', 'ALL']:  # 绘制
                        img2 = img.replace('\\', '/')
                        newname = re.findall('(.*)/(.*)\.(.*?)$', img2)[0][1]
                        self.face_draw(img, multi_pos,newname)
            else:
                content = '{} --> 失败'.format(mode)
                content = self.dict_get_value(result,content)

        elif mode == '人脸融合':
            datas = result.get('result')
            if datas:
                _session_id = time.strftime('%Y%m%d-%H%M%S', time.localtime()) + str(random.randint(0, 9))
                _path = r'./Record/Img/Merge/{}.png'.format(_session_id)
                with open(_path, 'wb') as f:
                    f.write(base64.b64decode(datas['merge_image']))

                _path_face = os.path.abspath(_path)
                content = '\n人脸融合完成，保存在 -> {}'.format(_path_face)
                self.txedit_face_child_content.setText(content)
            else:
                content = '{} --> 失败\n'.format(mode)
                content = self.dict_get_value(result,content)
                self.txedit_face_child_content.setText(content)


        else:
            content = '{}-->完成\n'.format(mode)
            content = self.dict_get_value(result,content)
            self.txedit_face_child_content.setText(content)
        return True


    @catch_except
    def face_draw(self,img:str,multi_pos:list,newname=None):
        """人脸位置绘制"""

        _session_id = time.strftime('%Y%m%d-%H%M%S', time.localtime()) + str(random.randint(0, 9))
        if newname: _session_id = newname
        _path_face = './Record/Img/Draw/{}.png'.format(_session_id)
        image = Image.open(img)
        draw = ImageDraw.Draw(image)
        for pos in multi_pos:
            draw.rectangle(pos,width=3)
        image.save(_path_face)
        content = self.txedit_face_child_content.toPlainText()
        _path_face = os.path.abspath(_path_face)
        content += '\n人脸绘制完成，保存在 -> {}'.format(_path_face)
        self.txedit_face_child_content.setText(content)


    @catch_except
    def face_crop(self,img,face_pos,newname=None):
        """
        传入原图像和人脸位置数据，切割人脸图像并保存

        """

        _session_id = time.strftime('%Y%m%d-%H%M%S', time.localtime()) + str(random.randint(0, 9))
        if newname: _session_id = newname
        _path_face = './Record/Img/Crop/{}.png'.format(_session_id)
        _img = Image.open(img)
        _face = _img.crop(face_pos)
        _face.save(_path_face)

        content = self.txedit_face_child_content.toPlainText()
        _path_face = os.path.abspath(_path_face)
        content += '\n人脸裁切完成，保存在 -> {}'.format(_path_face)
        self.txedit_face_child_content.setText(content)



    def btn_face_child_folder3_clicked(self, *args):
        file = QFileDialog.getOpenFileName(self,'选择视频',"./","All File(*)")
        if file[0]:
            self.lnedit_face_child_video.setText(file[0])


    @catch_except
    def btn_face_child_folder_clicked(self,*args):
        file = QFileDialog.getOpenFileName(self,'选择图片',"./","All File(*);;png(*.png);;jpeg(*.jpeg);;jpg(*.jpg);;bmp(*.bmp)")
        if file[0]:
            self.lnedit_face_child_img.setText(file[0])
        pass
    def btn_face_child_folder2_clicked(self,*args):
        file = QFileDialog.getOpenFileName(self,'选择图片',"./","All File(*);;png(*.png);;jpeg(*.jpeg);;jpg(*.jpg);;bmp(*.bmp)")

        if file[0]:
            self.lnedit_face_child_img2.setText(file[0])



    def resizeEvent_face(self, a0: QtGui.QResizeEvent) -> None:
        value = int(self.width()*0.2 /6)
        self.glayout_face_home.setSpacing(value)
        pass

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     UI = Face()
#     UI.show()
#     sys.exit(app.exec_())