import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from gui.karate_training import KarateTraining
from gui.data_collection import DataCollection
from gui.admin import Admin
from gui.login import Login

from utils.utils import open_new_window
from backend import global_vars


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./ui/mainWindow.ui", self)

        self.leave = self.findChild(QtWidgets.QPushButton, "leave")
        self.leave.clicked.connect(self.exit_window)

        self.login = self.findChild(QtWidgets.QPushButton, "login")
        self.login.clicked.connect(lambda: open_new_window(self, Login))

        self.training = self.findChild(QtWidgets.QPushButton, "karate_training")
        self.training.clicked.connect(lambda: open_new_window(self, KarateTraining))

        self.data_collection = self.findChild(QtWidgets.QPushButton, "data_collection")
        self.data_collection.clicked.connect(
            lambda: open_new_window(self, DataCollection)
        )

        self.admin = self.findChild(QtWidgets.QPushButton, "admin")
        self.admin.clicked.connect(lambda: open_new_window(self, Admin))

    def exit_window(self):
        self.close()

def main():
    global_vars.init()
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
