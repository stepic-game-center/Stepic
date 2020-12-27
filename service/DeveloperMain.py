import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

import configparser

config = configparser.RawConfigParser()


class DeveloperMainWindow(QMainWindow):

    def __init__(self):
        super(DeveloperMainWindow, self).__init__()
        self.setWindowTitle('STEPIC 开发者平台')  #窗口标题
        self.setWindowIcon(QIcon('../image/游戏.png'))
        self.setGeometry(300, 150, 1355, 730)  #窗口的大小和位置设置
        self.browser=QWebEngineView()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "退出", "您是否确定退出本平台？", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def receive_name(self, name):
        # 加载外部的web界面
        self.browser.load(QUrl('https://stepic.redcountry.top/devMain.html?username=' + name))
        self.setCentralWidget(self.browser)
        ###使用QToolBar创建导航栏，并使用QAction创建按钮
        # 添加导航栏
        navigation_bar = QToolBar('Navigation')
        # 设定图标的大小
        navigation_bar.setIconSize(QSize(16, 16))
        # 添加导航栏到窗口中
        self.addToolBar(navigation_bar)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = DeveloperMainWindow()
    win.show()
    sys.exit(app.exec_())