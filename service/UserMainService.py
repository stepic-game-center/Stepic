import sys
import requests
import json
import os
import configparser
import datetime
from threading import Thread
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath + '\windows')

from UserLogin import Ui_UserLoginWindow
from UserRegist import Ui_UserRegistWindow
from UserMain1 import Ui_UserMainWindow
from UserInformation1 import Ui_UserInformationWindow

config = configparser.RawConfigParser()


def async_call(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()

    return wrapper


class UserLoginForm(QtWidgets.QMainWindow, Ui_UserLoginWindow):
    sign_1 = pyqtSignal(str)

    def __init__(self, parent=None):
        super(UserLoginForm, self).__init__(parent)
        self.setupUi(self)
        self.read_config()
        self.btn_login.clicked.connect(self.login)
        self.btn_close.clicked.connect(self.close)
        self.btn_regit.clicked.connect(self.regist)

    def send_name(self, name):
        self.sign_1.emit(name)

    def login(self):
        username = self.lineEdit_name.text()
        password = self.lineEdit_pwd.text()
        if len(username) == 0 or len(password) == 0:
            QMessageBox.warning(self, "错误", "用户名和密码不得为空！", QMessageBox.Yes)
            return
        url = "https://stepic-api.redcountry.top/api/login_user"
        data = {"username": username, "password": password}
        res = requests.post(url=url, data=data)
        if res.text == "success":
            self.write_config()
            self.Win_main_1 = UserMainForm()
            self.sign_1.connect(self.Win_main_1.receive_name)
            self.send_name(username)
            self.close()
            self.Win_main_1.show()
        else:
            QMessageBox.warning(self, "错误", "您的用户名或密码输入有误，请重新输入！", QMessageBox.Yes)
            self.lineEdit_pwd.clear()
            self.lineEdit_pwd.setFocus()

    def regist(self):
        self.hide()
        self.Win_regist = UserRegistForm()
        self.Win_regist.show()

    def write_config(self):
        username = self.lineEdit_name.text()
        list1 = list(map(ord, self.lineEdit_pwd.text()))
        password = '|'.join('%s' %id for id in list1)
        config.read('../config/user.ini', encoding='utf-8')
        if config.has_section('User') == False:
            config.add_section('User')
        if self.checkBox.isChecked():
            config.set('User', 'remember', 'true')
            config.set('User', 'username', username)
            config.set('User', 'password', password)
        else:
            config.set('User', 'remember', 'false')
            config.set('User', 'username', username)
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
            else:
                self.checkBox.setChecked(False)
                username = config.get('User', 'username')
                self.lineEdit_name.setText(username)
                self.lineEdit_pwd.setFocus()


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
        url = "https://stepic-api.redcountry.top/api/regit_user"
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
    sign_2 = pyqtSignal(str)

    def __init__(self, parent=None):
        super(UserMainForm, self).__init__(parent)
        self.setupUi(self)
        url = "https://stepic-api.redcountry.top/api/game/query_all_pub"
        r = requests.post(url=url, data="")
        self.games = json.loads(r.text)
        index = 0
        for button in self.game_Button:
            button.game = self.games[index]
            index += 1
            button.clicked.connect(self.download_game)
        self.download_image()
        self.exit.triggered.connect(self.close)
        self.logout.triggered.connect(self.logout_user)
        self.information.triggered.connect(self.user_information)

    def receive_name(self, name):
        self.username = name
        url = 'https://stepic-api.redcountry.top/api/user/query_userinfo'
        data = {'username': name}
        res = requests.post(url=url, data=data)
        user = json.loads(res.text)
        self.exper = user['exper']
        if user['unick'] != None and user['unick'] != '':
            self.menu_Button.setText('欢迎您，' + user['unick'])
            self.logout.setText('注销账户：' + user['unick'])
            QtWidgets.QApplication.processEvents()
        else:
            self.menu_Button.setText('欢迎您，' + user['uname'])
            self.logout.setText('注销账户：' + user['uname'])
            QtWidgets.QApplication.processEvents()
        url_1 = 'https://stepic-api.redcountry.top/api/score/query_max_all'
        res_1 = requests.post(url=url_1, data='')
        if res_1.text == 'empty':
            self.score_table.setColumnCount(1)
            self.score_table.setRowCount(1)
            self.score_table.verticalHeader().setVisible(False)
            self.score_table.horizontalHeader().setVisible(False)
            newItem = QtWidgets.QTableWidgetItem('没有游玩记录...')
            self.score_table.setItem(0, 0, newItem)
            QtWidgets.QTableWidget.resizeRowsToContents(self.score_table)
        else:
            scores = json.loads(res_1.text)
            self.score_table.verticalHeader().setVisible(False)
            index = 0
            for score in scores:
                self.score_table.setRowCount(index + 1)
                item1 = QtWidgets.QTableWidgetItem(score['gname'])
                item1.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.score_table.setItem(index, 0, item1)
                if score['unick'] == None:
                    username = score['uname']
                else:
                    username = score['unick']
                item2 = QtWidgets.QTableWidgetItem(username)
                item2.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.score_table.setItem(index, 1, item2)
                item3 = QtWidgets.QTableWidgetItem(str(score['score']))
                item3.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.score_table.setItem(index, 2, item3)
                item4 = QtWidgets.QTableWidgetItem(score['date'])
                item4.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.score_table.setItem(index, 3, item4)
                index += 1

    def send_name(self, name):
        self.sign_2.emit(name)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "退出", "您是否确定退出本平台？", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def close(self):
        self.hide()
        app.quit()

    def logout_user(self):
        config.remove_section('User')
        config.write(open('../config/user.ini', 'w', encoding='utf-8'))
        self.hide()
        self.Win_login_1 = UserLoginForm()
        self.Win_login_1.show()

    @async_call
    def download_image(self):
        if config.has_section('Image'):
            for game in self.games:
                if config.has_option('Image', game['gname']):
                    if config.get('Image', game['gname']) == game['version']:
                        continue
                    else:
                        u = game["image"]
                        image = requests.get(u)
                        open("../image/game/" + game['image'].split('/')[-1], 'wb').write(image.content)
                        config.set('Image', game['gname'], game['version'])
                        config.write(open('../config/user.ini', 'w', encoding='utf-8'))
                else:
                    u = game["image"]
                    image = requests.get(u)
                    open("../image/game/" + game['image'].split('/')[-1], 'wb').write(image.content)
                    config.set('Image', game['gname'], game['version'])
                    config.write(open('../config/user.ini', 'w', encoding='utf-8'))
        else:
            config.add_section('Image')
            for game in self.games:
                u = game["image"]
                image = requests.get(u)
                open("../image/game/" + game['image'].split('/')[-1], 'wb').write(image.content)
                config.set('Image', game['gname'], game['version'])
                config.write(open('../config/user.ini', 'w', encoding='utf-8'))

    def download_game(self):
        index = 0
        if config.has_section('Game'):  # 配置文件中已有Game
            if config.has_option('Game', self.sender().game['gname']):  # 判断是否已有该游戏
                if config.get('Game', self.sender().game['gname']) == self.sender().game['version']:  # 有该游戏判断版本是否最新
                    self.hide()
                    os.system('python ../game/' + self.sender().game['filename'])
                    index += 5
                    self.show()
                else:  # 不是最新更新版本
                    reply = QMessageBox.question(self, '更新', '游戏版本可以更新，是否更新？', QMessageBox.Yes | QMessageBox.No)
                    if reply == QMessageBox.Yes:  # 更新游戏
                        url = self.sender().game['fileurl']
                        g = requests.get(url)
                        open('../game/' + self.sender().game['filename'], 'wb').write(g.content)
                        config.set('Game', self.sender().game['gname'], self.sender().game['version'])
                        massage = QMessageBox.information(self, '成功', '下载完成，是否打开游戏？', QMessageBox.Yes | QMessageBox.No)
                        if massage == QMessageBox.Yes:  # 打开游戏
                            self.hide()
                            os.system('python ../game/' + self.sender().game['filename'])
                            index += 5
                            self.show()
                    else:  # 不更新打开游戏
                        self.hide()
                        os.system('python ../game/' + self.sender().game['filename'])
                        index += 5
                        self.show()
            else:  # 下载游戏并在配置文件中记录
                reply = QMessageBox.question(self, '下载', '您还未下载该游戏，是否下载？', QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:  # 下载游戏
                    url = self.sender().game['fileurl']
                    g = requests.get(url)
                    open('../game/' + self.sender().game['filename'], 'wb').write(g.content)
                    config.set('Game', self.sender().game['gname'], self.sender().game['version'])
                    massage = QMessageBox.information(self, '成功', '下载完成，是否打开游戏？', QMessageBox.Yes | QMessageBox.No)
                    if massage == QMessageBox.Yes:  # 打开游戏
                        self.hide()
                        os.system('python ../game/' + self.sender().game['filename'])
                        index += 5
                        self.show()
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
                    self.hide()
                    os.system('python ../game/' + self.sender().game['filename'])
                    config.read('../config/user.ini', encoding='utf-8')
                    if config.has_option('Game', self.sender().game['name'] + '_score'):
                        score = config.get('Game', self.sender().game['name'] + '_score')
                        url_1 = 'https://stepic-api.redcountry.top/api/score/add'
                        data_1 = {'uname': self.username, 'gid': self.sender().game['gid'], 'score': score}
                        res_1 = requests.post(url=url_1, data=data_1)
                        if res_1.text == 'success' and int(score) > 0:
                            index += 5
                    self.receive_name(self.username)
                    self.show()
        config.write(open('../config/user.ini', 'w', encoding='utf-8'))
        url_2 = 'https://stepic-api.redcountry.top/api/user/update_exper'
        data_2 = {'username': self.username, 'exper': index}
        res_2 = requests.post(url=url_2, data=data_2)

    def user_information(self):
        self.Win_information = UserInformationForm()
        self.sign_2.connect(self.Win_information.receive_name)
        self.send_name(self.username)
        self.hide()
        self.Win_information.show()


class UserInformationForm(QtWidgets.QMainWindow, Ui_UserInformationWindow):
    sign_3 = pyqtSignal(str)

    def __init__(self, parent=None):
        super(UserInformationForm, self).__init__(parent)
        self.setupUi(self)
        self.change_Button.clicked.connect(self.change_information)

    def closeEvent(self, event):
        self.hide()
        self.Win_main = UserMainForm()
        self.sign_3.connect(self.Win_main.receive_name)
        self.send_name(self.username)
        self.Win_main.show()

    def send_name(self, name):
        self.sign_3.emit(name)

    def receive_name(self, name):
        self.username = name
        url = 'https://stepic-api.redcountry.top/api/user/query_userinfo'
        data = {'username': name}
        res = requests.post(url=url, data=data)
        user = json.loads(res.text)
        self.name_Edit.setText(user['uname'])
        if user['unick'] != None and user['unick'] != '':
            self.setWindowTitle(user['unick'] + '的个人主页')
            self.nick_Edit.setText(user['unick'])
        else:
            self.setWindowTitle(user['uname'] + '的个人主页')
        if user['sex'] == '男':
            self.man_radio.setChecked(True)
        elif user['sex'] == '女':
            self.woman_radio.setChecked(True)
        if user['birthday'] != None:
            date = datetime.datetime.strptime(user['birthday'], '%Y-%m-%d').date()
            self.birthday_Edit.setDate(date)
        else:
            date = datetime.datetime.strptime('2000-01-01', '%Y-%m-%d').date()
            self.birthday_Edit.setDate(date)
        self.phone_Edit.setText(user['phone'])
        self.intro_Edit.setText(user['intro'])
        level = int(user['exper'] / 100)
        self.level.setText(str(level) + '  级')
        self.exper.setText('经验值：' + str(user['exper'] % 100) + '/100')
        uid = user['uid']
        url_1 = 'https://stepic-api.redcountry.top/api/score/query_event'
        data_1 = {'uid': uid}
        res_1 = requests.post(url=url_1, data=data_1)
        if res_1.text == 'empty':
            self.score_table.setColumnCount(1)
            self.score_table.setRowCount(1)
            self.score_table.verticalHeader().setVisible(False)
            self.score_table.horizontalHeader().setVisible(False)
            newItem = QtWidgets.QTableWidgetItem('您最近没有游玩记录，游玩游戏获得得分即体现在最近动态中')
            self.score_table.setItem(0, 0, newItem)
            QtWidgets.QTableWidget.resizeRowsToContents(self.score_table)
        else:
            scores = json.loads(res_1.text)
            self.score_table.verticalHeader().setVisible(False)
            index = 0
            for score in scores:
                self.score_table.setRowCount(index + 1)
                item1 = QtWidgets.QTableWidgetItem(str(score['gname']))
                item1.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.score_table.setItem(index, 0, item1)
                item2 = QtWidgets.QTableWidgetItem(str(score['score']))
                item2.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.score_table.setItem(index, 1, item2)
                item3 = QtWidgets.QTableWidgetItem(str(score['date']))
                item3.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.score_table.setItem(index, 2, item3)
                index += 1

    def change_information(self):
        name = self.name_Edit.text()
        nick = self.nick_Edit.text()
        sex = '未知'
        if self.man_radio.isChecked():
            sex = '男'
        elif self.woman_radio.isChecked():
            sex = '女'
        phone = self.phone_Edit.text()
        b = self.birthday_Edit.date().toPyDate()
        birthday = str(b)
        intro = self.intro_Edit.toPlainText()
        if phone == '':
            QMessageBox.warning(self, '错误', '电话号码不得为空！', QMessageBox.Yes)
            self.phone_Edit.setFocus()
            return
        if len(phone) != 11 or phone.isdigit() == False:
            QMessageBox.warning(self, '错误', '请输入正确的电话号码！', QMessageBox.Yes)
            self.phone_Edit.setFocus()
            return
        url = 'https://stepic-api.redcountry.top/api/user/update_userinfo'
        data = {'uname': name, 'unick': nick, 'sex': sex, 'phone': phone, 'birthday': birthday, 'intro': intro}
        res = requests.post(url=url, data=data)
        if res.text == 'success':
            self.hide()
            QMessageBox.information(self, '成功', '修改用户成功！', QMessageBox.Yes)
            self.receive_name(name)
            self.show()
        else:
            QMessageBox.warning(self, '错误', '修改用户失败！', QMessageBox.Yes)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Win_login = UserLoginForm()
    Win_login.show()
    sys.exit(app.exec_())
