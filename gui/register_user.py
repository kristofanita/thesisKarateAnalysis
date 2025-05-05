from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLineEdit, QCheckBox

from database.users_db import register_new_user


class RegisterUser(QDialog):

    def __init__(self, main_window) -> None:
        print("IN REGISTER_USER")
        super().__init__()
        uic.loadUi("./ui/registerUser.ui", self)
        self.main_window = main_window

        # TODO validation for the fields below + compate pwd+pwd2
        self.username = self.findChild(QLineEdit, "username")
        self.password = self.findChild(QLineEdit, "password")
        self.password.setEchoMode(QLineEdit.Password)
        self.show_pwd = self.findChild(QCheckBox, "show_pwd")
        self.show_pwd.stateChanged.connect(self.toggle_pwd_visible)
        self.password_again = self.findChild(QLineEdit, "passwordAgain")
        self.password_again.setEchoMode(QLineEdit.Password)
        self.email = self.findChild(QLineEdit, "email")
        self.birth = self.findChild(QLineEdit, "birth")
        self.height_p = self.findChild(QLineEdit, "height")
        self.weight = self.findChild(QLineEdit, "weight")

        self.button_group = self.findChild(QDialogButtonBox, "buttonBox")
        self.button_group.accepted.connect(self.send_form_data)
        #self.button_group.rejected.connect(self.goback)
        

    def send_form_data(self):
        print(
            self.username.text(),
            self.password.text(),
            self.password_again.text(),
            self.email.text(),
            self.birth.text(),
            self.height_p.text(),
            self.weight.text(),
        )
        if self.password.text() == self.password_again.text():
            register_new_user(self.username.text(), self.password.text(), self.email.text(), self.birth.text(), self.height_p.text(), self.weight.text())
        
        else:
            print("password mismatch")

    def toggle_pwd_visible(self):
        if self.show_pwd.isChecked():
            self.password.setEchoMode(QLineEdit.Normal)
            self.password_again.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)
            self.password_again.setEchoMode(QLineEdit.Password)
