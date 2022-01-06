from csv import reader
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
from GUI.win_main import Ui_win_main
import numpy as np

windowtitle = "RC-Car Viewer"


class WinMain(QMainWindow, Ui_win_main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(windowtitle)
        self.actionBeenden.triggered.connect(self.close)
        self.action_ffnen.triggered.connect(self.openfile)

        self.actionVollbild.triggered.connect(self.toggle_fullscreen)
        self.actionOverview.triggered.connect(lambda: self.pageswitcher.setCurrentIndex(0))
        self.actionTable_View.triggered.connect(lambda: self.pageswitcher.setCurrentIndex(1))
        self.actionPlot_View.triggered.connect(lambda: self.pageswitcher.setCurrentIndex(2))

    def plot(self, x, y):
        self.graphWidget.plot(x, y)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def openfile(self):
        filepath = QFileDialog.getOpenFileName(self, self.tr("Open Data"), "/home", self.tr("*.txt *.csv"))
        try:
            datafile = open(filepath[0], 'r')
            data = np.array(list(reader(datafile)))
            self.table_tableview.setRowCount(len(data)-1)
            self.table_tableview.setColumnCount(len(data[1])-1)
            self.table_tableview.setHorizontalHeaderLabels(data[0][1:])
            self.table_tableview.setVerticalHeaderLabels(data[1:, 0])
            data = data[1:, 1:]

            for yloop in range(len(data)):
                for xloop in range(len(data[yloop])):
                    self.table_tableview.setItem(yloop, xloop, QTableWidgetItem(str(data[yloop][xloop])))
            self.table_tableview.resizeColumnsToContents()

            data = np.asarray(data, dtype=float)

            self.plot(data[:, 0], data[:, 1])

        except:
            print("Error reading file (No File selected?)")


desktop_app = QApplication()
win_main = WinMain()
win_main.show()
desktop_app.exec()
