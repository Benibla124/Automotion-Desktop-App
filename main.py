from csv import reader              # used for datafile opening
from datetime import datetime       # used for time axis operations

from PySide6.QtCore import QDir                                                 # PySide --> Qt Windows
from PySide6.QtGui import QPixmap                                               # PySide --> Qt Windows
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox, QGraphicsPixmapItem, QGraphicsScene, QWidget, QGraphicsView    # PySide --> Qt Windows
from GUI.win_main import Ui_win_main                                            # GUI.win_main --> Main Window
from GUI.win_plotsettings import Ui_win_plotsettings                            # GUI.win_plotsettings --> Plotsettings Window
from pyqtgraph import DateAxisItem, ViewBox, AxisItem, mkPen, PlotCurveItem     # Graph Items
from numpy import delete, array, asarray                                        # extended array operations
from staticmaps import Context, tile_provider_OSM, tile_provider_ArcGISWorldImagery, Line, create_latlng    # map rendering
from shutil import copy                                                         # File copy operations
import os                                                                       # path operations

windowtitle = "RC-Car Viewer"   # window title
plotinitialized = False         # check for first time plotting
data = []                       # init data array
plots = []                      # init plots array
a1 = []                         # init axis array
a2 = []                         # init axis array
a3 = []                         # init axis array
OG_PLOTCOLOR = ["red", "blue", "yellow", "green", "magenta", "cyan", "white", "purple", "darkorange", "lime", "pink", "grey"]    # init original plotcolors
OG_DATATYPES = [[1, 3, "Orientation", "roll", "pitch", "yaw", "", 0, 1, 2, ""],
                [1, 3, "Acceleration", "ax", "ay", "az", "", 3, 4, 5, ""],
                [0, 1, "Temperature", "Temp", "", "", "", 6, "", "", ""],
                [1, 4, "Rotational Velocity", "rpm_rear_l", "rpm_rear_r", "rpm_front_l", "rpm_front_r", 7, 8, 9, 10],
                [1, 1, "Velocity", "vel_ms", "", "", "", 11, "", "", ""],
                [0, 2, "Coordinates", "lat", "lng", "", "", 12, 13, "", ""]]
plotcolor = array(OG_PLOTCOLOR)     # save plotcolor as numpy array of OG_PLOTCOLOR
datatypes = array(OG_DATATYPES)     # save datatypes as numpy array of OG_DATATYPES
context = Context()                 # create Context (for map rendering)
context.set_tile_provider(tile_provider_OSM)    # set default tile provider (OSM)


# used for updating the different plot axes
def plots_update_views():
    global plots                                                                        # use global array
    for noofplots in range(1, len(plots) - 1):                                          # loop through the array beginning with the second item
        plots[noofplots].setGeometry(plots[0].vb.sceneBoundingRect())                   # resize
        plots[noofplots].linkedViewChanged(plots[0].vb, plots[noofplots].XAxis)         # resize


# used for finding an element in an axis
def find_element(axis, axisnumber, loopnumber, target):
    for elements in axis:               # loop through the axis
        try:
            axis.index(loopnumber)      # if the desired element exists at the current index, no error is reported
            target.append(axisnumber)   # the number of the axis gets appended to the target array
            break                       # break the loop, the item has been found
        except:
            pass                        # if the item doesn't exist at the current index, pass
    return target                       # return the target array


class WinMain(QMainWindow, Ui_win_main):        # Main-Window class
    def __init__(self):                         # init-stuff
        super().__init__()                      # more init-stuff
        self.setupUi(self)                      # set up own ui
        self.setWindowTitle(windowtitle)        # set window title
        if not os.path.exists('temp'):          # If the temp path doesn't exit, create it
            os.makedirs('temp')
        try:
            for filename in os.listdir("./temp/"):      # clear temp dir
                os.remove("./temp/" + filename)
        except:
            pass
        car_pixmap = QPixmap("GUI/Car_Render.png")  # create pixmap from the rendered image
        car_item = QGraphicsPixmapItem(car_pixmap)  # create item from the pixmap
        car_scene = QGraphicsScene(self)            # create scene
        car_scene.addItem(car_item)                 # add item to scene
        self.main_Car.setScene(car_scene)           # set created scene as scene for main_Car
        self.mapdisplay.setDragMode(QGraphicsView.ScrollHandDrag)   # enable dragging for mapdisplay
        openedfile = False                                                                      # default to false
        while not openedfile:                                                                   # loop openfile
            openedfile = self.openfile()                                                        # open the file
        self.actionBeenden.triggered.connect(self.close)                                        # connect File --> close to closing the window
        self.actionVollbild.triggered.connect(self.toggle_fullscreen)                           # connect Window --> Fullscreen to fullscreen
        self.actionOverview.triggered.connect(lambda: self.pageswitcher.setCurrentIndex(0))     # connect Window --> Overview to Overview
        self.overview_to_table.clicked.connect(lambda: self.pageswitcher.setCurrentIndex(1))    # connect Overview Table Button to table view
        self.actionTable_View.triggered.connect(lambda: self.pageswitcher.setCurrentIndex(1))   # connect Window --> Table View to table view
        self.overview_to_plot.clicked.connect(lambda: self.pageswitcher.setCurrentIndex(2))     # connect Overview Plot Button to plot view
        self.actionPlot_View.triggered.connect(lambda: self.pageswitcher.setCurrentIndex(2))    # connect Window --> Plot View to plot view
        self.overview_to_map.clicked.connect(lambda: self.pageswitcher.setCurrentIndex(3))      # connect Overview Map Button to map view
        self.actionMap_View.triggered.connect(lambda: self.pageswitcher.setCurrentIndex(3))     # connect Window --> Map View to map view
        self.MapLoadButton.clicked.connect(self.draw_map)                                       # connect "Load Map" to loading the map
        self.styleSatellite.clicked.connect(self.map_satellite)                                 # connect "Satellite Style Button" to changing the map style
        self.styleMap.clicked.connect(self.map_map)                                             # connect "OSM Style Button" to changing the map style
        self.saveImage.clicked.connect(self.save_map)                                           # connect "save image" button to saving the image
        self.PlotSettings.clicked.connect(lambda: win_plotsettings.show_window())               # connect "PlotSettings Button" to showing the plotsettings window

    def closeEvent(self, event):    # used for closing all window on main window exit
        win_plotsettings.close()    # close plotsettings

    def save_map(self):             # used for saving the map
        savepath = QFileDialog.getSaveFileName(self, "Save Location", QDir.homePath(), "*.svg")     # spawn dialog window for choosing the save path
        path = savepath[0]      # get the path only
        if not path == "":      # if the path isn't empty, check for extension
            if not path[-4:] == ".svg":                     # if the last 4 chars are not ".svg", add the extension
                path = path + ".svg"                        # add extension
            copy(os.getcwd() + "/temp/map_tmp.svg", path)   # copy the image to the location

    def map_map(self):    # used for switching to OSM mode
        context.set_tile_provider(tile_provider_OSM)    # set OSM as the tile provider
        self.draw_map()     # redraw the map

    def map_satellite(self):          # used for switching to satellite mode
        context.set_tile_provider(tile_provider_ArcGISWorldImagery)     # set ArcGISWorldImagery as the tile provider
        self.draw_map()     # redraw the map

    def plot(self, plotdata, axis1, axis2, axis3):
        global plots, plotinitialized, ax3
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
                        plotdata = delete(plotdata, int(datatypes[elements, subelements + 7]) - dataoffset, 1)
                        dataoffset += 1
                    except:
                        pass

        plotdata = asarray(plotdata, dtype=float)
        timeaxis = DateAxisItem()
        for plot_item in plots:
            plot_item.clear()
        self.graphWidget.setAxisItems({'bottom': timeaxis})

        dataoffset = 0
        plotcategories = datatypes[:, 2]
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

        if not plotinitialized:
            plots = [self.graphWidget.plotItem]
            plots.append(ViewBox())
            plots[0].showAxis('right')
            plots[0].scene().addItem(plots[1])
            plots[0].getAxis('right').linkToView(plots[1])
            plots[1].setXLink(plots[0])
            plots.append(ViewBox())
            ax3 = AxisItem('right')
            plots[0].layout.addItem(ax3, 2, 3)
            plots[0].scene().addItem(plots[2])
            ax3.linkToView(plots[2])
            plots[2].setXLink(plots[0])
            ax3.setZValue(-10000)
            plots.append(self.graphWidget.addLegend())
            plotinitialized = True

        plots[0].getAxis('right').setLabel(axis2label)
        plots[0].setLabels(left=axis1label)
        ax3.setLabel(axis3label)

        whichaxis = []

        for loopall in range(len(datatypes) - 1):
            whichaxis = find_element(axis1, 0, loopall, whichaxis)
            whichaxis = find_element(axis2, 1, loopall, whichaxis)
            whichaxis = find_element(axis3, 2, loopall, whichaxis)

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
                        pen = mkPen(color=plotcolor[indexnumber + dataoffset])
                        if whichaxis[axiscounter] == 0:
                            plots[whichaxis[axiscounter]].plot([xitem.timestamp() for xitem in timedata], plotdata[:, indexnumber], pen=pen, name=data[0][indexnumber + 1 + dataoffset])
                        else:
                            curve = PlotCurveItem([xitem.timestamp() for xitem in timedata], plotdata[:, indexnumber], pen=pen, name=data[0][indexnumber + 1 + dataoffset])
                            plots[3].addItem(curve, curve.name())
                            plots[whichaxis[axiscounter]].addItem(curve)
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
        gps_data = data[1:, int(datatypes[5, 7]):]
        gps_data = asarray(gps_data, dtype=float)
        context.add_object(Line([create_latlng(lat, lng) for lat, lng in gps_data], width=1))
        image = context.render_svg(1800, 900, 19)
        image.saveas("temp/map_tmp.svg")
        map_pixmap = QPixmap("temp/map_tmp.svg")
        map_item = QGraphicsPixmapItem(map_pixmap)
        map_scene = QGraphicsScene(self)
        map_scene.addItem(map_item)
        self.MapLoadButton.setVisible(0)
        self.mapdisplay.setVisible(1)
        self.saveImage.setVisible(1)
        self.styleSatellite.setVisible(1)
        self.styleMap.setVisible(1)
        self.mapdisplay.setScene(map_scene)

    def toggle_fullscreen(self):
        if not self.actionVollbild.isChecked():
            self.showNormal()
        else:
            self.showFullScreen()

    def openfile(self):
        global data, plotcolor, datatypes, OG_DATATYPES, OG_PLOTCOLOR
        plotcolor = array(OG_PLOTCOLOR)
        datatypes = array(OG_DATATYPES)
        self.pageswitcher.setCurrentIndex(0)
        self.mapdisplay.setVisible(0)
        self.saveImage.setVisible(0)
        self.MapLoadButton.setVisible(1)
        self.styleSatellite.setVisible(0)
        self.styleMap.setVisible(0)
        filepath = QFileDialog.getOpenFileName(self, "Open Data", QDir.homePath(), "*.txt *.csv")
        try:
            datafile = open(filepath[0], 'r')
        except:
            exit()
        data = array(list(reader(datafile)))
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
            msg_box = QMessageBox()
            msg_box.setText("There are errors in your gps data, Map View is not available.")
            msg_box.exec()

        if not errortypes == []:
            msg_box = QMessageBox()
            msg_box.setText("There are errors in your datafile, the following categories are not available for plotting: " + str(errortypes))
            msg_box.exec()

        data = tempdata
        self.table_tableview.resizeColumnsToContents()
        global a1, a2, a3
        a1 = []
        for initloop in range(len(datatypes)):
            if int(datatypes[initloop, 0]) == 1:
                a1.append(initloop)
        a2 = []
        a3 = []
        self.plot(data, a1, a2, a3)
        self.populate_table(data)
        fileopen = True
        return fileopen


class WinPlotsettings(QWidget, Ui_win_plotsettings):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Plot Settings")
        self.dropdown_axis.addItem("Axis 1")
        self.dropdown_axis.addItem("Axis 2")
        self.dropdown_axis.addItem("Axis 3")
        self.plotsettings_buttons.button(self.plotsettings_buttons.Ok).clicked.connect(self.save_settings)
        self.plotsettings_buttons.button(self.plotsettings_buttons.Apply).clicked.connect(self.apply_settings)
        self.plotsettings_buttons.button(self.plotsettings_buttons.Cancel).clicked.connect(self.discard_settings)
        self.dropdown_trace.currentIndexChanged.connect(self.refresh_visibility_button)
        self.dropdown_axis.currentIndexChanged.connect(self.axis_switch)
        self.visible_switch.clicked.connect(self.change_visibility)

    def show_window(self):
        self.dropdown_trace.clear()
        includingerrors = False
        for elements in range(len(datatypes) - 1):
            self.dropdown_trace.addItem(datatypes[elements, 2])
            if int(datatypes[elements, 0]) == 2:
                self.dropdown_trace.model().item(elements).setEnabled(False)
                includingerrors = True

        if includingerrors:
            self.dropdown_trace.setCurrentIndex(3)
        self.dropdown_axis.setEnabled(0)
        self.refresh_visibility_button()
        self.show()

    def axis_switch(self):
        global a1, a2, a3
        try:
            a1.remove(self.dropdown_trace.currentIndex())
        except:
            pass
        try:
            a2.remove(self.dropdown_trace.currentIndex())
        except:
            pass
        try:
            a3.remove(self.dropdown_trace.currentIndex())
        except:
            pass

        if self.visible_switch.isChecked():
            if self.dropdown_axis.currentIndex() == 0:
                a1.append(self.dropdown_trace.currentIndex())
            elif self.dropdown_axis.currentIndex() == 1:
                a2.append(self.dropdown_trace.currentIndex())
            elif self.dropdown_axis.currentIndex() == 2:
                a3.append(self.dropdown_trace.currentIndex())

    def refresh_visibility_button(self):
        self.visible_switch.setChecked(int(datatypes[self.dropdown_trace.currentIndex(), 0]))
        if self.visible_switch.isChecked():
            self.dropdown_axis.setEnabled(1)
        else:
            self.dropdown_axis.setEnabled(0)
        axisfound = False
        try:
            a1.index(self.dropdown_trace.currentIndex())
            self.dropdown_axis.setCurrentIndex(0)
            axisfound = True
        except:
            pass
        try:
            a2.index(self.dropdown_trace.currentIndex())
            self.dropdown_axis.setCurrentIndex(1)
            axisfound = True
        except:
            pass
        try:
            a3.index(self.dropdown_trace.currentIndex())
            self.dropdown_axis.setCurrentIndex(2)
            axisfound = True
        except:
            pass

        if not axisfound:
            self.dropdown_axis.setCurrentIndex(0)

    def change_visibility(self):
        if self.visible_switch.isChecked():
            self.dropdown_axis.setEnabled(1)
            datatypes[self.dropdown_trace.currentIndex(), 0] = 1
        else:
            self.dropdown_axis.setEnabled(0)
            datatypes[self.dropdown_trace.currentIndex(), 0] = 0
        self.axis_switch()

    def apply_settings(self):
        win_main.plot(data, a1, a2, a3)

    def save_settings(self):
        win_main.plot(data, a1, a2, a3)
        self.close()

    def discard_settings(self):
        self.close()


desktop_app = QApplication()
win_main = WinMain()
win_plotsettings = WinPlotsettings()
win_main.show()
desktop_app.exec()
