import sys
import os
import requests
import configparser
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath + '/windows')
sys.path.append(rootPath + '/service')

from AdminLogin import Ui_AdminLoginWindow
from DeveloperRegist import Ui_DeveloperRegistWindow
from AdminMain1 import Ui_AdminMainWindow
from AdminUser1 import  Ui_AdminUserWindow
from AdminDeveloper1 import Ui_AdminDeveloperWindow
from AdminGame1 import Ui_AdminGameWindow
from DeveloperMain import DeveloperMainWindow

config = configparser.RawConfigParser()


class AdminLoginForm(QtWidgets.QMainWindow, Ui_AdminLoginWindow):
    sign_1 = pyqtSignal(str)

    def __init__(self, parent=None):
        super(AdminLoginForm, self).__init__(parent)
        self.setupUi(self)
        self.read_config()
        self.loginButton.clicked.connect(self.login)
        self.exitBottun.clicked.connect(self.close)
        self.developer_regist_button.clicked.connect(self.developer_regist)

    def send_name(self, name):
        self.sign_1.emit(name)

    def login(self):
        if self.admin_radio.isChecked():
            username = self.nametext.text()
            password = self.passwordtext.text()
            if len(username) == 0 or len(password) == 0:
                QMessageBox.warning(self, "错误", "用户名和密码不得为空！", QMessageBox.Yes)
                return
            url = "https://stepic-api.redcountry.top/api/login_admin"
            data = {"username": username, "password": password}
            res = requests.post(url=url, data=data)
            if res.text == "success":
                if self.checkBox.isChecked():
                    self.write_config()
                self.hide()
                self.Win_admin_main = AdminMainForm()
                self.sign_1.connect(self.Win_admin_main.receive_name)
                self.send_name(username)
                self.Win_admin_main.show()
            else:
                QMessageBox.warning(self, "错误", "您的用户名或密码输入有误，请重新输入！", QMessageBox.Yes)
                self.passwordtext.clear()
                self.passwordtext.setFocus()
        else:
            username = self.nametext.text()
            password = self.passwordtext.text()
            if len(username) == 0 or len(password) == 0:
                QMessageBox.warning(self, "错误", "用户名和密码不得为空！", QMessageBox.Yes)
                return
            url = 'https://stepic-api.redcountry.top/api/login_developer'
            data = {'username': username, 'password': password}
            res = requests.post(url=url, data=data)
            if res.text == "success":
                if self.checkBox.isChecked():
                    self.write_config()
                self.Win_developer_main = DeveloperMainWindow()
                self.sign_1.connect(self.Win_developer_main.receive_name)
                self.send_name(username)
                self.hide()
                self.Win_developer_main.show()
            else:
                QMessageBox.warning(self, "错误", "您的用户名或密码输入有误，请重新输入！", QMessageBox.Yes)
                self.passwordtext.clear()
                self.passwordtext.setFocus()

    def developer_regist(self):
        self.Win_developer_regist = DeveloperRegistForm()
        self.hide()
        self.Win_developer_regist.show()

    def write_config(self):
        config.read('../config/admin.ini', encoding='utf-8')
        if self.admin_radio.isChecked():
            username = self.nametext.text()
            list1 = list(map(ord, self.passwordtext.text()))
            password = '|'.join('%s' % id for id in list1)
            if config.has_section('Admin') == False:
                config.add_section('Admin')
            config.set('Admin', 'remember', 'true')
            config.set('Admin', 'username', username)
            config.set('Admin', 'password', password)
        else:
            username = self.nametext.text()
            list1 = list(map(ord, self.passwordtext.text()))
            password = '|'.join('%s' % id for id in list1)
            if config.has_section('Developer') == False:
                config.add_section('Developer')
            config.set('Developer', 'remember', 'true')
            config.set('Developer', 'username', username)
            config.set('Developer', 'password', password)
        config.write(open('../config/admin.ini', 'w', encoding='utf-8'))

    def read_config(self):
        config.read('../config/admin.ini', encoding='utf-8')
        if config.has_section('Admin'):
            remember = config.get('Admin', 'remember')
            if remember == 'true':
                self.checkBox.setChecked(True)
                self.admin_radio.setChecked(True)
                username = config.get('Admin', 'username')
                list1 = list(map(int, config.get('Admin', 'password').split('|')))
                password = ''.join(map(chr, list1))
                self.nametext.setText(username)
                self.passwordtext.setText(password)
        else:
            if config.has_section('Developer'):
                remember = config.get('Developer', 'remember')
                if remember == 'true':
                    self.checkBox.setChecked(True)
                    self.developer_radio.setChecked(True)
                    username = config.get('Developer', 'username')
                    list1 = list(map(int, config.get('Developer', 'password').split('|')))
                    password = ''.join(map(chr, list1))
                    self.nametext.setText(username)
                    self.passwordtext.setText(password)


class DeveloperRegistForm(QtWidgets.QMainWindow, Ui_DeveloperRegistWindow):
    def __init__(self, parent=None):
        super(DeveloperRegistForm, self).__init__(parent)
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
        url = "https://stepic-api.redcountry.top/api/regit_developer"
        data = {"username": username, "password": password}
        res = requests.post(url=url, data=data)
        if res.text == "success":
            QMessageBox.information(self, "成功", "恭喜您，注册开发者账号成功！", QMessageBox.Yes)
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


class AdminMainForm(QtWidgets.QMainWindow, Ui_AdminMainWindow):
    sign_2 = pyqtSignal(str)

    def __init__(self, parent=None):
        super(AdminMainForm, self).__init__(parent)
        self.setupUi(self)
        self.exit_button.triggered.connect(self.close)
        self.logout.triggered.connect(self.logout_admin)
        self.user_Button.clicked.connect(self.admin_user)
        self.developer_Button.clicked.connect(self.admin_developer)
        self.game_Button.clicked.connect(self.admin_game)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "退出", "您是否确定退出本平台？", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def close(self):
        app.quit()

    def send_name(self, name):
        self.sign_2.emit(name)

    def receive_name(self, name):
        self.admin_name = name
        self.menu_Button.setText('欢迎您，管理员' + self.admin_name)
        self.logout.setText('注销账户：' + self.admin_name)

    def logout_admin(self):
        config.read('../config/admin.ini', encoding='utf-8')
        if config.has_section('Admin'):
            config.remove_section('Admin')
        config.write(open('../config/admin.ini', 'w', encoding='utf-8'))
        self.Win_login_1 = AdminLoginForm()
        self.hide()
        self.Win_login_1.show()

    def admin_user(self):
        self.Win_admin_user = AdminUserForm()
        self.sign_2.connect(self.Win_admin_user.receive_name)
        self.send_name(self.admin_name)
        self.hide()
        self.Win_admin_user.show()

    def admin_developer(self):
        self.Win_admin_developer = AdminDeveloperForm()
        self.sign_2.connect(self.Win_admin_developer.receive_name)
        self.send_name(self.admin_name)
        self.hide()
        self.Win_admin_developer.show()

    def admin_game(self):
        self.Win_admin_game = AdminGameForm()
        self.sign_2.connect(self.Win_admin_game.receive_name)
        self.send_name(self.admin_name)
        self.hide()
        self.Win_admin_game.show()


class AdminUserForm(QtWidgets.QMainWindow, Ui_AdminUserWindow):
    sign_3 = pyqtSignal(str)

    def __init__(self, parent=None):
        super(AdminUserForm, self).__init__(parent)
        self.setupUi(self)
        self.exit_button.triggered.connect(self.close)
        self.logout.triggered.connect(self.logout_admin)
        url = 'https://stepic-api.redcountry.top/api/user/query_all'
        res = requests.post(url=url, data='')
        if res.text == 'empty':
            self.user_table.setColumnCount(1)
            self.user_table.setRowCount(1)
            self.user_table.verticalHeader().setVisible(False)
            self.user_table.horizontalHeader().setVisible(False)
            newItem = QtWidgets.QTableWidgetItem('还没有用户...')
            newItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.user_table.setItem(0, 0, newItem)
            QtWidgets.QTableWidget.resizeRowsToContents(self.user_table)
        else:
            for button in self.delete_button:
                button.clicked.connect(self.delete_user)
            for button in self.update_button:
                button.clicked.connect(self.update_user)

    def send_name(self, name):
        self.sign_3.emit(name)

    def receive_name(self, name):
        self.admin_name = name
        self.menu_Button.setText('欢迎您，管理员' + self.admin_name)
        self.logout.setText('注销账户：' + self.admin_name)

    def closeEvent(self, event):
        self.Win_main = AdminMainForm()
        self.sign_3.connect(self.Win_main.receive_name)
        self.send_name(self.admin_name)
        self.hide()
        self.Win_main.show()

    def close(self):
        app.quit()

    def logout_admin(self):
        config.read('../config/admin.ini', encoding='utf-8')
        if config.has_section('Admin'):
            config.remove_section('Admin')
        config.write(open('../config/admin.ini', 'w', encoding='utf-8'))
        self.Win_login_1 = AdminLoginForm()
        self.hide()
        self.Win_login_1.show()

    def delete_user(self):
        uid = self.sender().user['uid']
        url = 'https://stepic-api.redcountry.top/api/user/delete'
        data = {'uname': self.sender().user['uname']}
        res = requests.post(url=url, data=data)
        if res.text == 'success':
            self.hide()
            for i in range(self.user_table.rowCount()):
                if self.user_table.item(i, 0).text() == str(uid):
                    self.user_table.removeRow(i)
                    break
            row = self.user_table.rowCount()
            if row == 0:
                self.user_table.setColumnCount(1)
                self.user_table.setRowCount(1)
                self.user_table.verticalHeader().setVisible(False)
                self.user_table.horizontalHeader().setVisible(False)
                newItem = QtWidgets.QTableWidgetItem('还没有用户...')
                newItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.user_table.setItem(0, 0, newItem)
                QtWidgets.QTableWidget.resizeRowsToContents(self.user_table)
            QMessageBox.information(self, '成功', '删除用户成功！', QMessageBox.Yes)
            self.show()
        else:
            QMessageBox.warning(self, '错误', '删除失败！', QMessageBox.Yes)

    def update_user(self):
        uid = self.sender().user['uid']
        uname = ''
        for i in range(self.user_table.rowCount()):
            if self.user_table.item(i, 0).text() == str(uid):
                uname = self.user_table.item(i, 1).text()
                break
        unick = ''
        for i in range(self.user_table.rowCount()):
            if self.user_table.item(i, 0).text() == str(uid):
                unick = self.user_table.item(i, 2).text()
                break
        sex = '未知'
        for man in self.man_radio:
            if man.user['uid'] == uid:
                if man.isChecked():
                    sex = '男'
                    break
        for woman in self.woman_radio:
            if woman.user['uid'] == uid:
                if woman.isChecked():
                    sex = '女'
                    break
        phone = ''
        for i in range(self.user_table.rowCount()):
            if self.user_table.item(i, 0).text() == str(uid):
                phone = self.user_table.item(i, 4).text()
                break
        birthday = ''
        for date in self.birthday_Edit:
            if date.user['uid'] == uid:
                birthday = str(date.date().toPyDate())
                break
        exper = ''
        for i in range(self.user_table.rowCount()):
            if self.user_table.item(i, 0).text() == str(uid):
                exper = self.user_table.item(i, 6).text()
                break
        intro = ''
        for i in range(self.user_table.rowCount()):
            if self.user_table.item(i, 0).text() == str(uid):
                intro = self.user_table.item(i, 7).text()
                break
        if phone != '' and (len(phone) != 11 or phone.isdigit() == False):
            QMessageBox.warning(self, '错误', '请输入正确的电话号码！', QMessageBox.Yes)
            item = QtWidgets.QTableWidgetItem('')
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            for i in range(self.user_table.rowCount()):
                if self.user_table.item(i, 0).text() == str(uid):
                    self.user_table.setItem(i, 4, item)
                    break
            return
        url = 'https://stepic-api.redcountry.top/api/user/update_user'
        data = {'uid': uid, 'uname': uname, 'unick': unick, 'sex': sex, 'phone': phone, 'birthday': birthday, 'exper': exper, 'intro': intro}
        res = requests.post(url=url, data=data)
        if res.text == 'success':
            self.hide()
            QMessageBox.information(self, '成功', '修改用户成功！', QMessageBox.Yes)
            self.show()
        else:
            QMessageBox.warning(self, '错误', '修改失败！', QMessageBox.Yes)


class AdminDeveloperForm(QtWidgets.QMainWindow, Ui_AdminDeveloperWindow):
    sign_4 = pyqtSignal(str)

    def __init__(self, parent=None):
        super(AdminDeveloperForm, self).__init__(parent)
        self.setupUi(self)
        self.exit_button.triggered.connect(self.close)
        self.logout.triggered.connect(self.logout_admin)
        url = 'https://stepic-api.redcountry.top/api/developer/query_all'
        res = requests.post(url=url, data='')
        if res.text == 'empty':
            self.developer_table.setColumnCount(1)
            self.developer_table.setRowCount(1)
            self.developer_table.verticalHeader().setVisible(False)
            self.developer_table.horizontalHeader().setVisible(False)
            newItem = QtWidgets.QTableWidgetItem('还没有开发者...')
            newItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.developer_table.setItem(0, 0, newItem)
            QtWidgets.QTableWidget.resizeRowsToContents(self.developer_table)
        else:
            for button in self.delete_button:
                button.clicked.connect(self.delete_developer)
            for button in self.update_button:
                button.clicked.connect(self.update_developer)

    def send_name(self, name):
        self.sign_4.emit(name)

    def receive_name(self, name):
        self.admin_name = name
        self.menu_Button.setText('欢迎您，管理员' + self.admin_name)
        self.logout.setText('注销账户：' + self.admin_name)

    def closeEvent(self, event):
        self.Win_main = AdminMainForm()
        self.sign_4.connect(self.Win_main.receive_name)
        self.send_name(self.admin_name)
        self.hide()
        self.Win_main.show()

    def close(self):
        app.quit()

    def logout_admin(self):
        config.read('../config/admin.ini', encoding='utf-8')
        if config.has_section('Admin'):
            config.remove_section('Admin')
        config.write(open('../config/admin.ini', 'w', encoding='utf-8'))
        self.Win_login_1 = AdminLoginForm()
        self.hide()
        self.Win_login_1.show()

    def delete_developer(self):
        did = self.sender().developer['did']
        url = 'https://stepic-api.redcountry.top/api/developer/delete'
        data = {'dname': self.sender().developer['dname']}
        res = requests.post(url=url, data=data)
        if res.text == 'success':
            self.hide()
            for i in range(self.developer_table.rowCount()):
                if self.developer_table.item(i, 0).text() == str(did):
                    self.developer_table.removeRow(i)
                    break
            row = self.developer_table.rowCount()
            if row == 0:
                self.developer_table.setColumnCount(1)
                self.developer_table.setRowCount(1)
                self.developer_table.verticalHeader().setVisible(False)
                self.developer_table.horizontalHeader().setVisible(False)
                newItem = QtWidgets.QTableWidgetItem('还没有开发者...')
                newItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.developer_table.setItem(0, 0, newItem)
                QtWidgets.QTableWidget.resizeRowsToContents(self.developer_table)
            QMessageBox.information(self, '成功', '删除开发者成功！', QMessageBox.Yes)
            self.show()
        else:
            QMessageBox.warning(self, '错误', '删除失败！', QMessageBox.Yes)

    def update_developer(self):
        did = self.sender().developer['did']
        dname = ''
        dnick = ''
        dphone = ''
        for i in range(self.developer_table.rowCount()):
            if self.developer_table.item(i, 0).text() == str(did):
                dname = self.developer_table.item(i, 1).text()
                dnick = self.developer_table.item(i, 2).text()
                dphone = self.developer_table.item(i, 3).text()
        if dphone != '' and (len(dphone) != 11 or dphone.isdigit() == False):
            QMessageBox.warning(self, '错误', '请输入正确的电话号码！', QMessageBox.Yes)
            item = QtWidgets.QTableWidgetItem('')
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            for i in range(self.developer_table.rowCount()):
                if self.developer_table.item(i, 0).text() == str(did):
                    item = QtWidgets.QTableWidgetItem('')
                    item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                    self.developer_table.setItem(i, 3, item)
                    break
            return
        url = 'https://stepic-api.redcountry.top/api/developer/update_info'
        data = {'dname': dname, 'dnick': dnick, 'dphone': dphone}
        res = requests.post(url=url, data=data)
        if res.text == 'success':
            self.hide()
            QMessageBox.information(self, '成功', '修改开发者成功！', QMessageBox.Yes)
            self.show()
        else:
            QMessageBox.warning(self, '错误', '修改失败！', QMessageBox.Yes)


class AdminGameForm(QtWidgets.QMainWindow, Ui_AdminGameWindow):
    sign_5 = pyqtSignal(str)

    def __init__(self, parent=None):
        super(AdminGameForm, self).__init__(parent)
        self.setupUi(self)
        self.exit_button.triggered.connect(self.close)
        self.logout.triggered.connect(self.logout_admin)
        url = 'https://stepic-api.redcountry.top/api/game/query_all'
        res = requests.post(url=url, data='')
        if res.text == 'empty':
            self.all_table.setColumnCount(1)
            self.all_table.setRowCount(1)
            self.all_table.verticalHeader().setVisible(False)
            self.all_table.horizontalHeader().setVisible(False)
            newItem = QtWidgets.QTableWidgetItem('还没有游戏...')
            newItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.all_table.setItem(0, 0, newItem)
            QtWidgets.QTableWidget.resizeRowsToContents(self.all_table)
        else:
            for button in self.delete_button:
                button.clicked.connect(self.delete_game)
        url_1 = 'https://stepic-api.redcountry.top/api/game/query_all_check'
        res_1 = requests.post(url=url_1, data='')
        if res_1.text == 'empty':
            self.review_table.setRowCount(1)
            self.review_table.setColumnCount(1)
            self.review_table.verticalHeader().setVisible(False)
            self.review_table.horizontalHeader().setVisible(False)
            item = QtWidgets.QTableWidgetItem('没有待审核的游戏...')
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.review_table.setItem(0, 0, item)
            QtWidgets.QTableWidget.resizeRowsToContents(self.review_table)
        else:
            for button in self.success_button:
                button.clicked.connect(self.success_game)
            for button in self.failed_button:
                button.clicked.connect(self.failed_game)

    def send_name(self, name):
        self.sign_5.emit(name)

    def receive_name(self, name):
        self.admin_name = name
        self.menu_Button.setText('欢迎您，管理员' + self.admin_name)
        self.logout.setText('注销账户：' + self.admin_name)

    def closeEvent(self, event):
        self.Win_main = AdminMainForm()
        self.sign_5.connect(self.Win_main.receive_name)
        self.send_name(self.admin_name)
        self.hide()
        self.Win_main.show()

    def close(self):
        app.quit()

    def logout_admin(self):
        config.read('../config/admin.ini', encoding='utf-8')
        if config.has_section('Admin'):
            config.remove_section('Admin')
        config.write(open('../config/admin.ini', 'w', encoding='utf-8'))
        self.Win_login_1 = AdminLoginForm()
        self.hide()
        self.Win_login_1.show()

    def delete_game(self):
        gid = self.sender().game['gid']
        url = 'https://stepic-api.redcountry.top/api/game/delete'
        data = {'gid': self.sender().game['gid']}
        res = requests.post(url=url, data=data)
        if res.text == 'success':
            self.hide()
            for i in range(self.all_table.rowCount()):
                if self.all_table.item(i, 0).text() == str(gid):
                    self.all_table.removeRow(i)
                    break
            row = self.all_table.rowCount()
            if row == 0:
                self.all_table.setColumnCount(1)
                self.all_table.setRowCount(1)
                self.all_table.verticalHeader().setVisible(False)
                self.all_table.horizontalHeader().setVisible(False)
                newItem = QtWidgets.QTableWidgetItem('还没有游戏...')
                newItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.all_table.setItem(0, 0, newItem)
                QtWidgets.QTableWidget.resizeRowsToContents(self.all_table)
            QMessageBox.information(self, '成功', '删除游戏成功！', QMessageBox.Yes)
            self.show()
        else:
            QMessageBox.warning(self, '错误', '删除失败！', QMessageBox.Yes)

    def success_game(self):
        gid = self.sender().game['gid']
        url = 'https://stepic-api.redcountry.top/api/game/check_pass'
        data = {'gid': self.sender().game['gid']}
        res = requests.post(url=url, data=data)
        if res.text == 'success':
            self.hide()
            for i in range(self.all_table.rowCount()):
                if self.all_table.item(i, 0).text() == str(gid):
                    item = QtWidgets.QTableWidgetItem('审核通过')
                    item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                    self.all_table.setItem(i, 6, item)
                    break
            for i in range(self.review_table.rowCount()):
                if self.review_table.item(i, 0).text() == str(gid):
                    self.review_table.removeRow(i)
                    break
            row = self.review_table.rowCount()
            if row == 0:
                self.review_table.setColumnCount(1)
                self.review_table.setRowCount(1)
                self.review_table.verticalHeader().setVisible(False)
                self.review_table.horizontalHeader().setVisible(False)
                item = QtWidgets.QTableWidgetItem('没有待审核的游戏...')
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.review_table.setItem(0, 0, item)
                QtWidgets.QTableWidget.resizeRowsToContents(self.review_table)
            QMessageBox.information(self, '成功', '审核游戏成功！', QMessageBox.Yes)
            self.show()
        else:
            QMessageBox.warning(self, '失败', '审核游戏失败！', QMessageBox.Yes)

    def failed_game(self):
        gid = self.sender().game['gid']
        url = 'https://stepic-api.redcountry.top/api/game/check_fail'
        data = {'gid': self.sender().game['gid']}
        res = requests.post(url=url, data=data)
        if res.text == 'success':
            self.hide()
            for i in range(self.all_table.rowCount()):
                if self.all_table.item(i, 0).text() == str(gid):
                    item = QtWidgets.QTableWidgetItem('审核失败')
                    item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                    self.all_table.setItem(i, 6, item)
                    break
            for i in range(self.review_table.rowCount()):
                if self.review_table.item(i, 0).text() == str(gid):
                    self.review_table.removeRow(i)
                    break
            row = self.review_table.rowCount()
            if row == 0:
                self.review_table.setColumnCount(1)
                self.review_table.setRowCount(1)
                self.review_table.verticalHeader().setVisible(False)
                self.review_table.horizontalHeader().setVisible(False)
                item = QtWidgets.QTableWidgetItem('没有待审核的游戏...')
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.review_table.setItem(0, 0, item)
                QtWidgets.QTableWidget.resizeRowsToContents(self.review_table)
            QMessageBox.information(self, '成功', '审核游戏成功！', QMessageBox.Yes)
            self.show()
        else:
            QMessageBox.warning(self, '失败', '审核游戏失败！', QMessageBox.Yes)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Win_login = AdminLoginForm()
    Win_login.show()
    sys.exit(app.exec_())
