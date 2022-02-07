from csv import reader
from datetime import datetime
from random import randint

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QColorDialog, QWidget, \
    QMessageBox
from GUI.win_main import Ui_win_main
from GUI.win_plotsettings import Ui_win_plotsettings
import pyqtgraph
import numpy as np

windowtitle = "RC-Car Viewer"
data = []
plotcolor = np.array(["red", "blue", "yellow", "green", "magenta", "cyan", "white", "purple", "aqua", "lime", "pink", "grey"])
datatypes = np.array([[1, 3, "Orientation", "roll", "pitch", "yaw", "", 0, 1, 2, ""], [1, 3, "Acceleration", "ax", "ay", "az", "", 3, 4, 5, ""], [1, 1, "Temperature", "Temp", "", "", "", 6, "", "", ""], [1, 2, "Coordinates", "lat", "lng", "", "", 7, 8, "", ""], [1, 4, "Rotational Velocity", "rpm_rear_l", "rpm_rear_r", "rpm_front_l", "rpm_front_r", 9, 10, 11, 12], [1, 1, "Velocity", "vel_ms", "", "", "", 13, "", "", ""]])


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
        self.overview_to_table.clicked.connect(lambda: self.pageswitcher.setCurrentIndex(1))
        self.actionTable_View.triggered.connect(lambda: self.pageswitcher.setCurrentIndex(1))
        self.overview_to_plot.clicked.connect(lambda: self.pageswitcher.setCurrentIndex(2))
        self.actionPlot_View.triggered.connect(lambda: self.pageswitcher.setCurrentIndex(2))
        self.PlotSettings.clicked.connect(lambda: win_plotsettings.show())

    def plot(self, plotdata):
        timedata = []
        dataoffset = 0
        timeformat = "%Y-%m-%d %H:%M:%S.%f"
        for timeloop in range(1, len(plotdata)):
            timedata.append(datetime.strptime(plotdata[timeloop][0], timeformat))
        plotdata = plotdata[1:, 1:]
        for elements in range(len(datatypes)):
            for subelements in range(len(datatypes[elements, 7:])):
                try:
                    plotdata = np.delete(plotdata, int(datatypes[elements, subelements + 7]) - dataoffset, 1)
                    dataoffset += 1
                except:
                    pass
        plotdata = np.asarray(plotdata, dtype=float)
        timeaxis = pyqtgraph.DateAxisItem()
        self.graphWidget.clear()
        self.graphWidget.setAxisItems({'bottom': timeaxis})
        self.graphWidget.addLegend()
        for elements in range(len(datatypes)):
            for subelements in range(len(datatypes[elements, 7:])):
                #try:
                    pen = pyqtgraph.mkPen(color=plotcolor[int(datatypes[elements, subelements + 7])])
                    self.graphWidget.plot([xitem.timestamp() for xitem in timedata], plotdata[:, int(datatypes[elements, subelements + 7])], pen=pen, name=data[0][int(datatypes[elements, subelements + 7]) + 1])
                #except:
                    #pass TODO error fix here


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
        global plotcolor
        data = np.array(list(reader(datafile)))
        tempdata = data
        errortypes = []
        for yloop in range(len(data)):
            for xloop in range(len(data[yloop])):
                if data[yloop][xloop] == "error":
                    for typeloop in range(len(datatypes)):
                        if str(xloop) in datatypes[typeloop, 7:]:
                            errortypes.append(datatypes[typeloop, 2])
                            datatypes[typeloop, 0] = 2

        if not errortypes == []:
            msgBox = QMessageBox()
            msgBox.setText("There are errors in your datafile, the following categories are not being included: " + str(errortypes))
            msgBox.exec()
        data = tempdata
        self.table_tableview.resizeColumnsToContents()
        self.plot(data)
        self.populate_table(data)

        fileopen = True
        return fileopen

    def show_win_plotsettings(self):
        win_plotsettings.show()


class WinPlotsettings(QWidget, Ui_win_plotsettings):
    global plotcolor

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Plot Settings")
        self.dropdown_trace.addItems(datatypes[:, 2])
        self.visible_switch.clicked.connect(self.change_visibility)
        self.color_picker.clicked.connect(self.pick_color)
        self.color_picker.setEnabled(0)
        self.plotsettings_buttons.button(self.plotsettings_buttons.Ok).clicked.connect(self.save_settings)
        self.plotsettings_buttons.button(self.plotsettings_buttons.Apply).clicked.connect(self.apply_settings)
        self.plotsettings_buttons.button(self.plotsettings_buttons.Cancel).clicked.connect(self.discard_settings)
        self.dropdown_trace.currentIndexChanged.connect(self.refresh_visibibity_button)

    def refresh_visibibity_button(self):
        self.visible_switch.setChecked(datatypes[self.dropdown_trace.currentIndex(), 0])
        if self.visible_switch.isChecked():
            self.color_picker.setEnabled(1)
        else:
            self.color_picker.setEnabled(0)

    def change_visibility(self):
        if self.visible_switch.isChecked():
            self.color_picker.setEnabled(1)
            datatypes[self.dropdown_trace.currentIndex(), 0] = True
        else:
            self.color_picker.setEnabled(0)
            datatypes[self.dropdown_trace.currentIndex(), 0] = False

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
