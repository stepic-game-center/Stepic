import sys
import requests
import json
import os
import configparser
from threading import Thread
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QToolButton
sys.path.append(r'D:\workspace\python\stepic\service')

from UserLogin import Ui_UserLoginWindow
from UserRegist import Ui_UserRegistWindow
from UserMain1 import Ui_UserMainWindow

config = configparser.RawConfigParser()

def async_call(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()

    return wrapper


class UserLoginForm(QtWidgets.QMainWindow, Ui_UserLoginWindow):
    def __init__(self, parent=None):
        super(UserLoginForm, self).__init__(parent)
        self.setupUi(self)
        self.read_config()
        self.btn_login.clicked.connect(self.login)
        self.btn_close.clicked.connect(self.close)
        self.btn_regit.clicked.connect(self.regist)

    def login(self):
        username = self.lineEdit_name.text()
        password = self.lineEdit_pwd.text()

        if len(username) == 0 or len(password) == 0:
            QMessageBox.warning(self, "错误", "用户名和密码不得为空！", QMessageBox.Yes)
            return
        url = "http://106.13.236.185:5000/api/login_user"
        data = {"username": username, "password": password}
        res = requests.post(url=url, data=data)
        if res.text == "success":
            if self.checkBox.isChecked():
                self.write_config()
            self.hide()
            Win_main.show()
        else:
            QMessageBox.warning(self, "错误", "您的用户名或密码输入有误，请重新输入！", QMessageBox.Yes)
            self.lineEdit_pwd.clear()
            self.lineEdit_pwd.setFocus()

    def regist(self):
        self.hide()
        Win_regist.show()

    def write_config(self):
        username = self.lineEdit_name.text()
        list1 = list(map(ord, self.lineEdit_pwd.text()))
        password = '|'.join('%s' %id for id in list1)
        config.read('../config/user.ini', encoding='utf-8')
        if config.has_section('User') == False:
            config.add_section('User')
        config.set('User', 'remember', 'true')
        config.set('User', 'username', username)
        config.set('User', 'password', password)
        config.write(open('../config/user.ini', 'w', encoding='utf-8'))

    def read_config(self):
        config.read('../config/user.ini', encoding='utf-8')
        if config.has_section('User'):
            remember = config.get('User', 'remember')
            if remember == 'true':
                self.checkBox.setChecked(True)
                username = config.get('User', 'username')
                list1 = list(map(int, config.get('User', 'password').split('|')))
                password = ''.join(map(chr, list1))
                self.lineEdit_name.setText(username)
                self.lineEdit_pwd.setText(password)


class UserRegistForm(QtWidgets.QMainWindow, Ui_UserRegistWindow):
    def __init__(self, parent=None):
        super(UserRegistForm, self).__init__(parent)
        self.setupUi(self)
        self.btn_regist.clicked.connect(self.regist)
        self.btn_close.clicked.connect(self.closeEvent)

    def closeEvent(self, event):
        self.lineEdit_name.clear()
        self.lineEdit_pwd.clear()
        self.lineEdit_repwd.clear()
        self.lineEdit_name.setFocus()
        Win_login.show()
        self.close()

    def regist(self):
        username = self.lineEdit_name.text()
        password = self.lineEdit_pwd.text()
        repassword = self.lineEdit_repwd.text()
        if len(username) == 0 or len(password) == 0 or len(repassword) == 0:
            QMessageBox.warning(self, "错误", "用户名和密码不得为空！", QMessageBox.Yes)
            return
        if password != repassword:
            QMessageBox.warning(self, "错误", "两次输入密码不相同！", QMessageBox.Yes)
            self.lineEdit_repwd.clear()
            self.lineEdit_repwd.setFocus()
            return
        url = "http://106.13.236.185:5000/api/regit_user"
        data = {"username": username, "password": password}
        res = requests.post(url=url, data=data)
        if res.text == "success":
            QMessageBox.information(self, "成功", "恭喜您，注册用户成功！", QMessageBox.Yes)
            self.lineEdit_name.clear()
            self.lineEdit_pwd.clear()
            self.lineEdit_repwd.clear()
            self.lineEdit_name.setFocus()
            Win_login.show()
            self.close()
        elif res.text == "repeat":
            QMessageBox.warning(self, "错误", "用户名已被注册！", QMessageBox.Yes)
        else:
            QMessageBox.warning(self, "错误", "注册失败！", QMessageBox.Yes)


class UserMainForm(QtWidgets.QMainWindow, Ui_UserMainWindow):
    def __init__(self, parent=None):
        super(UserMainForm, self).__init__(parent)
        self.setupUi(self)
        url = "http://106.13.236.185:5000/api/game/query_all_pub"
        r = requests.post(url=url, data="")
        self.games = json.loads(r.text)
        self.download_image()
        index = 0
        for button in self.game_Button:
            button.game = self.games[index]
            index += 1
            button.clicked.connect(self.download_game)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "退出", "您是否确定退出本平台？", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    @async_call
    def download_image(self):
        config.read('../config/user.ini', encoding='utf-8')
        if config.has_section('Image'):
            for game in self.games:
                if config.has_option('Image', game['gname']):
                    if config.get('Image', game['gname']) == game['version']:
                        continue
                    else:
                        os.remove('../image/game/' + game['image'].split('/')[-1])
                        u = game["image"]
                        image = requests.get(u)
                        open("../image/game/" + game['image'].split('/')[-1], 'wb').write(image.content)
                        config.set('Image', game['gname'], game['version'])
                else:
                    u = game["image"]
                    image = requests.get(u)
                    open("../image/game/" + game['image'].split('/')[-1], 'wb').write(image.content)
                    config.set('Image', game['gname'], game['version'])
        else:
            config.add_section('Image')
            for game in self.games:
                u = game["image"]
                image = requests.get(u)
                open("../image/game/" + game['image'].split('/')[-1], 'wb').write(image.content)
                config.set('Image', game['gname'], game['version'])
        config.write(open('../config/user.ini', 'w', encoding='utf-8'))

    def download_game(self):
        config.read('../config/user.ini', encoding='utf-8')
        if config.has_section('Game'):  # 配置文件中已有Game
            if config.has_option('Game', self.sender().game['gname']):  # 判断是否已有该游戏
                if config.get('Game', self.sender().game['gname']) == self.sender().game['version']:  # 有该游戏判断版本是否最新
                    Win_main.hide()
                    os.system('python ../game/' + self.sender().game['filename'])
                    Win_main.show()
                else:  # 不是最新更新版本
                    reply = QMessageBox.question(self, '更新', '游戏版本可以更新，是否更新？', QMessageBox.Yes | QMessageBox.No)
                    if reply == QMessageBox.Yes:  # 更新游戏
                        os.remove('../game/' + self.sender().game['filename'])
                        url = self.sender().game['fileurl']
                        g = requests.get(url)
                        open('../game/' + self.sender().game['filename'], 'wb').write(g.content)
                        config.set('Game', self.sender().game['gname'], self.sender().game['version'])
                        massage = QMessageBox.information(self, '成功', '下载完成，是否打开游戏？', QMessageBox.Yes | QMessageBox.No)
                        if massage == QMessageBox.Yes:  # 打开游戏
                            Win_main.hide()
                            os.system('python ../game/' + self.sender().game['filename'])
                            Win_main.show()
                    else:  # 不更新打开游戏
                        Win_main.hide()
                        os.system('python ../game/' + self.sender().game['filename'])
                        Win_main.show()
            else:  # 下载游戏并在配置文件中记录
                reply = QMessageBox.question(self, '下载', '您还未下载该游戏，是否下载？', QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:  # 下载游戏
                    url = self.sender().game['fileurl']
                    g = requests.get(url)
                    open('../game/' + self.sender().game['filename'], 'wb').write(g.content)
                    config.set('Game', self.sender().game['gname'], self.sender().game['version'])
                    massage = QMessageBox.information(self, '成功', '下载完成，是否打开游戏？', QMessageBox.Yes | QMessageBox.No)
                    if massage == QMessageBox.Yes:  # 打开游戏
                        Win_main.hide()
                        os.system('python ../game/' + self.sender().game['filename'])
                        Win_main.show()
        else:  # 新增Game配置文件并询问是否下载
            config.add_section('Game')
            reply = QMessageBox.question(self, '下载', '您还未下载该游戏，是否下载？', QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:  # 下载游戏
                url = self.sender().game['fileurl']
                g = requests.get(url)
                open('../game/' + self.sender().game['filename'], 'wb').write(g.content)
                config.set('Game', self.sender().game['gname'], self.sender().game['version'])
                massage = QMessageBox.information(self, '成功', '下载完成，是否打开游戏？', QMessageBox.Yes | QMessageBox.No)
                if massage == QMessageBox.Yes:  # 打开游戏
                    Win_main.hide()
                    os.system('python ../game/' + self.sender().game['filename'])
                    Win_main.show()
        config.write(open('../config/user.ini', 'w', encoding='utf-8'))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Win_login = UserLoginForm()
    Win_login.show()
    Win_regist = UserRegistForm()
    Win_main = UserMainForm()
    sys.exit(app.exec_())