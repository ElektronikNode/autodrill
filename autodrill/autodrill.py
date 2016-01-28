#!/usr/bin/python

'''
autodrill is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

autodrill is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with autodrill. If not, see < http://www.gnu.org/licenses/ >.

(C) 2014- by Friedrich Feichtinger, <fritz_feichtinger@aon.at>
(C) 2014- by Thomas Pointhuber, <thomas.pointhuber@gmx.at>
'''

from PyQt4.QtGui import QMainWindow, QTreeWidget, QTreeWidgetItem, QFileDialog, QDialog, QMessageBox, QKeyEvent
from PyQt4.QtCore import QSettings, QCoreApplication, QVariant, QFileInfo, QTimer
from PyQt4 import Qt, QtCore

from ui.ui_mainwindow import Ui_MainWindow

from BoardDrillsWidget import BoardDrillsWidget
from VideoWidget import VideoWidget
from DrillCam import DrillCam
from ui.dialogDrills import DialogDrills
from ui.dialogDrillParameter import DialogDrillParameter
from ui.dialogCamera import DialogCamera

from readDrillFile import *
from bilinearTrafo import *
from findPath import *
from writeGCode import *
from machineInterface import *

import sys


# jog speeds (mm/s ?)
SLOWJOG=1
FASTJOG=1000


class AutodrillMainWindow(QMainWindow, Ui_MainWindow):

	def __init__(self):
		QMainWindow.__init__(self)

		# for QSettings
		QCoreApplication.setOrganizationName("Feichtinger");
		QCoreApplication.setApplicationName("Autodrill");
		
		self.updateTimer=QTimer()
		self.updateTimer.start(50);


		# set up the user interface from Designer.
		self.setupUi(self)

		self.boardDrillsWidget = BoardDrillsWidget()
		self.gridLayout.addWidget(self.boardDrillsWidget, 0, 0, 2, 1)

		self.cameraWidget = DrillCam()
		self.gridLayout.addWidget(self.cameraWidget, 0, 1, 1, 1)

		self.dialogDrills=DialogDrills(self)
		self.dialogDrillParameter=DialogDrillParameter(self)
		self.dialogCamera=DialogCamera(self)


		# init local variables
		self.rawHoles = {}		# dictionary: holes sorted by diameter (from drill file)
		self.fitHoles = {}		# dictionary: holes fitted to available drill diameters

		self.selectedHoles=list()		# list of selected holes
		self.trafoPoints=list()			# points used for transformation (file coordinates)
		self.trafoMachinePoints=list() 	# corresponding machine coordinates


		# load settings (and set default values)
		self.settings=QSettings()
		self.drills=list()

		for item in self.settings.value("drills", "").toList():
			self.drills.append(item.toDouble()[0])
		self.diaTol=self.settings.value("diaTol", 0.05).toDouble()[0]
		self.cameraZoom=self.settings.value("cameraZoom", 1.0).toDouble()[0]
		self.cameraOffset=(self.settings.value("cameraOffsetX", 0.0).toDouble()[0], self.settings.value("cameraOffsetY", 0.0).toDouble()[0])
		self.feedrate=self.settings.value("feedrate", 10.0).toDouble()[0]
		self.drillDepth=self.settings.value("drillDepth", 2.0).toDouble()[0]
		self.drillSpacing=self.settings.value("drillSpacing", 5.0).toDouble()[0]
		self.toolChangePos=(self.settings.value("toolChangePosX", 0.0).toDouble()[0], self.settings.value("toolChangePosY", 0.0).toDouble()[0], self.settings.value("toolChangePosZ", 20.0).toDouble()[0])
		self.currentPath=self.settings.value("currentPath", "").toString()



		# connect signals and slots
		self.action_loadDrillFile.triggered.connect(self.action_loadDrillFile_triggered)
		self.action_dialogDrills.triggered.connect(self.action_dialogDrills_triggered)
		self.action_dialogDrillParameter.triggered.connect(self.action_dialogDrillParameter_triggered)
		self.action_dialogCamera.triggered.connect(self.action_dialogCamera_triggered)
		self.action_writeGCode.triggered.connect(self.action_writeGCode_triggered)

		self.treeWidget_holes.currentItemChanged.connect(self.treeNodeSelected)
		self.boardDrillsWidget.holeSelected.connect(self.holeSelected)

		self.pushButton_addPoint.clicked.connect(self.addTrafoPoint)
		self.pushButton_removeAll.clicked.connect(self.removeAllTrafoPoints)

		self.verticalSlider_cameraZoom.valueChanged.connect(self.zoomChanged)
		
		self.updateTimer.timeout.connect(self.updatePositionLabel)

		# init widgets
		self.updateHolesTable()
		self.cameraWidget.setZoom(self.cameraZoom)
		self.verticalSlider_cameraZoom.setValue(self.cameraZoom*10)


		# check for LinuxCNC
		if not LinuxCNCInstalled():
			QMessageBox.information(self, "LinuxCNC", "Please install LinuxCNC")
			return

		if not LinuxCNCRunning():
			QMessageBox.information(self, "LinuxCNC", "Please start LinuxCNC now.")

		# for jogging
		self.grabKeyboard()
		self.jogSpeed=SLOWJOG
		self.jogAxes=[0, 0, 0]
		
		
		

	def action_loadDrillFile_triggered(self):
		if not self.drills:
			QMessageBox.information(self, "No drills defined", "Please define some drills first. (Settings -> Drills)")
			return

		self.cameraWidget.pause()
		filename = str(QFileDialog.getOpenFileName(self, "select drill file", self.currentPath, "Drill Files (*.drl *.drd)").toUtf8())
		if filename:
			# load file
			print(filename)
			self.rawHoles=readDrillFile(filename)
			if not self.rawHoles:
				QMessageBox.critical(self, "File error", "Could not load file.")
				self.cameraWidget.resume()
				return


			self.currentPath=QFileInfo(filename).absolutePath()
			self.settings.setValue("currentPath", self.currentPath)

			self.fitHoles=fitHolesToDrills(self.rawHoles, self.drills, self.diaTol)
			self.updateHolesTable()
			self.boardDrillsWidget.setAllHoles(self.fitHoles)
			self.removeAllTrafoPoints()

		self.cameraWidget.resume()


	def updateHolesTable(self):
		self.treeWidget_holes.clear()
		self.treeWidget_holes.setColumnCount(3)
		self.treeWidget_holes.setColumnWidth(0, 50)
		self.treeWidget_holes.setColumnWidth(1, 50)
		self.treeWidget_holes.setColumnWidth(2, 70)
		self.treeWidget_holes.setColumnWidth(3, 70)
		self.treeWidget_holes.setHeaderLabels(["dia", "#", "X", "Y"])

		diaList=list(self.fitHoles.keys())
		diaList.sort()

		for dia in diaList:
			drillItem = QTreeWidgetItem()
			drillItem.setText(0, str(dia))
			drillItem.setText(1, str(len(self.fitHoles[dia])))
			self.treeWidget_holes.addTopLevelItem(drillItem)

			for hole in (self.fitHoles[dia]):
				x, y, ID = hole
				holeItem = QTreeWidgetItem(ID+1000)	# use ID of hole as type
				holeItem.setText(2, "{:3.1f}".format(x))
				holeItem.setText(3, "{:3.1f}".format(y))
				drillItem.addChild(holeItem)

				if hole in self.selectedHoles:
					self.treeWidget_holes.setCurrentItem(holeItem)
					#self.treeWidget_holes.expandItem(drillItem)
					#self.treeWidget_holes.scrollToItem(holeItem)

		if not self.selectedHoles:
			self.treeWidget_holes.setCurrentItem(None)


	def treeNodeSelected(self):
		item=self.treeWidget_holes.currentItem()

		if item:
			self.selectedHoles=list()
			if item.childCount() > 0:
				for i in range(item.childCount()) :
					self.selectedHoles.append(self.getHole(item.child(i).type()-1000))
			else:
				self.selectedHoles.append(self.getHole(item.type()-1000))

		self.boardDrillsWidget.setSelectedHoles(self.selectedHoles)


	def holeSelected(self, hole):
		self.selectedHoles=[hole]
		self.boardDrillsWidget.setSelectedHoles(self.selectedHoles)
		self.updateHolesTable()
		#print(holeID)


	def addTrafoPoint(self):
		#print("Move CNC over hole and select it!")
		if len(self.selectedHoles) == 0:
			QMessageBox.information("Transformation", "Please select a hole first.")
			return
		if len(self.selectedHoles) != 1:
			QMessageBox.warning("Transformation", "Please select only one point.")
			return

		# get machine coordinates and add camera offset
		xm, ym, zm = getMachinePosition()
		xo, yo = self.cameraOffset
		self.trafoMachinePoints.append((xm+xo, ym+yo))

		# get coordinate of selected hole
		x, y, ID = self.selectedHoles[0]
		self.trafoPoints.append((x, y))

		self.label_trafoPoints.setText(str(len(self.trafoPoints)))

		if len(self.trafoPoints) == 4:
			# 4 points are enough
			self.pushButton_addPoint.setEnabled(False)


	def removeAllTrafoPoints(self):
		self.trafoPoints=list()
		self.trafoMachinePoints=list()
		self.label_trafoPoints.setText("0")
		self.pushButton_addPoint.setEnabled(True)


	def getHole(self, holeID):
		diaList=list(self.fitHoles.keys())
		for dia in diaList:
			for hole in (self.fitHoles[dia]):
				if hole[2] == holeID:
					return hole

	def action_dialogDrills_triggered(self):
		# init dialog
		self.dialogDrills.setDrills(self.drills)
		self.dialogDrills.setHoleTol(self.diaTol)

		self.cameraWidget.pause()
		if self.dialogDrills.exec_() == QDialog.Accepted:

			# read back values
			self.drills=self.dialogDrills.getDrills()
			self.drills.sort()
			self.diaTol=self.dialogDrills.getHoleTol()

			# save to settings
			self.settings.setValue("drills", self.drills)
			self.settings.setValue("diaTol", self.diaTol)

			# fit holes
			self.fitHoles=fitHolesToDrills(self.rawHoles, self.drills, self.diaTol)

			# update widgets
			self.selectedHoles=list()
			self.updateHolesTable()
			self.boardDrillsWidget.setAllHoles(self.fitHoles)

		self.cameraWidget.resume()


	def action_dialogDrillParameter_triggered(self):
		self.dialogDrillParameter.setFeedrate(self.feedrate)
		self.dialogDrillParameter.setDepth(self.drillDepth)
		self.dialogDrillParameter.setSpacing(self.drillSpacing)
		self.dialogDrillParameter.setToolChangePos(self.toolChangePos)

		self.cameraWidget.pause()
		if self.dialogDrillParameter.exec_() == QDialog.Accepted:
			self.feedrate=self.dialogDrillParameter.getFeedrate()
			self.drillDepth=self.dialogDrillParameter.getDepth()
			self.drillSpacing=self.dialogDrillParameter.getSpacing()
			self.toolChangePos=self.dialogDrillParameter.getToolChangePos()

			self.settings.setValue("feedrate", self.feedrate)
			self.settings.setValue("drillDepth", self.drillDepth)
			self.settings.setValue("drillSpacing", self.drillSpacing)
			x, y, z=self.toolChangePos
			self.settings.setValue("toolChangePosX", x)
			self.settings.setValue("toolChangePosY", y)
			self.settings.setValue("toolChangePosZ", z)

		self.cameraWidget.resume()


	def action_dialogCamera_triggered(self):
		self.dialogCamera.setOffset(self.cameraOffset)

		self.cameraWidget.pause()
		if self.dialogCamera.exec_() == QDialog.Accepted:
			self.cameraOffset=self.dialogCamera.getOffset()
			x, y=self.cameraOffset
			self.settings.setValue("cameraOffsetX", x)
			self.settings.setValue("cameraOffsetY", y)

		self.cameraWidget.resume()

	def action_writeGCode_triggered(self):

		if not len(self.trafoPoints) in {3, 4}:
			QMessageBox.warning(self, "not enough points", "Please select at least 3 transformation points.")
			return

		T=bilinearTrafo(self.trafoPoints, self.trafoMachinePoints)
		for dia in self.fitHoles:
			drillPath=findPath(T.transform(self.fitHoles[dia]))
			#print(type(path))
			#print(path)
			writeGCode(dia, drillPath, self.currentPath, self.feedrate, self.drillDepth, self.drillSpacing, self.toolChangePos)

		QMessageBox.information(self, "G-Code", "Finished!")


	def zoomChanged(self):
		self.cameraZoom=float(self.verticalSlider_cameraZoom.value())/10
		self.cameraWidget.setZoom(self.cameraZoom)
		self.settings.setValue("cameraZoom", self.cameraZoom)
		
		
	def keyPressEvent(self, e):
		if(e.key()==QtCore.Qt.Key_Escape):
			print("EStop")
			# TODO
			
		elif e.key()==QtCore.Qt.Key_Shift:
			self.jogSpeed=FASTJOG	# switch to fast jog mode
			
		elif e.key()==QtCore.Qt.Key_Up:
			self.jogAxes[1]=1
		elif e.key()==QtCore.Qt.Key_Down:
			self.jogAxes[1]=-1
		elif e.key()==QtCore.Qt.Key_Left:
			self.jogAxes[0]=-1
		elif e.key()==QtCore.Qt.Key_Right:
			self.jogAxes[0]=1
		elif e.key()==QtCore.Qt.Key_PageUp:
			self.jogAxes[2]=1
		elif e.key()==QtCore.Qt.Key_PageDown:
			self.jogAxes[2]=-1
			
		self.updateJog()


	def keyReleaseEvent(self, e):
		if e.key()==QtCore.Qt.Key_Shift:
			self.jogSpeed=SLOWJOG	# switch to slow jog mode
			
		elif e.key()==QtCore.Qt.Key_Up or e.key()==QtCore.Qt.Key_Down:
			self.jogAxes[1]=0
		elif e.key()==QtCore.Qt.Key_Left or e.key()==QtCore.Qt.Key_Right:
			self.jogAxes[0]=0
		elif e.key()==QtCore.Qt.Key_PageUp or e.key()==QtCore.Qt.Key_PageDown:
			self.jogAxes[2]=0
			
		self.updateJog()
			
			
	def updateJog(self):
		for i in range(3):
			if self.jogAxes[i]>0:
				jogAxis(i, self.jogSpeed)
			elif self.jogAxes[i]<0:
				jogAxis(i, -self.jogSpeed)
			else:
				stopAxis(i)
				
				
	def updatePositionLabel(self):
		x, y, z = getMachinePosition()
		self.statusBar().showMessage("X: {:.2f}  Y: {:.2f}  Z: {:.2f}".format(x, y, z))


# assign holes to drills from given toolbox
# pick next larger drill except d_hole - tol < d_drill
def fitHolesToDrills(holes, drills, tol):

	if not drills:
		return {}

	diaList=list(holes.keys())		# list of hole diameters
	drillDiaList=list(drills)		# list of drill diameters

	diaList.sort()
	drillDiaList.sort()

	fitHoles={}							# dict of holes with assigned diameters
	drillNo=0							# index of current drill
	drillDia=drillDiaList[0]			# current drill diameter

	for dia in diaList:

		while dia>drillDia+tol:
			# we need a bigger drill
			if drillNo==len(drillDiaList)-1:
				# there is no bigger drill
				break

			drillNo=drillNo+1
			drillDia=drillDiaList[drillNo]

		# drill fits to hole

		# create hole set if not existing
		if drillDia not in fitHoles:
			fitHoles[drillDia]=set()

		# assign holes
		fitHoles[drillDia] |= (holes[dia])

	return fitHoles


if __name__ == '__main__':

	app = Qt.QApplication(sys.argv)
	ui = AutodrillMainWindow()
	ui.show()

	sys.exit(app.exec_())
