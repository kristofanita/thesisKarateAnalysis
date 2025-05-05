from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea,QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic

from utils.utils import go_to_previous_window


Ui_ProfileWindow, BaseFeedbackWindow = uic.loadUiType("./ui/profile.ui")
class ProfileCopy(Ui_ProfileWindow, BaseFeedbackWindow):
    def __init__(self, parent):
        super().__init__()
        
        #
        self.parent_window = parent
        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

        self.vbox.addWidget(self.back)

        self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        #self.setCentralWidget(self.scroll)

        uic.loadUi("./ui/profile.ui", self)
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




        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

        self.vbox.addWidget(self.back)

        self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)
        
        #self.initUI()


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
