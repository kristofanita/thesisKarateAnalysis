from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow

from utils.utils import go_to_previous_window


class Profile(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi("./ui/profile.ui", self)
        self.parent_window = parent

        self.back = self.findChild(QtWidgets.QPushButton, "back")
        self.back.clicked.connect(
            lambda: go_to_previous_window(self, self.parent_window)
        )

        self.personal_data = self.findChild(QtWidgets.QPushButton, "personalData")
        self.personal_data.clicked.connect(self.open_personal_data)

        self.saved_sessions = self.findChild(QtWidgets.QPushButton, "savedSession")
        self.saved_sessions.clicked.connect(self.open_saved_sessions)

        self.goals = self.findChild(QtWidgets.QPushButton, "goals")
        self.goals.clicked.connect(self.open_goals)

        self.improvement = self.findChild(QtWidgets.QPushButton, "improvement")
        self.improvement.clicked.connect(self.open_improvements)

        self.data_display = self.findChild(QtWidgets.QScrollArea, "dataView")

        self.data = self.findChild(QtWidgets.QLabel, "data")

    def open_personal_data(self):
        # some query
        res = "This is the personal data text."
        self.setText(res)

    def open_saved_sessions(self):
        # some query
        res = "This is the saves sessions text."
        self.setText(res)

    def open_goals(self):
        # some query
        res = "This is the goals text."
        self.setText(res)

    def open_improvements(self):
        # some query
        res = "This is the improvements text."
        self.setText(res)

    def setText(self, data):
        self.data.setText(data)
