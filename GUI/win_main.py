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
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)

class Ui_win_main(object):
    def setupUi(self, win_main):
        if not win_main.objectName():
            win_main.setObjectName(u"win_main")
        win_main.resize(1273, 800)
        self.actionBeenden = QAction(win_main)
        self.actionBeenden.setObjectName(u"actionBeenden")
        self.action_ffnen = QAction(win_main)
        self.action_ffnen.setObjectName(u"action_ffnen")
        self.actionVollbild = QAction(win_main)
        self.actionVollbild.setObjectName(u"actionVollbild")
        self.actionVollbild.setCheckable(True)
        self.centralwidget = QWidget(win_main)
        self.centralwidget.setObjectName(u"centralwidget")
        win_main.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(win_main)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1273, 20))
        self.menuDatei = QMenu(self.menubar)
        self.menuDatei.setObjectName(u"menuDatei")
        self.menuFenster = QMenu(self.menubar)
        self.menuFenster.setObjectName(u"menuFenster")
        win_main.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(win_main)
        self.statusbar.setObjectName(u"statusbar")
        win_main.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuDatei.menuAction())
        self.menubar.addAction(self.menuFenster.menuAction())
        self.menuDatei.addAction(self.action_ffnen)
        self.menuDatei.addSeparator()
        self.menuDatei.addAction(self.actionBeenden)
        self.menuFenster.addAction(self.actionVollbild)

        self.retranslateUi(win_main)

        QMetaObject.connectSlotsByName(win_main)
    # setupUi

    def retranslateUi(self, win_main):
        win_main.setWindowTitle(QCoreApplication.translate("win_main", u"MainWindow", None))
        self.actionBeenden.setText(QCoreApplication.translate("win_main", u"Beenden", None))
        self.action_ffnen.setText(QCoreApplication.translate("win_main", u"\u00d6ffnen", None))
        self.actionVollbild.setText(QCoreApplication.translate("win_main", u"Vollbild", None))
        self.menuDatei.setTitle(QCoreApplication.translate("win_main", u"Datei", None))
        self.menuFenster.setTitle(QCoreApplication.translate("win_main", u"Fenster", None))
    # retranslateUi

