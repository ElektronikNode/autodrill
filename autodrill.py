
from PyQt4.QtGui import QMainWindow
from PyQt4 import Qt

from mainwindow import Ui_MainWindow
from BoardDrillsWidget import BoardDrillsWidget
from VideoWidget import VideoWidget

from readDrill import *
from bilinear import *

import sys

allHoles = None


class AutodrillMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # Set up the user interface from Designer.
        self.setupUi(self)
        
        #self.cameraWidgetObject = VideoWidget()
        #self.gridLayout.addWidget(self.cameraWidgetObject, 0, 1, 1, 1)

        self.boardDrillsObject = BoardDrillsWidget(allHoles)
        self.gridLayout.addWidget(self.boardDrillsObject, 0, 0, 2, 1)

# assign holes to drills from given toolbox
# pick next larger drill except d_hole < d_drill + tol
def fitHolesToDrills(holes, drills, tol):
	diaList=list(holes.keys())		# list of hole diameters
	drillDiaList=list(drills)		# list of drill diameters
	
	diaList.sort()
	drillDiaList.sort()
	
	newHoles={}							# dict of holes with assigned diameters
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
		if drillDia not in newHoles:
			newHoles[drillDia]=set()
			
		# assign holes
		newHoles[drillDia] |= (holes[dia])
		
	return newHoles

if __name__ == '__main__':
	
	allHoles=readDrillFile("test.drl")

	drills={0.6, 0.8, 1.1, 1.3, 1.5, 1.7, 2.0}
	
	newHoles=fitHolesToDrills(allHoles, drills, 0.05)
	
	for dia in newHoles:
		print()
		print("dia "+str(dia)+":")
		print(newHoles[dia])
		print()
		
	
	points = {(0, 0), (1, 0), (0, 1)}
	points_t = {(0, 0), (1, 0.1), (-0.1, 1)}

	
	T=bilinear(points, points_t)
	
	p = (0.5, 0.5)

	print(T.transform(p))
	
	app = Qt.QApplication(sys.argv)
	ui = AutodrillMainWindow()
	ui.show()
	
	sys.exit(app.exec_())

