
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
		
		self.rawHoles = {}
		self.fitHoles = {}

		self.drills={0.6, 0.8, 1.1, 1.3, 1.5, 1.7, 2.0}
		
		self.currentTrafoHole=0

		# Set up the user interface from Designer.
		self.setupUi(self)

		self.treeWidget_holes.currentItemChanged.connect(self.treeNodeSelected)
		self.action_loadDrillFile.triggered.connect(self.action_loadDrillFile_triggered)
		self.pushButton_startNextTrafo.clicked.connect(self.startNextTrafo)
		self.pushButton_finishTrafo.clicked.connect(self.finishTrafo)
		
		#self.cameraWidgetObject = VideoWidget()
		#self.gridLayout.addWidget(self.cameraWidgetObject, 0, 1, 1, 1)

		self.boardDrillsWidget = BoardDrillsWidget()
		self.gridLayout.addWidget(self.boardDrillsWidget, 0, 0, 2, 1)
		
		self.updateHoles()
		
		
	def action_loadDrillFile_triggered(self):
		filename = QFileDialog.getOpenFileName(self, "select drill file", "", "Drill Files (*.drl)")
		if filename:
			#print("file: " + filename)
			self.rawHoles=readDrillFile(filename)
			self.fitHoles=fitHolesToDrills(self.rawHoles, self.drills, 0.05)
			self.updateHoles()
		
		
	def updateHoles(self):
		
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
				
		self.boardDrillsWidget.setAllHoles(self.fitHoles)
		
				
	def treeNodeSelected(self):
		item=self.treeWidget_holes.currentItem()
		holeIDs=set()
		
		if item.childCount() > 0:
			for i in range(item.childCount()) :
				holeIDs.add(item.child(i).type()-1000)
				
		else:
			holeIDs.add(item.type()-1000)
			
		self.boardDrillsWidget.setSelectedHoles(holeIDs)
		
		
	def startNextTrafo(self):
		#print("Move CNC over hole and select it!")
		if self.currentTrafoHole==0:
			self.currentTrafoHole=1
			self.pushButton_startNextTrafo.setText("Next Hole")
			self.pushButton_finishTrafo.setEnabled(True)
			
		elif self.currentTrafoHole<3:
			self.currentTrafoHole+=1
			self.label_trafoPoints.setText(str(self.currentTrafoHole))
		
		else:
			self.pushButton_startNextTrafo.setEnabled(False)
			
			
	def finishTrafo(self):
		
		# calculate transformation from collected points
		self.pushButton_startNextTrafo.setText("Start")
		self.pushButton_startNextTrafo.setEnabled(True)
		self.pushButton_finishTrafo.setEnabled(False)
		self.label_trafoPoints.setText(str(0))
		
		

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

