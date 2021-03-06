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
'''

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPainter, QWidget
from PyQt4.QtCore import QRectF, pyqtSignal

class BoardDrillsWidget(QWidget):
	""" A class for rendering board drills """
	holeSelected=pyqtSignal(object)

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)

		self.setMinimumSize(200, 200)
		self.allHoles={}
		self.selectedHoles=list()


	def paintEvent(self, event):
		#print("paint")
		qp = QPainter(self)
		qp.setRenderHints(QPainter.Antialiasing)

		if self.allHoles:
			self.drawBoard(qp, self.allHoles)
		else:
			# fill background grey
			qp.setPen(QtCore.Qt.gray)
			qp.setBrush(QtCore.Qt.gray)
			qp.drawRect(0, 0, self.width(), self.height())
			# draw text
			qp.setPen(QtCore.Qt.white)
			qp.drawText(QRectF(0, 0, self.width(), self.height()), QtCore.Qt.AlignCenter, "Please load drill file")


	def setAllHoles(self, allHoles):
		self.allHoles = allHoles
		#print(self.allHoles)
		self.update()


	# transform real coordinates (mm) to pixel coordinates
	def real2Pixel(self, pos):
		x,y=pos
		xPixel=self.startWidth + (x-self.minX)*self.scale
		yPixel=self.height() - (self.startHeight + (y-self.minY)*self.scale)

		return xPixel,yPixel


	def drawBoard(self, qp, allHoles):
		boardMargin = 1
		boardPadding = 10

		# calculate size of board to fit all holes
		self.minX, maxX = None, None
		self.minY, maxY = None, None

		for drillsize in allHoles:
			for hole in allHoles[drillsize]:
				if maxX is None or hole[0] > maxX:
					maxX = hole[0]
				if self.minX is None or hole[0] < self.minX:
					self.minX = hole[0]
				if maxY is None or hole[1] > maxY:
					maxY = hole[1]
				if self.minY is None or hole[1] < self.minY:
					self.minY = hole[1]

		boardHeight = maxY-self.minY
		boardWidth = maxX-self.minX

		size = self.size()

		availableSpaceHeight = size.height()-2*boardMargin-2*boardPadding
		availableSpaceWidth = size.width()-2*boardMargin-2*boardPadding

		# calculate self.scale, to fit board
		boardScaleHeight = availableSpaceHeight/float(boardHeight)
		boardScaleWidth = availableSpaceWidth/float(boardWidth)

		self.scale = min([boardScaleHeight, boardScaleWidth])

		# calculate start-position of drills on widget
		self.startWidth = boardMargin+boardPadding+(size.width()-2*boardMargin-(boardWidth*self.scale+2*boardPadding))/2
		self.startHeight = boardMargin+boardPadding+(size.height()-2*boardMargin-(boardHeight*self.scale+2*boardPadding))/2

		# draw outline
		self.drawBoardOutline(qp,
							  self.startWidth-boardPadding,
							  self.startHeight-boardPadding,
							  boardWidth*self.scale+2*boardPadding,
							  boardHeight*self.scale+2*boardPadding)


		#print(self.selectedHoleIDs)


		# draw single holes
		for drillsize in allHoles:
			for hole in allHoles[drillsize]:
				#print(hole[2])
				if hole in self.selectedHoles:
					selected=True
					#print("selected")
				else:
					selected=False

				self.drawSingleHole(qp, self.real2Pixel((hole[0], hole[1])), drillsize, selected)


	def drawSingleHole(self, qp, pos, drillsize, selected):
		# set color of hole
		dias=self.allHoles.keys()
		dMin=min(dias)
		dMax=max(dias)
		hue=180
		if(dMin != dMax):
			hue=(drillsize-dMin)/(dMax-dMin)*240+60
		
		color=QtGui.QColor.fromHsv(hue, 255, 196)

		if selected:
			#print("selected")
			color=QtGui.QColor.fromRgb(255, 0, 0)

		qp.setPen(color)
		qp.setBrush(color)

		# draw hole
		x,y=pos
		qp.drawEllipse(QRectF(x-4, y-4, 8, 8))


	def drawBoardOutline(self, qp, x, y, w, h):
		# set color of outline
		qp.setPen(QtCore.Qt.lightGray)
		qp.setBrush(QtCore.Qt.white)

		# draw outline
		qp.drawRect(x, y, w, h)


	def setSelectedHoles(self, holes):
		self.selectedHoles=holes
		self.update()


	def mousePressEvent(self, event):
		xm=event.x()
		ym=event.y()

		for drillsize in self.allHoles:
			for hole in self.allHoles[drillsize]:
				xh,yh=self.real2Pixel((hole[0], hole[1]))
				if ((xm-xh)*(xm-xh)+(ym-yh)*(ym-yh) < 10*10):
					self.holeSelected.emit(hole)
