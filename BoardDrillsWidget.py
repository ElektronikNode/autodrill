from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPainter, QWidget
from PyQt4.QtCore import QRectF

class BoardDrillsWidget(QWidget):
	""" A class for rendering board drills """
 
	def __init__(self, parent=None):
		QWidget.__init__(self)
		
		self.setMinimumSize(200, 200)
		self.allHoles={}
		self.selectedHoleIDs={}
	
	
	def paintEvent(self, event):
		#print("paint")
		qp = QPainter(self)
		qp.setRenderHints(QPainter.Antialiasing)
		if self.allHoles:
			self.drawBoard(qp, self.allHoles)
		else:
			self.drawBoardOutline(qp, 0, 0, self.width(), self.height())
		qp.end()
	
	
	def setAllHoles(self, allHoles):
		self.allHoles = allHoles
		self.update()
	
	
	def drawBoard(self, qp, allHoles):
		boardMargin = 1
		boardPadding = 10
		
		# calculate size of board to fit all holes
		minX, maxX = None, None
		minY, maxY = None, None

		for drillsize in allHoles:
			for hole in allHoles[drillsize]:
				if hole[0] > maxX or maxX is None:
					maxX = hole[0]
				if hole[0] < minX or minX is None:
					minX = hole[0]
				if hole[1] > maxY or maxY is None:
					maxY = hole[1]
				if hole[1] < minY or minY is None:
					minY = hole[1]

		boardHeight = maxY-minY
		boardWidth = maxX-minX
		
		size = self.size()

		availableSpaceHeight = size.height()-2*boardMargin-2*boardPadding
		availableSpaceWidth = size.width()-2*boardMargin-2*boardPadding

		# calculate scale, to fit board
		boardScaleHeight = availableSpaceHeight/float(boardHeight)
		boardScaleWidth = availableSpaceWidth/float(boardWidth)
		
		scale = min([boardScaleHeight, boardScaleWidth])
		
		# calculate start-position of drills on widget
		startWidth = boardMargin+boardPadding+(size.width()-2*boardMargin-(boardWidth*scale+2*boardPadding))/2
		startHeight = boardMargin+boardPadding+(size.height()-2*boardMargin-(boardHeight*scale+2*boardPadding))/2
	
		# draw outline
		self.drawBoardOutline(qp, 
							  startWidth-boardPadding,
							  startHeight-boardPadding,
							  boardWidth*scale+2*boardPadding,
							  boardHeight*scale+2*boardPadding)
							  
	
		#print(self.selectedHoleIDs)
		
		# draw single holes
		for drillsize in allHoles:
			for hole in allHoles[drillsize]:
				#print(hole[2])
				if hole[2] in self.selectedHoleIDs:
					selected=True
					#print("selected")
				else:
					selected=False
					
				self.drawSingleHole(qp, startWidth+((hole[0]-minX)*scale), startHeight+((hole[1]-minY)*scale), drillsize, selected)


	def drawSingleHole(self, qp, x, y, drillsize, selected):
		# set color of hole
		color=QtGui.QColor.fromHsv(int(drillsize*255/3), 255, 196)
		
		if selected:
			#print("selected")
			color=QtGui.QColor.fromRgb(255, 0, 0)
			
		qp.setPen(color)
		qp.setBrush(color)

		# draw hole
		qp.drawEllipse(QRectF(x-4, y-4, 8, 8))


	def drawBoardOutline(self, qp, x, y, w, h):
		# set color of outline
		qp.setPen(QtCore.Qt.lightGray)
		qp.setBrush(QtCore.Qt.white)

		# draw outline
		qp.drawRect(x, y, w, h)
		
	def setSelectedHoles(self, holeIDs):
		self.selectedHoleIDs=holeIDs
		self.update()

