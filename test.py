import sys

from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.users = {}

    def initUI(self):
        self.setWindowTitle("账户登录")
        self.setGeometry(1000, 700, 600, 400)

        self.layout = QVBoxLayout()

        self.username_label = QLabel("学号:")
        self.setGeometry(1000, 700, 600, 400)
        self.layout.addWidget(self.username_label)
        self.username_input = QLineEdit()
        self.layout.addWidget(self.username_input)

        self.password_label = QLabel("密码:")
        self.layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton("登录")
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_button)

        self.register_button = QPushButton("注册")
        self.register_button.clicked.connect(self.register)
        self.layout.addWidget(self.register_button)

        self.setLayout(self.layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username in self.users and self.users[username] == password:
            self.openHomePage()
        else:
            QMessageBox.warning(self, "错误", "用户名或密码错误")

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username in self.users:
            QMessageBox.warning(self, "错误", "该学号已注册")
        else:
            self.users[username] = password
            QMessageBox.information(self, "注册", "注册成功")

    def openHomePage(self):
        self.home_page = HomePage()
        self.home_page.show()


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("主页")
        self.layout = QVBoxLayout()
        self.link_label = QLabel('<a href="http://www.hdu.edu.cn">hdu.edu.cn</a>')
        self.link_label.setOpenExternalLinks(True)
        self.layout.addWidget(self.link_label)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
