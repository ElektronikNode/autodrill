#!/usr/bin/python


from PyQt4.QtGui import QMainWindow, QTreeWidget, QTreeWidgetItem, QFileDialog, QDialog, QMessageBox
from PyQt4.QtCore import QSettings, QCoreApplication, QVariant
from PyQt4 import Qt

from ui_mainwindow import Ui_MainWindow

from BoardDrillsWidget import BoardDrillsWidget
from VideoWidget import VideoWidget
from DrillCam import DrillCam
from dialogDrills import DialogDrills
from dialogCamera import DialogCamera

from readDrillFile import *
from bilinearTrafo import *
from findPath import *
from writeGCode import *
from machineInterface import *

import sys

class AutodrillMainWindow(QMainWindow, Ui_MainWindow):

	def __init__(self):
		QMainWindow.__init__(self)

		QCoreApplication.setOrganizationName("Feichtinger");
		QCoreApplication.setApplicationName("Autodrill");


		# set up the user interface from Designer.
		self.setupUi(self)

		self.boardDrillsWidget = BoardDrillsWidget()
		self.gridLayout.addWidget(self.boardDrillsWidget, 0, 0, 2, 1)
		
		self.cameraWidget = DrillCam()
		self.gridLayout.addWidget(self.cameraWidget, 0, 1, 1, 1)

		self.dialogDrills=DialogDrills(self)
		self.dialogCamera=DialogCamera(self)
		
		
		# init local variables
		self.rawHoles = {}		# dictionary: holes sorted by diameter (from drill file)
		self.fitHoles = {}		# dictionary: holes fitted to available drill diameters

		self.selectedHoles=list()		# list of selected holes
		self.trafoPoints=list()			# points used for transformation (file coordinates)
		self.trafoMachinePoints=list() 	# corresponding machine coordinates
		
		
		# load settings
		self.settings=QSettings()
		self.drills=list()
		for item in self.settings.value("drills").toList():
			self.drills.append(item.toDouble()[0])
		self.holeTol=self.settings.value("holeTol", 0.05).toDouble()[0]
		self.cameraZoom=self.settings.value("cameraZoom", 1.0).toDouble()[0]
		self.cameraOffset=(self.settings.value("cameraOffsetX", 0.0).toDouble()[0], self.settings.value("cameraOffsetY", 0.0).toDouble()[0])
		

		# connect signals and slots
		self.action_loadDrillFile.triggered.connect(self.action_loadDrillFile_triggered)
		self.action_dialogDrills.triggered.connect(self.action_dialogDrills_triggered)
		self.action_dialogCamera.triggered.connect(self.action_dialogCamera_triggered)
		self.action_writeGCode.triggered.connect(self.action_writeGCode_triggered)
		
		self.treeWidget_holes.currentItemChanged.connect(self.treeNodeSelected)
		self.boardDrillsWidget.holeSelected.connect(self.holeSelected)

		self.pushButton_addPoint.clicked.connect(self.addTrafoPoint)
		self.pushButton_removeAll.clicked.connect(self.removeAllTrafoPoints)
		
		self.verticalSlider_cameraZoom.valueChanged.connect(self.zoomChanged)
		
		
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


	def action_loadDrillFile_triggered(self):
		if not self.drills:
			QMessageBox.information(self, "No drills defined", "Please define some drills first. (Settings -> Drills)")
			return
		
		self.cameraWidget.pause()
		filename = QFileDialog.getOpenFileName(self, "select drill file", "", "Drill Files (*.drl *.drd)")
		if filename:
			#print("file: " + filename)
			self.rawHoles=readDrillFile(filename)
			self.fitHoles=fitHolesToDrills(self.rawHoles, self.drills, self.holeTol)
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
		xm, ym = getMachinePosition()
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
		self.dialogDrills.setHoleTol(self.holeTol)

		self.cameraWidget.pause()
		if self.dialogDrills.exec_() == QDialog.Accepted:

			# read back values
			self.drills=self.dialogDrills.getDrills()
			self.drills.sort()
			self.holeTol=self.dialogDrills.getHoleTol()

			# save to settings
			self.settings.setValue("drills", self.drills)
			self.settings.setValue("holeTol", self.holeTol)

			# fit holes
			self.fitHoles=fitHolesToDrills(self.rawHoles, self.drills, self.holeTol)

			# update widgets
			self.selectedHoles=list()
			self.updateHolesTable()
			self.boardDrillsWidget.setAllHoles(self.fitHoles)
		
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
			path=findPath(T.transform(self.fitHoles[dia]))
			#print(type(path))
			#print(path)
			writeGCode(dia, path)
			
			
	def zoomChanged(self):
		self.cameraZoom=float(self.verticalSlider_cameraZoom.value())/10
		self.cameraWidget.setZoom(self.cameraZoom)
		self.settings.setValue("cameraZoom", self.cameraZoom)
		


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
