from PyQt5.QtWidgets import QLabel


class HyperlinkLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__()
        self.setOpenExternalLinks(True)
        self.setParent(parent)

    def mouseReleaseEvent(self, method):
        # QMouseEvent is added insted of the lambda function
        # TODO fix this
        print("sending a username?")
        # method()
