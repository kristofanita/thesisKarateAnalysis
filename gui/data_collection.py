from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QMainWindow
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5 import QtCore, QtGui
from datetime import datetime, timedelta

from utils.utils import go_to_previous_window
from backend.karateDeviceHardware import Makiwara
from backend.makiwaradataprocess import dataProcess
from backend import global_vars


Ui_DataCollectionWindow, BaseFeedbackWindow = uic.loadUiType("./ui/dataCollection.ui")
#QMainWindow
class DataCollection(Ui_DataCollectionWindow, BaseFeedbackWindow):
    # makiwara = Makiwara()
    def __init__(self, parent):
        super().__init__()
        #uic.loadUi("./ui/dataCollection.ui", self)
        self.setupUi(self)
        self.grafica = None
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        #self.frame.resize(300,300)
        self.frame.setGeometry(30, 150, 600, 550)
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

        self.back = self.findChild(QtWidgets.QPushButton, "back")
        self.back.clicked.connect(
            lambda: go_to_previous_window(self, self.parent_window)
        )

        self.play = self.findChild(QtWidgets.QPushButton, "play")
        self.play.clicked.connect(self.press_play_pause)

        self.pause = self.findChild(QtWidgets.QPushButton, "pause")
        self.pause.clicked.connect(self.press_play_pause)
        self.pause.setDisabled(True)
        
        #self.graphicalView = self.findChild(QtWidgets.QGraphicsView, "graphicView")

        self.timeInput = self.findChild(QtWidgets.QLineEdit, "timeInput")
        int_validator = QIntValidator(0, 255, self.timeInput)
        self.timeInput.setValidator(int_validator)
        self.timeInput.textChanged.connect(self.get_time_input)

    def press_play_pause(self):
        if self.play.isEnabled():
            print("it relates to the play functionality")
            self.makiwara.runMakiwara1()
            print("Data collection finished")
            
            
            
        else:
            print("it relates to the pause functionality")
            if self.makiwara.p2.is_alive():
                self.makiwara.p2.terminate()
                print("TERMINATED")
                self.makiwara.convertData()
                dataProcess()
                print(global_vars.currentMeasurementStats.head())
                self.grafica = Canvas_grafica_karate()
                self.verticalLayout_grafica.addWidget(self.grafica)
        
        # set values to the opposite
        self.play.setDisabled(not self.pause.isEnabled())
        self.pause.setDisabled(self.pause.isEnabled())
        
    def get_time_input(self):
        print(self.timeInput.text(), type(self.timeInput))
        global_vars.timeInput = int(self.timeInput.text())



class Canvas_grafica_karate(FigureCanvas):
    def __init__(self, parent=None):     
        self.fig = plt.figure(figsize=(5, 5))
        super().__init__(self.fig) 
        self.grafica_datos()


    def generate_timevector(self):
        start = global_vars.start_time
        end = global_vars.end_time
        n_points = len(global_vars.rawDataFrame.X2)

        start_dateTime = datetime.strptime(start, "%Y.%m.%d-%H:%M:%S.%f")
        end_dateTime = datetime.strptime(end, "%Y.%m.%d-%H:%M:%S.%f")

        time_diff = end_dateTime - start_dateTime
        time_step = time_diff / (n_points - 1)

        tmp = [start_dateTime + i * time_step for i in range(n_points)]
        global_vars.time_vector = list(map(lambda dt: dt.strftime("%H:%M:%S"), tmp))
        #.append(t_vec)

    def grafica_datos(self):
        self.generate_timevector()
        matplotlib.rc('xtick', labelsize=6)

        plt.plot(global_vars.time_vector, global_vars.rawDataFrame.X1)
        plt.plot(global_vars.time_vector, global_vars.rawDataFrame.Y1)
        plt.plot(global_vars.time_vector, global_vars.rawDataFrame.Z1)
        plt.xticks(rotation=45)
        plt.title("Accelerometer signals")
        plt.xlabel("Time: H:M:S")
        plt.ylabel("Acceleration [G]")
        #plt.close()

        QtCore.QTimer.singleShot(10, self.grafica_datos)
