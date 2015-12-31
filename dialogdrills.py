# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogdrills.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DialogDrills(object):
    def setupUi(self, DialogDrills):
        DialogDrills.setObjectName(_fromUtf8("DialogDrills"))
        DialogDrills.resize(431, 597)
        self.verticalLayout_2 = QtGui.QVBoxLayout(DialogDrills)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(DialogDrills)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tableWidget_drills = QtGui.QTableWidget(self.groupBox)
        self.tableWidget_drills.setObjectName(_fromUtf8("tableWidget_drills"))
        self.tableWidget_drills.setColumnCount(1)
        self.tableWidget_drills.setRowCount(1)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_drills.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_drills.setHorizontalHeaderItem(0, item)
        self.tableWidget_drills.verticalHeader().setVisible(True)
        self.gridLayout.addWidget(self.tableWidget_drills, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.groupBox_2 = QtGui.QGroupBox(DialogDrills)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.lineEdit_holeTol = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_holeTol.setObjectName(_fromUtf8("lineEdit_holeTol"))
        self.horizontalLayout_3.addWidget(self.lineEdit_holeTol)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.pushButton_cancel = QtGui.QPushButton(DialogDrills)
        self.pushButton_cancel.setObjectName(_fromUtf8("pushButton_cancel"))
        self.horizontalLayout_2.addWidget(self.pushButton_cancel)
        self.pushButton_OK = QtGui.QPushButton(DialogDrills)
        self.pushButton_OK.setDefault(True)
        self.pushButton_OK.setObjectName(_fromUtf8("pushButton_OK"))
        self.horizontalLayout_2.addWidget(self.pushButton_OK)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(DialogDrills)
        QtCore.QMetaObject.connectSlotsByName(DialogDrills)

    def retranslateUi(self, DialogDrills):
        DialogDrills.setWindowTitle(_translate("DialogDrills", "Dialog", None))
        self.groupBox.setTitle(_translate("DialogDrills", "Drills", None))
        self.tableWidget_drills.setSortingEnabled(True)
        item = self.tableWidget_drills.verticalHeaderItem(0)
        item.setText(_translate("DialogDrills", "1", None))
        item = self.tableWidget_drills.horizontalHeaderItem(0)
        item.setText(_translate("DialogDrills", "diameter", None))
        self.groupBox_2.setTitle(_translate("DialogDrills", "Lower Hole Tolerance", None))
        self.label.setText(_translate("DialogDrills", "Normally Autodrill will pick the next larger drill bit for a given hole diameter. But for holes that are slightly over the size of the drill bit, Autodrill can pick the undersized drill bit if the difference is smaller than the lower hole tolerance.", None))
        self.pushButton_cancel.setText(_translate("DialogDrills", "Cancel", None))
        self.pushButton_OK.setText(_translate("DialogDrills", "OK", None))

