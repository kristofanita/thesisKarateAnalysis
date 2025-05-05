import numpy as np
import pandas as pd
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QScrollArea
from PyQt5.QtGui import QScreen
import sys
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QTimer
from datetime import datetime, timedelta

from utils.utils import go_to_previous_window, open_new_window
from gui.profile import Profile
from gui.feedback import Feedback
from gui.karate_plots import PlotTraining
from backend.karateDeviceHardware import Makiwara
from backend.makiwaradataprocess import dataProcess
from backend import global_vars


Ui_KarateTrainingWindow, BaseFeedbackWindow = uic.loadUiType("./ui/karateTraining.ui")
#QMainWindow
class KarateTraining(Ui_KarateTrainingWindow, BaseFeedbackWindow):
    
    def __init__(self, parent):
        super().__init__()
        #uic.loadUi("./ui/karateTraining.ui", self)
        self.setupUi(self)
        self.grafica = None
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
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
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
        self.frame_control.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame_control.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_control.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_control.setObjectName("frame_control")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_control)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.parent_window = parent
        
        

        self.back = self.findChild(QtWidgets.QPushButton, "back")
        self.back.clicked.connect(
            lambda: go_to_previous_window(self, self.parent_window)
        )

        self.profile = self.findChild(QtWidgets.QPushButton, "profile")
        self.profile.clicked.connect(lambda: open_new_window(self, Profile))

        self.play = self.findChild(QtWidgets.QPushButton, "play")
        # <a target="_blank" href="https://icons8.com/icon/36067/circled-play">Play Button</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
        self.play.clicked.connect(self.press_play_pause)

        #self.pause = self.findChild(QtWidgets.QPushButton, "pause")
        #self.pause.clicked.connect(self.press_play_pause)
        #self.pause.setDisabled(True)
        
        self.stop = self.findChild(QtWidgets.QPushButton, "stop")
        self.stop.setEnabled(False)
        # <a target="_blank" href="https://icons8.com/icon/rIlhCoOzIUwg/stop-circled">Stop Circled</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
        self.stop.clicked.connect(self.stop_training)
        
        self.leave = self.findChild(QtWidgets.QPushButton, "leave")
        self.leave.clicked.connect(self.exit_window)
        #?self.graphicalView = self.findChild(QtWidgets.QGraphicsView, "graphicView")

    """def press_play_pause(self):
        buttonEnabled = self.play.isEnabled()
        self.play.setDisabled(not self.pause.isEnabled())
        self.pause.setDisabled(self.pause.isEnabled())
        self.makiwara.runMakiwara(buttonEnabled)
        """

    def exit_window(self):
        self.close()

    def press_play_pause(self):
        if self.play.isEnabled():
            try:
                global_vars.makiwara = Makiwara()
                global_vars.makiwara.runMakiwara1()

                self.grafica = PlotTraining()
                self.verticalLayout_grafica.addWidget(self.grafica)
            
            except AssertionError as e:
                print("Cannot start the p1, p2 processes again")
            
        # else:
        #     print("it relates to the pause functionality")
        #     if self.makiwara.p2.is_alive():
        #        self.makiwara.p2.terminate()
        #        print("TERMINATED")
        #        self.makiwara.convertData()
        #        dataProcess()
                
        #        self.grafica = Canvas_grafica_karate()
        #        self.verticalLayout_grafica.addWidget(self.grafica)
        
        self.play.setDisabled(True)
        self.stop.setEnabled(True)
        #self.play.setDisabled(not self.pause.isEnabled())
        #self.pause.setDisabled(self.pause.isEnabled())
        
        

    def stop_training(self):
        if global_vars.makiwara.p1.is_alive() | global_vars.makiwara.p2.is_alive():
                # self.makiwara.p1.terminate()
                global_vars.makiwara.p1.kill()
                # global_vars.t1.append(datetime.now().strftime("%y.%m.%d-%H:%M:%S.%f"))
                global_vars.makiwara.p2.kill()
                t_end2 = datetime.now() #.strptime("%y.%m.%d-%H:%M:%S.%f")
                print("TERMINATED")             # '%Y.%m.%d-%H:%M:%S.%f'
                global_vars.makiwara.convertData(t_end2)
                print("starting to process data")
                punch_detected = False
                try:
                    punch_detected = dataProcess()
                except Exception as e:
                    print(e)
                    self.close()
                if not punch_detected:
                    #self.grafica = Canvas_grafica_karate()
                    self.grafica.timer.stop()
                    self.grafica.grafica_datos()
                    toolbar = NavigationToolbar(self.grafica, self)
                    toolbar.setStyleSheet("background-color: lightblue")
                    #self.verticalLayout_grafica.addWidget(self.grafica)
                    self.verticalLayout_grafica.addWidget(toolbar)
                else:
                    open_new_window(self, Feedback)
                """global_vars.rawDataFrame = pd.read_csv("/home/karate/karateProjectFullstack/data/GLaci_1_2.csv")
                num_points = len(global_vars.rawDataFrame)
                global_vars.time_vector = global_vars.makiwara.generate_time_vector(global_vars.makiwara.t1[0], t_end2, num_points)
                dataProcess()
                open_new_window(self, Feedback)"""
        self.stop.setDisabled(True)
        self.play.setDisabled(False)
