from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QMainWindow, QLineEdit, QCheckBox

from gui.register_user import RegisterUser
from utils.hyperlink import HyperlinkLabel
from utils.utils import open_dialog, send_new_password
from database.users_db import verify_user
from utils.utils import open_new_window, go_to_previous_window
from gui.karate_training import KarateTraining
from backend import global_vars


class Login(QDialog):
    def __init__(self, main_window):
        super().__init__()
        uic.loadUi("./ui/login.ui", self)
        self.main_window = main_window

        self.email = self.findChild(QtWidgets.QLineEdit, "email")
        self.password = self.findChild(QtWidgets.QLineEdit, "password")
        self.password.setEchoMode(QLineEdit.Password)
        self.show_pwd = self.findChild(QCheckBox, "show_pwd")
        self.show_pwd.stateChanged.connect(self.toggle_pwd_visible)

        self.button_group = self.findChild(QDialogButtonBox, "buttonBox")
        self.button_group.accepted.connect(lambda: self.get_button_value(True))
        self.button_group.rejected.connect(lambda: self.get_button_value(False))

        self.sign_up = self.findChild(QtWidgets.QPushButton, "signUp")
        #self.sign_up.clicked.connect(
        #    lambda: open_dialog(main_window, RegisterUser)
        #)
        self.sign_up.clicked.connect(lambda: open_new_window(self, RegisterUser))

        #self.forgot_password = HyperlinkLabel(self)
        #self.forgot_password.setText("Forgot Password")
        #self.forgot_password.move(20, 115)
        #self.forgot_password.resize(80, 20)
        #self.forgot_password.mouseReleaseEvent(
        #    lambda: send_new_password(self.email.text())
        #)

    def get_button_value(self, isAccepted):
        if isAccepted:
            print(
                f"\n accepted!\nuser: {self.email.text()},\npassword: {self.password.text()}"
            )
            if verify_user(self.email.text(), self.password.text()):
                self.main_window.show()
                self.accept()
            else:
                self.main_window.show()
                #raise LoginFailedException()
        else:
            print("\n rejected")# ez a cancel gomb
            self.reject()

    def toggle_pwd_visible(self):
        if self.show_pwd.isChecked():
            self.password.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)


class LoginFailedException(Exception):
    def __init__(self, message="Loigin failed: invalid username or password"):
        super().__init__(message)
        pass
