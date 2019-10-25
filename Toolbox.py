"""
@author 微&风
@data   2019.10.20

实现：
    调用百度API，实现所有功能，并且可以通过微信进行调用

思路：
    窗体使用PYQT5进行设计，
    1、暂不考虑无边框
    2、功能分类，多TAB还是单TAB?
    3、先实现窗体调用，再考虑微信调用
    4、使用百度API提供的包
    5、考虑设计用户登录？密码保护？数据加密？


"""

from ToolBox.voice import *
from ToolBox.face_ import *
from ToolBox.bodyays import *

class Main(Voice,Face,Body):
    def __init__(self):
        super(Main, self).__init__()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.resizeEvent_ui(a0)
        self.resizeEvent_face(a0)
        self.resizeEvent_body(a0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    UI = Main()
    UI.show()
    sys.exit(app.exec_())