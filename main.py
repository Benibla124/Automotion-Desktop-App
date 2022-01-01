from PySide6.QtWidgets import QApplication, QMainWindow
from GUI.win_main import Ui_win_main


windowtitle = "RC-Car Viewer"


class WinMain(QMainWindow, Ui_win_main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(windowtitle)
        self.actionBeenden.triggered.connect(self.close)
        self.actionVollbild.triggered.connect(self.toggle_fullscreen)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()


desktop_app = QApplication()
win_main = WinMain()
win_main.show()
desktop_app.exec()
