import sys
import requests
import json
import datetime
import configparser
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal

from AdminLogin import Ui_AdminLoginWindow
from DeveloperRegist import Ui_DeveloperRegistWindow
from AdminMain1 import Ui_AdminMainWindow
from AdminUser1 import  Ui_AdminUserWindow

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
            url = "http://106.13.236.185:5000/api/login_admin"
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
            url = 'http://106.13.236.185:5000/api/login_developer'
            data = {'username': username, 'password': password}
            res = requests.post(url=url, data=data)
            if res.text == "success":
                if self.checkBox.isChecked():
                    self.write_config()
                QMessageBox.information(self, '成功', '登录成功！', QMessageBox.Yes)
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
        url = "http://106.13.236.185:5000/api/regit_developer"
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

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "退出", "您是否确定退出本平台？", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            app.quit()
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


class AdminUserForm(QtWidgets.QMainWindow, Ui_AdminUserWindow):
    sign_3 = pyqtSignal(str)

    def __init__(self, parent=None):
        super(AdminUserForm, self).__init__(parent)
        self.setupUi(self)
        self.exit_button.triggered.connect(self.close)
        self.logout.triggered.connect(self.logout_admin)
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
        url = 'http://106.13.236.185:5000/api/user/delete'
        data = {'uname': self.sender().user['uname']}
        res = requests.post(url=url, data=data)
        if res.text == 'success':
            self.hide()
            self.user_table.removeRow(self.sender().id)
            QMessageBox.information(self, '成功', '删除用户成功', QMessageBox.Yes)
            self.show()
        else:
            QMessageBox.warning(self, '错误', '删除失败', QMessageBox.Yes)

    def update_user(self):
        id = self.sender().id
        uid = self.user_table.item(id, 0).text()
        uname = self.user_table.item(id, 1).text()
        unick = self.user_table.item(id, 2).text()
        sex = '未知'
        for man in self.man_radio:
            if man.id == id:
                if man.isChecked():
                    sex = '男'
                    break
        for woman in self.woman_radio:
            if woman.id == id:
                if woman.isChecked():
                    sex = '女'
                    break
        phone = self.user_table.item(id, 4).text()
        birthday = ''
        for date in self.birthday_Edit:
            if date.id == id:
                birthday = str(date.date().toPyDate())
                break
        exper = self.user_table.item(id, 6).text()
        intro = self.user_table.item(id, 7).text()
        if phone != '' and (len(phone) != 11 or phone.isdigit() == False):
            QMessageBox.warning(self, '错误', '请输入正确的电话号码！', QMessageBox.Yes)
            item = QtWidgets.QTableWidgetItem('')
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.user_table.setItem(id, 4, item)
            return
        url = 'http://106.13.236.185:5000/api/user/update_user'
        data = {'uid': uid, 'uname': uname, 'unick': unick, 'sex': sex, 'phone': phone, 'birthday': birthday, 'exper': exper, 'intro': intro}
        res = requests.post(url=url, data= data)
        if res.text == 'success':
            self.hide()
            QMessageBox.information(self, '成功', '修改用户成功', QMessageBox.Yes)
            self.show()
        else:
            QMessageBox.warning(self, '错误', '修改失败', QMessageBox.Yes)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Win_login = AdminLoginForm()
    Win_login.show()
    sys.exit(app.exec_())
