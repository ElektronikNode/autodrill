# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'autodrill/ui/dialogDrillParameter.ui'
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

class Ui_DialogDrillParameter(object):
    def setupUi(self, DialogDrillParameter):
        DialogDrillParameter.setObjectName(_fromUtf8("DialogDrillParameter"))
        DialogDrillParameter.resize(571, 305)
        self.verticalLayout_2 = QtGui.QVBoxLayout(DialogDrillParameter)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(DialogDrillParameter)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineEdit_feedrate = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_feedrate.setObjectName(_fromUtf8("lineEdit_feedrate"))
        self.gridLayout.addWidget(self.lineEdit_feedrate, 0, 0, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(DialogDrillParameter)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lineEdit_depth = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_depth.setObjectName(_fromUtf8("lineEdit_depth"))
        self.gridLayout_2.addWidget(self.lineEdit_depth, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox_3 = QtGui.QGroupBox(DialogDrillParameter)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.lineEdit_spacing = QtGui.QLineEdit(self.groupBox_3)
        self.lineEdit_spacing.setObjectName(_fromUtf8("lineEdit_spacing"))
        self.gridLayout_3.addWidget(self.lineEdit_spacing, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox_3)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_3.addWidget(self.label_3, 0, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.label_sketch = QtGui.QLabel(DialogDrillParameter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_sketch.sizePolicy().hasHeightForWidth())
        self.label_sketch.setSizePolicy(sizePolicy)
        self.label_sketch.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sketch.setObjectName(_fromUtf8("label_sketch"))
        self.horizontalLayout_2.addWidget(self.label_sketch)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        spacerItem3 = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.pushButton_cancel = QtGui.QPushButton(DialogDrillParameter)
        self.pushButton_cancel.setObjectName(_fromUtf8("pushButton_cancel"))
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.pushButton_OK = QtGui.QPushButton(DialogDrillParameter)
        self.pushButton_OK.setDefault(True)
        self.pushButton_OK.setObjectName(_fromUtf8("pushButton_OK"))
        self.horizontalLayout.addWidget(self.pushButton_OK)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(DialogDrillParameter)
        QtCore.QMetaObject.connectSlotsByName(DialogDrillParameter)

    def retranslateUi(self, DialogDrillParameter):
        DialogDrillParameter.setWindowTitle(_translate("DialogDrillParameter", "Drill Parameters", None))
        self.groupBox.setTitle(_translate("DialogDrillParameter", "Feedrate", None))
        self.label.setText(_translate("DialogDrillParameter", "mm/s", None))
        self.groupBox_2.setTitle(_translate("DialogDrillParameter", "Depth (d)", None))
        self.label_2.setText(_translate("DialogDrillParameter", "mm", None))
        self.groupBox_3.setTitle(_translate("DialogDrillParameter", "Spacing (s)", None))
        self.label_3.setText(_translate("DialogDrillParameter", "mm", None))
        self.label_sketch.setText(_translate("DialogDrillParameter", "sketch", None))
        self.pushButton_cancel.setText(_translate("DialogDrillParameter", "Cancel", None))
        self.pushButton_OK.setText(_translate("DialogDrillParameter", "OK", None))

