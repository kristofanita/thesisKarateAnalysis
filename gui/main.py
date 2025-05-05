import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QPalette, QColor

from gui.karate_training import KarateTraining
from gui.login import Login, LoginFailedException

from utils.utils import open_new_window
from backend import global_vars


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./ui/mainWindow.ui", self)

        self.training = self.findChild(QtWidgets.QPushButton, "karate_training")
        self.training.setEnabled(False)
        self.training.clicked.connect(lambda: open_new_window(self, KarateTraining))


        self.leave = self.findChild(QtWidgets.QPushButton, "leave")
        self.leave.clicked.connect(self.exit_window)

        self.login = self.findChild(QtWidgets.QPushButton, "login")
        #self.login.clicked.connect(lambda: open_new_window(self, Login))
        self.login.clicked.connect(self.user_login)

        if global_vars.current_user is not None: # tehat sikeres login volt
            self.training.setEnabled(True)
            self.login.setEnabled(False)

        
    def exit_window(self):
        self.close()

    def user_login(self):
        try:
            login_dialog = Login(self)
            login_dialog.exec_()
        except LoginFailedException as e:
            QMessageBox.critical(None, "Error:", str(e))
        if global_vars.current_user is not None: # tehat sikeres login volt
            self.training.setEnabled(True)
            self.login.setEnabled(False)

def main():
    try:
        global_vars.init()
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(243, 255, 255)) # 173, 216, 230
        palette.setColor(QPalette.WindowText, QColor('black'))
        app.setPalette(palette)
        win = MainWindow()
        win.show()
    except Exception as e:
        print(e)
    finally:
        sys.exit(app.exec())
