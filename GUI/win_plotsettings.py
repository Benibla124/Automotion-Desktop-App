# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'win_plotsettings.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QCheckBox, QComboBox, QDialogButtonBox, QHBoxLayout, QLabel, QSizePolicy, QSpacerItem, QVBoxLayout)

class Ui_win_plotsettings(object):
    def setupUi(self, win_plotsettings):
        if not win_plotsettings.objectName():
            win_plotsettings.setObjectName(u"win_plotsettings")
        win_plotsettings.resize(293, 143)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(win_plotsettings.sizePolicy().hasHeightForWidth())
        win_plotsettings.setSizePolicy(sizePolicy)
        win_plotsettings.setMinimumSize(QSize(293, 143))
        win_plotsettings.setMaximumSize(QSize(293, 143))
        self.verticalLayout = QVBoxLayout(win_plotsettings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.dropdown_trace = QComboBox(win_plotsettings)
        self.dropdown_trace.setObjectName(u"dropdown_trace")

        self.verticalLayout.addWidget(self.dropdown_trace)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.visible_switch = QCheckBox(win_plotsettings)
        self.visible_switch.setObjectName(u"visible_switch")
        font = QFont()
        font.setBold(False)
        self.visible_switch.setFont(font)
        self.visible_switch.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout.addWidget(self.visible_switch)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(win_plotsettings)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setBold(False)
        font1.setStrikeOut(False)
        font1.setKerning(True)
        self.label.setFont(font1)

        self.horizontalLayout_2.addWidget(self.label)

        self.dropdown_axis = QComboBox(win_plotsettings)
        self.dropdown_axis.setObjectName(u"dropdown_axis")

        self.horizontalLayout_2.addWidget(self.dropdown_axis)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.plotsettings_buttons = QDialogButtonBox(win_plotsettings)
        self.plotsettings_buttons.setObjectName(u"plotsettings_buttons")
        self.plotsettings_buttons.setStandardButtons(QDialogButtonBox.Apply|QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.plotsettings_buttons.setCenterButtons(False)

        self.verticalLayout.addWidget(self.plotsettings_buttons)


        self.retranslateUi(win_plotsettings)

        QMetaObject.connectSlotsByName(win_plotsettings)
    # setupUi

    def retranslateUi(self, win_plotsettings):
        win_plotsettings.setWindowTitle(QCoreApplication.translate("win_plotsettings", u"Form", None))
        self.visible_switch.setText(QCoreApplication.translate("win_plotsettings", u"Visible", None))
        self.label.setText(QCoreApplication.translate("win_plotsettings", u"Axis:", None))
    # retranslateUi

