from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from gui.register_user import RegisterUser
from utils.hyperlink import HyperlinkLabel
from utils.utils import open_dialog, send_new_password


class Login(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi("./ui/login.ui", self)
        self.parent_window = parent

        self.username = self.findChild(QtWidgets.QLineEdit, "username")
        self.password = self.findChild(QtWidgets.QLineEdit, "password")

        self.button_group = self.findChild(QDialogButtonBox, "buttonBox")
        self.button_group.accepted.connect(lambda: self.get_button_value(True))
        self.button_group.rejected.connect(lambda: self.get_button_value(False))

        self.sign_up = self.findChild(QtWidgets.QPushButton, "signUp")
        self.sign_up.clicked.connect(
            lambda: open_dialog(self.parent_window, RegisterUser)
        )

        self.forgot_password = HyperlinkLabel(self)
        self.forgot_password.setText("Forgot Password")
        self.forgot_password.move(20, 115)
        self.forgot_password.resize(80, 20)
        self.forgot_password.mouseReleaseEvent(
            lambda: send_new_password(self.username.text())
        )

    def get_button_value(self, isAccepted):
        if isAccepted:
            print(
                f"\n accepted!\nuser: {self.username.text()},\npassword: {self.password.text()}"
            )
            # TODO: get cwd, save the file on this name
        else:
            print("\n rejected")
