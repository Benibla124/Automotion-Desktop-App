from csv import reader
from datetime import datetime
from random import randint

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox, QGraphicsPixmapItem, QGraphicsScene
from GUI.win_main import Ui_win_main
import pyqtgraph
import os
import numpy as np
import staticmaps

windowtitle = "RC-Car Viewer"
data = []
plotcolor = np.array(["red", "blue", "yellow", "green", "magenta", "cyan", "white", "purple", "aqua", "lime", "pink", "grey"])
datatypes = np.array([[1, 3, "Orientation", "roll", "pitch", "yaw", "", 0, 1, 2, ""], [1, 3, "Acceleration", "ax", "ay", "az", "", 3, 4, 5, ""], [1, 1, "Temperature", "Temp", "", "", "", 6, "", "", ""], [1, 4, "Rotational Velocity", "rpm_rear_l", "rpm_rear_r", "rpm_front_l", "rpm_front_r", 7, 8, 9, 10], [1, 1, "Velocity", "vel_ms", "", "", "", 11, "", "", ""], [0, 2, "Coordinates", "lat", "lng", "", "", 12, 13, "", ""]])
context = staticmaps.Context()
context.set_tile_provider(staticmaps.tile_provider_OSM)


def randcolor():
    color = [randint(0, 255), randint(0, 255), randint(0, 255)]
    return color


class WinMain(QMainWindow, Ui_win_main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(windowtitle)
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
        self.action_ffnen.triggered.connect(self.openfile)
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

    def map_satellite(self):
        context.set_tile_provider(staticmaps.tile_provider_ArcGISWorldImagery)
        self.draw_map()

    def map_map(self):
        context.set_tile_provider(staticmaps.tile_provider_OSM)
        self.draw_map()

    def plot(self, plotdata):
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
                        self.graphWidget.plot([xitem.timestamp() for xitem in timedata], plotdata[:, indexnumber],
                                              pen=pen, name=data[0][indexnumber + 1 + dataoffset])
                    except:
                        pass


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


desktop_app = QApplication()
win_main = WinMain()
win_main.show()
desktop_app.exec()
