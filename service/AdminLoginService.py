import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QMessageBox
sys.path.append(r'D:\workspace\python\stepic\service')

from AdminLogin import Ui_AdminLoginWindow


class AdminLoginForm(QMainWindow, Ui_AdminLoginWindow):
    def __init__(self, parent=None):
        super(AdminLoginForm, self).__init__(parent)
        self.setupUi(self)
        self.loginButton.clicked.connect(self.login)
        self.exitBottun.clicked.connect(self.close)

    def login(self):
        admin = self.nametext.text()
        password = self.passwordtext.text()
        if len(admin) == 0 or len(password) == 0:
            QMessageBox.warning(self, "错误", "用户名和密码不得为空！", QMessageBox.Yes)
            return
        url = "http://106.13.236.185:5000/api/login_admin"
        data = {"username": admin, "password": password}
        res = requests.post(url=url, data=data)
        if res.text == "success":
            self.massage_success()
        else:
            QMessageBox.warning(self, "错误", "您的用户名或密码输入有误，请重新输入！", QMessageBox.Yes)
            self.passwordtext.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = AdminLoginForm()
    myWin.show()
    sys.exit(app.exec_())
