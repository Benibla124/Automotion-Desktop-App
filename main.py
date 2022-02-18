from csv import reader
from datetime import datetime
from random import randint

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox, \
    QGraphicsPixmapItem, QGraphicsScene, QWidget
from GUI.win_main import Ui_win_main
from GUI.win_plotsettings import Ui_win_plotsettings
import pyqtgraph
import os
import numpy as np
import staticmaps

windowtitle = "RC-Car Viewer"
data = []
plots = []
plotcolor = np.array(["red", "blue", "yellow", "green", "magenta", "cyan", "white", "purple", "aqua", "lime", "pink", "grey"])
datatypes = np.array([[1, 3, "Orientation", "roll", "pitch", "yaw", "", 0, 1, 2, ""], [1, 3, "Acceleration", "ax", "ay", "az", "", 3, 4, 5, ""], [0, 1, "Temperature", "Temp", "", "", "", 6, "", "", ""], [1, 4, "Rotational Velocity", "rpm_rear_l", "rpm_rear_r", "rpm_front_l", "rpm_front_r", 7, 8, 9, 10], [1, 1, "Velocity", "vel_ms", "", "", "", 11, "", "", ""], [0, 2, "Coordinates", "lat", "lng", "", "", 12, 13, "", ""]])
context = staticmaps.Context()
context.set_tile_provider(staticmaps.tile_provider_OSM)


def plots_update_views():
    global plots
    for noofplots in range(1, len(plots)):
        plots[noofplots].setGeometry(plots[0].vb.sceneBoundingRect())
        plots[noofplots].linkedViewChanged(plots[0].vb, plots[noofplots].XAxis)


def find_element(axis, axisnumber, loopnumber, target):
    for elements in axis:
        try:
            axis.index(loopnumber)
            target.append(axisnumber)
            break
        except:
            pass
    return target


def randcolor():
    color = [randint(0, 255), randint(0, 255), randint(0, 255)]
    return color


class WinMain(QMainWindow, Ui_win_main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(windowtitle)
        if not os.path.exists('temp'):  # If the temp path doesn't exit, create it
            os.makedirs('temp')
        try:
            for filename in os.listdir("./temp/"):
                os.remove("./temp/" + filename)
        except:
            pass
        car_pixmap = QPixmap("GUI/Car_Render.png")
        car_item = QGraphicsPixmapItem(car_pixmap)
        car_scene = QGraphicsScene(self)
        car_scene.addItem(car_item)
        self.main_Car.setScene(car_scene)
        openedfile = False
        while not openedfile:
            openedfile = self.openfile()
        self.actionBeenden.triggered.connect(self.close)
        self.actionVollbild.triggered.connect(self.toggle_fullscreen)
        self.actionOverview.triggered.connect(lambda: self.pageswitcher.setCurrentIndex(0))
        self.overview_to_table.clicked.connect(lambda: self.pageswitcher.setCurrentIndex(1))
        self.actionTable_View.triggered.connect(lambda: self.pageswitcher.setCurrentIndex(1))
        self.overview_to_plot.clicked.connect(lambda: self.pageswitcher.setCurrentIndex(2))
        self.actionPlot_View.triggered.connect(lambda: self.pageswitcher.setCurrentIndex(2))
        self.overview_to_map.clicked.connect(lambda: self.pageswitcher.setCurrentIndex(3))
        self.actionMap_View.triggered.connect(lambda: self.pageswitcher.setCurrentIndex(3))
        self.MapLoadButton.clicked.connect(self.draw_map)
        self.styleSatellite.clicked.connect(self.map_satellite)
        self.styleMap.clicked.connect(self.map_map)
        self.PlotSettings.clicked.connect(lambda: win_plotsettings.show())

    def map_satellite(self):
        context.set_tile_provider(staticmaps.tile_provider_ArcGISWorldImagery)
        self.draw_map()

    def map_map(self):
        context.set_tile_provider(staticmaps.tile_provider_OSM)
        self.draw_map()

    def plot(self, plotdata, axis1, axis2, axis3):
        global plots
        timedata = []
        dataoffset = 0
        timeformat = "%Y-%m-%d %H:%M:%S.%f"
        for timeloop in range(1, len(plotdata)):
            timedata.append(datetime.strptime(plotdata[timeloop][0], timeformat))
        plotdata = plotdata[1:, 1:]
        for elements in range(len(datatypes)):
            if int(datatypes[elements, 0]) == 2:
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
        dataoffset = 0
        plotcategories = datatypes[:, 2]

        if not np.array(axis3).size == 0:
            axisneeded = 3
        elif not np.array(axis2).size == 0:
            axisneeded = 2
        elif not np.array(axis1).size == 0:
            axisneeded = 1
        else:
            axisneeded = 0

        axis1label = ""
        axis2label = ""
        axis3label = ""

        for axis1loop in range(len(axis1)):
            if not axis1loop == 0:
                axis1label = axis1label + ", "
            axis1label = axis1label + plotcategories[axis1[axis1loop]]

        for axis2loop in range(len(axis2)):
            if not axis2loop == 0:
                axis2label = axis2label + ", "
            axis2label = axis2label + plotcategories[axis2[axis2loop]]

        for axis3loop in range(len(axis3)):
            if not axis3loop == 0:
                axis3label = axis3label + ", "
            axis3label = axis3label + plotcategories[axis3[axis3loop]]

        if axisneeded >= 1:
            plots = [self.graphWidget.plotItem]
            plots[0].setLabels(left=axis1label)

            if axisneeded >= 2:
                plots.append(pyqtgraph.ViewBox())
                plots[0].showAxis('right')
                plots[0].scene().addItem(plots[1])
                plots[0].getAxis('right').linkToView(plots[1])
                plots[1].setXLink(plots[0])
                plots[0].getAxis('right').setLabel(axis2label)

                if axisneeded == 3:
                    plots.append(pyqtgraph.ViewBox())
                    ax3 = pyqtgraph.AxisItem('right')
                    plots[0].layout.addItem(ax3, 2, 3)
                    plots[0].scene().addItem(plots[2])
                    ax3.linkToView(plots[2])
                    plots[2].setXLink(plots[0])
                    ax3.setZValue(-10000)
                    ax3.setLabel(axis3label)

        whichaxis = []

        for loopall in range(len(datatypes) - 1):
            whichaxis = find_element(axis1, 0, loopall, whichaxis)
            whichaxis = find_element(axis2, 1, loopall, whichaxis)
            whichaxis = find_element(axis3, 2, loopall, whichaxis)

        if not axisneeded == 0:
            plots_update_views()
            plots[0].vb.sigResized.connect(plots_update_views)

        axiscounter = 0

        for elements in range(len(datatypes)):
            if int(datatypes[elements, 0]) == 2:
                dataoffset = dataoffset + int(datatypes[elements, 1])
            elif int(datatypes[elements, 0]) == 0:
                pass
            elif int(datatypes[elements, 0]) == 1:
                for subelements in range(len(datatypes[elements, 7:])):
                    try:
                        indexnumber = int(datatypes[elements, subelements + 7]) - dataoffset
                        pen = pyqtgraph.mkPen(color=plotcolor[indexnumber + dataoffset])
                        if whichaxis == 0:
                            plots[whichaxis[axiscounter]].plot([xitem.timestamp() for xitem in timedata], plotdata[:, indexnumber], pen=pen, name=data[0][indexnumber + 1 + dataoffset])
                        else:
                            plots[whichaxis[axiscounter]].addItem(pyqtgraph.PlotCurveItem([xitem.timestamp() for xitem in timedata], plotdata[:, indexnumber], pen=pen, name=data[0][indexnumber + 1 + dataoffset]))
                    except:
                        pass
                axiscounter += 1

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

    def draw_map(self):
        gps_data = data[1:, int(datatypes[5, 7]) + 1:]
        gps_data = np.asarray(gps_data, dtype=float)
        context.add_object(
        staticmaps.Line([staticmaps.create_latlng(lat, lng) for lat, lng in gps_data], width=1))
        image = context.render_svg(1800, 900, 19)
        image.saveas("temp/map_tmp.svg")
        map_pixmap = QPixmap("temp/map_tmp.svg")
        map_item = QGraphicsPixmapItem(map_pixmap)
        map_scene = QGraphicsScene(self)
        map_scene.addItem(map_item)
        self.MapLoadButton.setVisible(0)
        self.mapdisplay.setVisible(1)
        self.styleSatellite.setVisible(1)
        self.styleMap.setVisible(1)
        self.mapdisplay.setScene(map_scene)

    def toggle_fullscreen(self):
        if not self.actionVollbild.isChecked():
            self.showNormal()
        else:
            self.showFullScreen()

    def openfile(self):
        self.mapdisplay.setVisible(0)
        self.MapLoadButton.setVisible(1)
        self.styleSatellite.setVisible(0)
        self.styleMap.setVisible(0)
        filepath = QFileDialog.getOpenFileName(self, self.tr("Open Data"), "/home/blacher", self.tr("*.txt *.csv"))
        try:
            datafile = open(filepath[0], 'r')
        except:
            exit()
        global data
        global plotcolor
        data = np.array(list(reader(datafile)))
        tempdata = data
        for yloop in range(len(data)):
            for xloop in range(len(data[yloop])):
                if data[yloop][xloop] == "error":
                    for typeloop in range(len(datatypes)):
                        if str(xloop-1) in datatypes[typeloop, 7:]:
                            datatypes[typeloop, 0] = 2

        errortypes = []
        for elements in range(len(datatypes)):
            if int(datatypes[elements, 0]) == 2:
                errortypes.append(datatypes[elements, 2])

        if "Coordinates" in errortypes:
            self.actionMap_View.setEnabled(0)
            self.overview_to_map.setEnabled(0)
            errortypes.remove("Coordinates")
            msgBox = QMessageBox()
            msgBox.setText("There are errors in your gps data, Map View is not available.")
            msgBox.exec()

        if not errortypes == []:
            msgBox = QMessageBox()
            msgBox.setText("There are errors in your datafile, the following categories are not available for plotting: " + str(errortypes))
            msgBox.exec()

        data = tempdata
        self.table_tableview.resizeColumnsToContents()
        axis1init = []
        # TODO fix behaviour on error
        for initloop in range(len(datatypes)):
            if int(datatypes[initloop, 0]) == 1:
                axis1init.append(initloop)
        axis2init = []
        axis3init = []
        self.plot(data, axis1init, axis2init, axis3init)
        self.populate_table(data)
        fileopen = True
        return fileopen


class WinPlotsettings(QWidget, Ui_win_plotsettings):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Plot Settings")
        for elements in range(len(datatypes)):
            if not int(datatypes[elements, 0]) == 2:
                self.dropdown_trace.addItem(datatypes[elements, 2])
        self.visible_switch.clicked.connect(self.change_visibility)
        self.dropdown_axis.setEnabled(0)
        self.plotsettings_buttons.button(self.plotsettings_buttons.Ok).clicked.connect(self.save_settings)
        self.plotsettings_buttons.button(self.plotsettings_buttons.Apply).clicked.connect(self.apply_settings)
        self.plotsettings_buttons.button(self.plotsettings_buttons.Cancel).clicked.connect(self.discard_settings)
        self.dropdown_trace.currentIndexChanged.connect(self.refresh_visibibity_button)

    def refresh_visibibity_button(self):
        self.visible_switch.setChecked(datatypes[self.dropdown_trace.currentIndex(), 0])
        if self.visible_switch.isChecked():
            self.dropdown_axis.setEnabled(1)
        else:
            self.dropdown_axis.setEnabled(0)

    def change_visibility(self):
        if self.visible_switch.isChecked():
            self.dropdown_axis.setEnabled(1)
            datatypes[self.dropdown_trace.currentIndex(), 0] = 1
        else:
            self.dropdown_axis.setEnabled(0)
            datatypes[self.dropdown_trace.currentIndex(), 0] = 0

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
