
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QTreeWidget, QTreeWidgetItem, QFileDialog
from PyQt4 import Qt

from mainwindow import Ui_MainWindow
from BoardDrillsWidget import BoardDrillsWidget
from VideoWidget import VideoWidget

from readDrillFile import *
from bilinear import *
from findPath import *
from writeGCode import *

import sys




class AutodrillMainWindow(QMainWindow, Ui_MainWindow):
	
	def __init__(self):
		QMainWindow.__init__(self)
		
		self.rawHoles = {}		# dictionary: holes sorted by diameter that come from drill file
		self.fitHoles = {}		# dictionary: holes fitted to available drill diameters

		self.drills={0.6, 0.8, 1.1, 1.3, 1.5, 1.7, 2.0}	# set of available drills
		
		self.selectedHoles=list()		# list of selected holes
		self.trafoPoints=list()			# points used for transformation (file coordinates)
		self.trafoMachinePoints=list() 	# corresponding machine coordinates
		

		# Set up the user interface from Designer.
		self.setupUi(self)
		
		self.boardDrillsWidget = BoardDrillsWidget()
		self.gridLayout.addWidget(self.boardDrillsWidget, 0, 0, 2, 1)

		self.treeWidget_holes.currentItemChanged.connect(self.treeNodeSelected)
		self.boardDrillsWidget.holeSelected.connect(self.holeSelected)
		
		self.action_loadDrillFile.triggered.connect(self.action_loadDrillFile_triggered)
		
		self.pushButton_addPoint.clicked.connect(self.addTrafoPoint)
		self.pushButton_removeAll.clicked.connect(self.removeAllTrafoPoints)
		
		
		#self.cameraWidgetObject = VideoWidget()
		#self.gridLayout.addWidget(self.cameraWidgetObject, 0, 1, 1, 1)
		
		self.updateHolesTable()
		self.boardDrillsWidget.setAllHoles(self.fitHoles)
		
		
	def action_loadDrillFile_triggered(self):
		filename = QFileDialog.getOpenFileName(self, "select drill file", "", "Drill Files (*.drl)")
		if filename:
			#print("file: " + filename)
			self.rawHoles=readDrillFile(filename)
			self.fitHoles=fitHolesToDrills(self.rawHoles, self.drills, 0.05)
			
			self.updateHolesTable()
			self.boardDrillsWidget.setAllHoles(self.fitHoles)
		
		
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
			print("Please select a hole first.")
			return
		if len(self.selectedHoles) != 1:
			print("Please select only one point.")
			return
			
		x, y, ID = self.selectedHoles[0]	# get coordinate of selected hole
		
		self.trafoPoints.append((x, y))
		# TODO get machine coordinates
		self.trafoMachinePoints.append((0, 0))
		
		self.label_trafoPoints.setText(str(len(self.trafoPoints)))
		
		if len(self.trafoPoints) == 4:
			# 4 points are enough
			self.pushButton_addPoint.setEnabled(False)
			
	def removeAllTrafoPoints(self):
		
		self.trafoPoints.clear()
		self.trafoMachinePoints.clear()
		self.label_trafoPoints.setText("0")
		self.pushButton_addHole.setEnabled(True)
		
		
	def getHole(self, holeID):
		diaList=list(self.fitHoles.keys())
		for dia in diaList:
			for hole in (self.fitHoles[dia]):
				if hole[2] == holeID:
					return hole
		
		

# assign holes to drills from given toolbox
# pick next larger drill except d_hole < d_drill + tol
def fitHolesToDrills(holes, drills, tol):
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
	
	
	
	#for dia in fitHoles:
		
	#	path=findPath(fitHoles[dia])
	#	writeGCode(dia, path)
		#print()
		#print("dia "+str(dia)+":")
		#print(fitHoles[dia])
		#print()
		
	
	#points = {(0, 0), (1, 0), (0, 1), (1, 1)}
	#points_t = {(0, 0), (1, 0.1), (-0.1, 1)}

	#path=findPath(points)

	
	#T=bilinear(points, points_t)
	
	#p = (0.5, 0.5)

	#print(T.transform(p))
	
	app = Qt.QApplication(sys.argv)
	ui = AutodrillMainWindow()
	ui.show()
	
	sys.exit(app.exec_())

