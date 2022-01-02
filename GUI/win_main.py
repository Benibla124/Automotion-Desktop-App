# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'win_main.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QHeaderView, QLabel,
                               QMainWindow, QMenu, QMenuBar, QSizePolicy,
                               QStackedWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
                               QWidget, QAbstractItemView)

class Ui_win_main(object):
    def setupUi(self, win_main):
        if not win_main.objectName():
            win_main.setObjectName(u"win_main")
        win_main.resize(1200, 800)
        self.actionBeenden = QAction(win_main)
        self.actionBeenden.setObjectName(u"actionBeenden")
        self.action_ffnen = QAction(win_main)
        self.action_ffnen.setObjectName(u"action_ffnen")
        self.actionVollbild = QAction(win_main)
        self.actionVollbild.setObjectName(u"actionVollbild")
        self.actionVollbild.setCheckable(True)
        self.actionVollbild.setChecked(False)
        self.actionOverview = QAction(win_main)
        self.actionOverview.setObjectName(u"actionOverview")
        self.actionTable_View = QAction(win_main)
        self.actionTable_View.setObjectName(u"actionTable_View")
        self.centralwidget = QWidget(win_main)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pageswitcher = QStackedWidget(self.centralwidget)
        self.pageswitcher.setObjectName(u"pageswitcher")
        self.view_overview = QWidget()
        self.view_overview.setObjectName(u"view_overview")
        self.pageswitcher.addWidget(self.view_overview)
        self.view_table = QWidget()
        self.view_table.setObjectName(u"view_table")
        self.verticalLayout_3 = QVBoxLayout(self.view_table)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.lab_tableview = QLabel(self.view_table)
        self.lab_tableview.setObjectName(u"lab_tableview")
        font = QFont()
        font.setPointSize(18)
        self.lab_tableview.setFont(font)
        self.lab_tableview.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.lab_tableview)

        self.table_tableview = QTableWidget(self.view_table)
        self.table_tableview.setObjectName(u"table_tableview")
        self.table_tableview.setEnabled(True)
        self.table_tableview.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_tableview.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout_3.addWidget(self.table_tableview)

        self.pageswitcher.addWidget(self.view_table)

        self.verticalLayout_2.addWidget(self.pageswitcher)

        win_main.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(win_main)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 20))
        self.menuDatei = QMenu(self.menubar)
        self.menuDatei.setObjectName(u"menuDatei")
        self.menuFenster = QMenu(self.menubar)
        self.menuFenster.setObjectName(u"menuFenster")
        win_main.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuDatei.menuAction())
        self.menubar.addAction(self.menuFenster.menuAction())
        self.menuDatei.addAction(self.action_ffnen)
        self.menuDatei.addSeparator()
        self.menuDatei.addAction(self.actionBeenden)
        self.menuFenster.addAction(self.actionVollbild)
        self.menuFenster.addSeparator()
        self.menuFenster.addAction(self.actionOverview)
        self.menuFenster.addAction(self.actionTable_View)

        self.retranslateUi(win_main)

        self.pageswitcher.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(win_main)
    # setupUi

    def retranslateUi(self, win_main):
        win_main.setWindowTitle(QCoreApplication.translate("win_main", u"MainWindow", None))
        self.actionBeenden.setText(QCoreApplication.translate("win_main", u"Beenden", None))
        self.action_ffnen.setText(QCoreApplication.translate("win_main", u"\u00d6ffnen", None))
        self.actionVollbild.setText(QCoreApplication.translate("win_main", u"Vollbild", None))
        self.actionOverview.setText(QCoreApplication.translate("win_main", u"Overview", None))
        self.actionTable_View.setText(QCoreApplication.translate("win_main", u"Table View", None))
        self.lab_tableview.setText(QCoreApplication.translate("win_main", u"Table View", None))
        self.menuDatei.setTitle(QCoreApplication.translate("win_main", u"Datei", None))
        self.menuFenster.setTitle(QCoreApplication.translate("win_main", u"Fenster", None))
    # retranslateUi

