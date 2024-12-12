from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLineEdit


class RegisterUser(QDialog):

    def __init__(self, parent=None) -> None:
        super().__init__()
        uic.loadUi("./ui/registerUser.ui", self)
        self.parent_window = parent

        # TODO validation for the fields below + compate pwd+pwd2
        self.username = self.findChild(QLineEdit, "username")
        self.password = self.findChild(QLineEdit, "password")
        self.password_again = self.findChild(QLineEdit, "passwordAgain")
        self.email = self.findChild(QLineEdit, "email")

        self.button_group = self.findChild(QDialogButtonBox, "buttonBox")
        self.button_group.accepted.connect(self.send_form_data)

    def send_form_data(self):
        print(
            self.username.text(),
            self.password.text(),
            self.password_again.text(),
            self.email.text(),
        )
