from statistics import mean
from PyQt5 import uic
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QOpenGLWidget,
    QListView,
    QFrame,
    QApplication,
)
#import pyqtgraph as pg
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets


from utils.templates import SCORE, MAX_ACC, PUNCH_TIME, SECONDARY_PUSH_AMPL, TOTAL_ENERGY, X_PERCENTAGE, TOTAL_ENERGY2
from utils.utils import go_to_previous_window, open_dialog, open_new_window
from gui.save_session import SaveSession
from gui.profile import Profile
from gui.karate_plots import PlotFeedback
from backend import global_vars
from database.training_db import save_training_session


# https://github.com/MagnoEfren/PyQt5/tree/main/Grafica%20con%20Matplotlib%20PyQt5

Ui_FeedbackWindow, BaseFeedbackWindow = uic.loadUiType("./ui/feedback.ui")
#QMainWindow, 
class Feedback(Ui_FeedbackWindow, BaseFeedbackWindow):

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        #uic.loadUi("./ui/feedback.ui", self)

        self.setupUi(self)
        self.grafica = PlotFeedback()
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        width = int(screen_geometry.width() * 0.9)
        height = int(screen_geometry.height() * 0.9)
        self.setGeometry(50, 50, width, height)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        #self.frame.resize(300,300)
        self.frame.setGeometry(30, 100, 1300, 900)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_grafica = QtWidgets.QVBoxLayout()
        self.verticalLayout_grafica.setObjectName("verticalLayout_grafica")
        self.horizontalLayout.addLayout(self.verticalLayout_grafica)

        self.frame_control = QtWidgets.QFrame(self.frame)
        self.frame_control.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_control.setStyleSheet("background-color: rgb(0, 170, 127);")
        self.frame_control.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_control.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_control.setObjectName("frame_control")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_control)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.parent_window = parent
        print("IN FEEDBACK WINDOW")
        self.verticalLayout_grafica.addWidget(self.grafica)

        toolbar = NavigationToolbar(self.grafica, self)
        toolbar.setStyleSheet("background-color: lightblue")
        self.verticalLayout_grafica.addWidget(self.grafica)
        self.verticalLayout_grafica.addWidget(toolbar)

        self.score = self.findChild(QLabel, "score")
        self.punch_time = self.findChild(QLabel, "punch_time")
        self.max_acc = self.findChild(QLabel, "max_acc")
        self.push_ampl = self.findChild(QLabel, "secondaryPushAmpl")
        self.total_e = self.findChild(QLabel, "total_energy")
        self.x_percentage = self.findChild(QLabel, "x_resultant_percentage")
        self.total_e2 = self.findChild(QLabel, "total_energy2")
        self.set_text()

        self.back = self.findChild(QPushButton, "back")
        self.back.clicked.connect(
            lambda: go_to_previous_window(self, self.parent_window)
        )

        self.profile = self.findChild(QtWidgets.QPushButton, "profile")
        self.profile.clicked.connect(lambda: open_new_window(self, Profile))

        self.save = self.findChild(QPushButton, "save")
        self.save.clicked.connect(self.save_data)

        #self.frame = self.findChild(QFrame, "qframe")
        #self.frame_control = self.findChild(QFrame, "qframecontrol")

    def set_text(self) -> None:
        
        #sc = int(mean(global_vars.currentMeasurementStats.Score))
        sc = global_vars.currentMeasurementStats.Score
        pT = global_vars.currentMeasurementStats.punchTime[1]
        mA = round(mean(global_vars.currentMeasurementStats.max_acc), 3)
        pA = mean(global_vars.currentMeasurementStats.secondaryPushAmpl)
        tE = round(mean(global_vars.currentMeasurementStats.total_energy), 3)
        xP = round(mean(global_vars.currentMeasurementStats.x_resultant_percentage), 3)
        tE2 = round(mean(global_vars.currentMeasurementStats.total_energy2), 3)

        self.score.setText(SCORE.format(str(sc)))
        self.punch_time.setText(PUNCH_TIME.format(str(pT)))
        self.max_acc.setText(MAX_ACC.format(str(mA)))
        self.push_ampl.setText(SECONDARY_PUSH_AMPL.format(str(pA)))
        self.total_e.setText(TOTAL_ENERGY.format(str(tE)))
        self.x_percentage.setText(X_PERCENTAGE.format(str(xP)))
        self.total_e2.setText(TOTAL_ENERGY2.format(str(tE2)))

    def save_data(self):
        # TODO save mechanism
        print("Saving data to DB.")
        # TODO override accept button not to close the whole app
        #open_dialog(self, SaveSession)
        save_training_session()
        print("Latest session was saved to the database")
