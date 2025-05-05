from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import (QWidget, QSlider, QTextEdit, QLabel, QPushButton, QScrollArea,QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random
import pickle
from sklearn.cluster import KMeans

from utils.utils import go_to_previous_window
from backend import global_vars


ML_path_list = [
    "/home/karate/karateProjectFullstack/machine_learning_models/maxAcc_totalE2_kmeans7.pkl",
    "/home/karate/karateProjectFullstack/machine_learning_models/maxAcc_xpercentage_kmeans5.pkl",
    "/home/karate/karateProjectFullstack/machine_learning_models/punchTime_totalE2_kmeans5.pkl",
    "/home/karate/karateProjectFullstack/machine_learning_models/totalE_dominantFreq_kmeans9.pkl",
    "/home/karate/karateProjectFullstack/machine_learning_models/totalE_totalE2_kmeans7.pkl"
]
labels_title_list=[
    ["Maximum acceleration", "lateral percentage of resultant acceleration", "Lateral energy lost"],
    ["Punch time", "total energy on the second wooden plate", "Punch effectiveness"],
    ["Total energy on the first wooden plate", "dominant frequency", "Attention for Makiwara hits back"],
    ["Total energy1", "Total energy2", "Energy transfer between the two wooden plates"],
    ["Maximum acceleration on surface level", "total energy on second wooden plate", "Special technique"]
]
suggestion_info=[
    "A practitioner who looses more energy in lateral dimension,\n could pay more attention on the straightness of the strike.\n Goal on the diagram: lower part - towards the right side.",
    "Practitioners’ goal could be a shorter blow time with higher total energy induced.\n In order to reach shorter punch time, right after you hit the Makiwara\n make sure to perform a second push as well, when you feel it hits back to your arm.",
    "This diagram helps you to focus on the secondary force and how strong it should be.\n As your results get mor to the upper side of the diagram, you need to increase the secondary force.",
    "Goal is to not only hit the surface with your hand,\n but improve a technique with your body which will increase the punch energy in the system.",
    "Goal is to perform the most energy in the system with the special technique.\n While you lower the maximum acceleration on the surface, try to involve more of your body weigth into the punch."
]
class Profile(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.initUI()
        self.parent_window = parent

    def initUI(self):
        self.setWindowTitle("Profile window")
        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.widget.setMinimumSize(5000,5000)
        #self.vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

        self.setGeometry(QRect(0, 0, 2000, 1000))
        self.title = QLabel("My Profile", self.widget)
        self.title.setFont(QFont("Verdana", 24))
        self.title.move(245, 25)
        self.title.resize(170, 50)

        self.title2 = QLabel("Analysis of trainings", self.widget)
        self.title2.setFont(QFont("Verdana", 20))
        self.title2.move(500, 300)
        self.title2.resize(300, 50)

        #5 plot az unsupervised ML modelleknek
        self.current_y = 450 # kezdo pozi, title alatt
        self.plot_height = 350
        self.spacing = 50

        for i in range(len(ML_path_list)):
            fig = Figure(figsize=(5,3))
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            #ax.plot([random.randint(0, 10) for _ in range(10)])

            with open(ML_path_list[i], 'rb') as f:
                model = pickle.load(f)
                centroids = model.cluster_centers_
                ax.scatter(centroids[:, 0], centroids[:, 1], marker='*')
                ax.set_xlabel(labels_title_list[i][0])
                ax.set_ylabel(labels_title_list[i][1])
                ax.set_title(labels_title_list[i][2])

            print(self.current_y)
            canvas.setParent(self.widget)
            canvas.move(50, self.current_y*(i+1)-50)
            canvas.resize(1200, self.plot_height+50)

            punch_info = QLabel('punch_info', self.widget)
            punch_info.setText(suggestion_info[i])
            punch_info.move(1300, self.current_y*(i+1))

        self.back = QPushButton(self.widget)
        self.back.setIcon(QIcon("/home/karate/karateProjectFullstack/assets/arrow_back.png"))
        self.back.setIconSize(QSize(50, 50))
        self.back.setFixedSize(50, 50)
        self.back.move(500, 25)
        self.back.clicked.connect(
            lambda: go_to_previous_window(self, self.parent_window)
        )

        self.leave = QPushButton(self.widget)
        self.leave.setIcon(QIcon("/home/karate/karateProjectFullstack/assets/close_50.png"))
        self.leave.setIconSize(QSize(50, 50))
        self.leave.setFixedSize(50, 50)
        self.leave.move(560, 25)
        self.leave.clicked.connect(self.exit_window)

        self.user_info = QLabel('This is label', self.widget)
        self.user_info.move(50, 150)
        self.user_info.setText(global_vars.current_user.print_user_data())


        #self.vbox.addWidget(self.back)

        #self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        #self.setGeometry(600, 100, 1000, 900)
        self.setWindowTitle('My Profile')
        self.show()

        return
    
    def exit_window(self):
        self.close()

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
