import sys
import requests
import json
import os
import configparser
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from AdminLogin import Ui_AdminLoginWindow
from DeveloperRegist import Ui_DeveloperRegistWindow

config = configparser.RawConfigParser()


class AdminLoginForm(QtWidgets.QMainWindow, Ui_AdminLoginWindow):
    def __init__(self, parent=None):
        super(AdminLoginForm, self).__init__(parent)
        self.setupUi(self)
        self.read_config()
        self.loginButton.clicked.connect(self.login)
        self.exitBottun.clicked.connect(self.close)
        self.developer_regist_button.clicked.connect(self.developer_regist)

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
                QMessageBox.information(self, '成功', '登录成功！', QMessageBox.Yes)
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
        self.hide()
        Win_developer_regist.show()

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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Win_login = AdminLoginForm()
    Win_developer_regist = DeveloperRegistForm()
    Win_login.show()
    sys.exit(app.exec_())
