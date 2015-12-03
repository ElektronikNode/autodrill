# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Thu Dec  3 09:22:19 2015
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(942, 653)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.paintWidget = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.paintWidget.sizePolicy().hasHeightForWidth())
        self.paintWidget.setSizePolicy(sizePolicy)
        self.paintWidget.setObjectName(_fromUtf8("paintWidget"))
        self.gridLayout.addWidget(self.paintWidget, 0, 0, 2, 1)
        self.cameraWidget = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cameraWidget.sizePolicy().hasHeightForWidth())
        self.cameraWidget.setSizePolicy(sizePolicy)
        self.cameraWidget.setObjectName(_fromUtf8("cameraWidget"))
        self.gridLayout.addWidget(self.cameraWidget, 0, 1, 1, 2)
        self.treeWidget_holes = QtGui.QTreeWidget(self.centralwidget)
        self.treeWidget_holes.setObjectName(_fromUtf8("treeWidget_holes"))
        self.treeWidget_holes.headerItem().setText(0, _fromUtf8("1"))
        self.gridLayout.addWidget(self.treeWidget_holes, 1, 1, 1, 1)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pushButton_startNextTrafo = QtGui.QPushButton(self.groupBox)
        self.pushButton_startNextTrafo.setObjectName(_fromUtf8("pushButton_startNextTrafo"))
        self.verticalLayout.addWidget(self.pushButton_startNextTrafo)
        self.pushButton_finishTrafo = QtGui.QPushButton(self.groupBox)
        self.pushButton_finishTrafo.setObjectName(_fromUtf8("pushButton_finishTrafo"))
        self.verticalLayout.addWidget(self.pushButton_finishTrafo)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.label_trafoPoints = QtGui.QLabel(self.groupBox)
        self.label_trafoPoints.setObjectName(_fromUtf8("label_trafoPoints"))
        self.horizontalLayout.addWidget(self.label_trafoPoints)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtGui.QSpacerItem(20, 138, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addWidget(self.groupBox, 1, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 942, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuSettings = QtGui.QMenu(self.menubar)
        self.menuSettings.setObjectName(_fromUtf8("menuSettings"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action_loadDrillFile = QtGui.QAction(MainWindow)
        self.action_loadDrillFile.setObjectName(_fromUtf8("action_loadDrillFile"))
        self.action_drillsDialog = QtGui.QAction(MainWindow)
        self.action_drillsDialog.setObjectName(_fromUtf8("action_drillsDialog"))
        self.action_cameraOffset = QtGui.QAction(MainWindow)
        self.action_cameraOffset.setObjectName(_fromUtf8("action_cameraOffset"))
        self.menuFile.addAction(self.action_loadDrillFile)
        self.menuSettings.addAction(self.action_drillsDialog)
        self.menuSettings.addAction(self.action_cameraOffset)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "auto drill", None))
        self.groupBox.setTitle(_translate("MainWindow", "Transformation", None))
        self.pushButton_startNextTrafo.setText(_translate("MainWindow", "Start", None))
        self.pushButton_finishTrafo.setText(_translate("MainWindow", "Finish", None))
        self.label_2.setText(_translate("MainWindow", "Please select 2..4 points.", None))
        self.label.setText(_translate("MainWindow", "Points used:", None))
        self.label_trafoPoints.setText(_translate("MainWindow", "0", None))
        self.menuFile.setTitle(_translate("MainWindow", "&File", None))
        self.menuSettings.setTitle(_translate("MainWindow", "S&ettings", None))
        self.action_loadDrillFile.setText(_translate("MainWindow", "&Load Drill File", None))
        self.action_drillsDialog.setText(_translate("MainWindow", "&Drills", None))
        self.action_cameraOffset.setText(_translate("MainWindow", "Camera Offset", None))

