from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog

# from PyQt5.QtGui import QRegExpValidator


class SaveSession(QDialog):
    def __init__(self, data):
        super().__init__()
        uic.loadUi("./ui/saveFile.ui", self)
        self.data_to_save = data

        self.file_name = self.findChild(QtWidgets.QLineEdit, "fileName")
        # TODO: set up a QRegExpValidator

        self.button_group = self.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        self.button_group.accepted.connect(lambda: self.get_button_value(True))
        self.button_group.rejected.connect(lambda: self.get_button_value(False))

    def get_button_value(self, isAccepted):
        if isAccepted:
            print(f"\n accepted: {self.file_name.text()}")
            # TODO: get cwd, save the file on this name
        else:
            print("\n rejected")
