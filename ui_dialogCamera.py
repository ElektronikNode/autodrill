# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogCamera.ui'
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

class Ui_DialogCamera(object):
    def setupUi(self, DialogCamera):
        DialogCamera.setObjectName(_fromUtf8("DialogCamera"))
        DialogCamera.resize(406, 335)
        self.verticalLayout = QtGui.QVBoxLayout(DialogCamera)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_2 = QtGui.QGroupBox(DialogCamera)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.comboBox_device = QtGui.QComboBox(self.groupBox_2)
        self.comboBox_device.setObjectName(_fromUtf8("comboBox_device"))
        self.gridLayout_2.addWidget(self.comboBox_device, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(268, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtGui.QGroupBox(DialogCamera)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 4)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_offsetX = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_offsetX.setObjectName(_fromUtf8("lineEdit_offsetX"))
        self.gridLayout.addWidget(self.lineEdit_offsetX, 1, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(151, 38, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 2, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEdit_offsetY = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_offsetY.setObjectName(_fromUtf8("lineEdit_offsetY"))
        self.gridLayout.addWidget(self.lineEdit_offsetY, 2, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 2, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 4)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem2 = QtGui.QSpacerItem(20, 28, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.pushButton_cancel = QtGui.QPushButton(DialogCamera)
        self.pushButton_cancel.setObjectName(_fromUtf8("pushButton_cancel"))
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.pushButton_OK = QtGui.QPushButton(DialogCamera)
        self.pushButton_OK.setDefault(True)
        self.pushButton_OK.setObjectName(_fromUtf8("pushButton_OK"))
        self.horizontalLayout.addWidget(self.pushButton_OK)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(DialogCamera)
        QtCore.QMetaObject.connectSlotsByName(DialogCamera)

    def retranslateUi(self, DialogCamera):
        DialogCamera.setWindowTitle(_translate("DialogCamera", "Dialog", None))
        self.groupBox_2.setTitle(_translate("DialogCamera", "Device", None))
        self.groupBox.setTitle(_translate("DialogCamera", "Offset", None))
        self.label.setText(_translate("DialogCamera", "x/y distance of camera with reference to spindle axis", None))
        self.label_2.setText(_translate("DialogCamera", "x", None))
        self.label_5.setText(_translate("DialogCamera", "mm", None))
        self.label_3.setText(_translate("DialogCamera", "y", None))
        self.label_6.setText(_translate("DialogCamera", "mm", None))
        self.label_4.setText(_translate("DialogCamera", "Hint: Set a reference point in LinuxCNC and drill a test hole. Then move the camera to the hole and take the negative of the current position. ", None))
        self.pushButton_cancel.setText(_translate("DialogCamera", "Cancel", None))
        self.pushButton_OK.setText(_translate("DialogCamera", "OK", None))

