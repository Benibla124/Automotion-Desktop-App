from csv import reader
from datetime import datetime
from random import randint

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QColorDialog, QWidget
from GUI.win_main import Ui_win_main
from GUI.win_plotsettings import Ui_win_plotsettings
import pyqtgraph
import numpy as np

windowtitle = "RC-Car Viewer"
data = []
plotvisibility = []
plotcolor = []


def randcolor():
    color = [randint(0, 255), randint(0, 255), randint(0, 255)]
    return color


class WinMain(QMainWindow, Ui_win_main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(windowtitle)
        openedfile = False
        while not openedfile:
            openedfile = self.openfile()
        self.actionBeenden.triggered.connect(self.close)
        self.action_ffnen.triggered.connect(self.openfile)
        self.actionVollbild.triggered.connect(self.toggle_fullscreen)
        self.actionOverview.triggered.connect(lambda: self.pageswitcher.setCurrentIndex(0))
        self.actionTable_View.triggered.connect(lambda: self.pageswitcher.setCurrentIndex(1))
        self.actionPlot_View.triggered.connect(lambda: self.pageswitcher.setCurrentIndex(2))
        self.PlotSettings.clicked.connect(lambda: win_plotsettings.show())

    def plot(self, plotdata):
        timedata = []
        timeformat = "%Y-%m-%d %H:%M:%S.%f"
        for timeloop in range(1, len(plotdata)):
            timedata.append(datetime.strptime(plotdata[timeloop][0], timeformat))
        plotdata = plotdata[1:, 1:]
        plotdata = np.asarray(plotdata, dtype=float)
        timeaxis = pyqtgraph.DateAxisItem()
        # pen = pyqtgraph.mkPen(color=(0, 0, 255))  # make own pen
        self.graphWidget.clear()
        self.graphWidget.setAxisItems({'bottom': timeaxis})
        # self.graphWidget.setBackground('w') # set white background
        self.graphWidget.addLegend()
        for category in range(len(plotdata[0])):
            if plotvisibility[category]:
                pen = pyqtgraph.mkPen(color=plotcolor[category])
                self.graphWidget.plot([xitem.timestamp() for xitem in timedata], plotdata[:, category], pen=pen, name=data[0][category+1])

    def populate_table(self, tabledata):
        self.table_tableview.setRowCount(len(tabledata)-1)
        self.table_tableview.setColumnCount(len(tabledata[1])-1)
        self.table_tableview.setHorizontalHeaderLabels(tabledata[0][1:])
        self.table_tableview.setVerticalHeaderLabels(tabledata[1:, 0])
        tabledata = tabledata[1:, 1:]
        for yloop in range(len(tabledata)):
            for xloop in range(len(tabledata[yloop])):
                self.table_tableview.setItem(yloop, xloop, QTableWidgetItem(str(tabledata[yloop][xloop])))
        self.table_tableview.resizeColumnsToContents()

    def toggle_fullscreen(self):
        if not self.actionVollbild.isChecked():
            self.showNormal()
        else:
            self.showFullScreen()

    def openfile(self):
        filepath = QFileDialog.getOpenFileName(self, self.tr("Open Data"), "/home/blacher", self.tr("*.txt *.csv"))
        datafile = open(filepath[0], 'r')
        global data
        global plotvisibility
        global plotcolor
        data = np.array(list(reader(datafile)))

        for category in range(1, len(data[0])):
            print(category)
            if data[0][category] == 'ax' or data[0][category] == 'ay' or data[0][category] == 'az':
                plotvisibility.append(True)
            else:
                plotvisibility.append(False)
            plotcolor.append(randcolor())

        self.plot(data)
        self.populate_table(data)

        fileopen = True
        return fileopen

    def show_win_plotsettings(self):
        win_plotsettings.show()


class WinPlotsettings(QWidget, Ui_win_plotsettings):
    global plotvisibility
    global plotcolor

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Plot Settings")
        self.dropdown_trace.addItems(data[0][1:])
        self.visible_switch.clicked.connect(self.change_visibility)
        self.color_picker.clicked.connect(self.pick_color)
        self.color_picker.setEnabled(0)
        self.plotsettings_buttons.button(self.plotsettings_buttons.Ok).clicked.connect(self.save_settings)
        self.plotsettings_buttons.button(self.plotsettings_buttons.Apply).clicked.connect(self.apply_settings)
        self.plotsettings_buttons.button(self.plotsettings_buttons.Cancel).clicked.connect(self.discard_settings)
        self.dropdown_trace.currentIndexChanged.connect(self.refresh_visibibity_button)

    def refresh_visibibity_button(self):
        self.visible_switch.setChecked(plotvisibility[self.dropdown_trace.currentIndex()])
        if self.visible_switch.isChecked():
            self.color_picker.setEnabled(1)
        else:
            self.color_picker.setEnabled(0)

    def change_visibility(self):
        if self.visible_switch.isChecked():
            self.color_picker.setEnabled(1)
            plotvisibility[self.dropdown_trace.currentIndex()] = True
        else:
            self.color_picker.setEnabled(0)
            plotvisibility[self.dropdown_trace.currentIndex()] = False

    def pick_color(self):
        color = QColorDialog.getColor()
        plotcolor[self.dropdown_trace.currentIndex()] = color

    def apply_settings(self):
        win_main.plot(data)

    def save_settings(self):
        win_main.plot(data)
        self.close()

    def discard_settings(self):

        self.close()


desktop_app = QApplication()
win_main = WinMain()
win_plotsettings = WinPlotsettings()
win_main.show()
desktop_app.exec()
