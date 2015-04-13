from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPainter, QWidget
from PyQt4.QtCore import QRectF

class BoardDrillsWidget(QWidget):
    """ A class for rendering board drills """
 
    def __init__(self, allHoles, parent=None):
        QWidget.__init__(self)
        
        self.setMinimumSize(200, 200)
        
        self.setAllHoles(allHoles)
    
    def paintEvent(self, event): 
        qp = QPainter(self)
        qp.setRenderHints(QPainter.Antialiasing)
        self.drawHoles(qp, self.allHoles)
        qp.end()
    
    def setAllHoles(self, allHoles):
        self.allHoles = allHoles
        self.repaint()
    
    def drawHoles(self, qp, allHoles):
        boardMargin = 1
        boardPadding = 10
        
        # calculate size of board to fit all holes
        maxX, minX = None, None
        maxY, minY = None, None

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
        boardScaleHeight = availableSpaceHeight/boardHeight
        boardScaleWidth = availableSpaceWidth/boardWidth
        
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
        
        # draw single holes
        for drillsize in allHoles:
            for hole in allHoles[drillsize]:
                self.drawSingleHole(qp, startWidth+((hole[0]-minX)*scale), startHeight+((hole[1]-minY)*scale), drillsize)

    def drawSingleHole(self, qp, x, y, drillsize):
        # set color of hole
        qp.setPen(QtGui.QColor.fromHsv(int(drillsize*255/3), 255, 196))
        qp.setBrush(QtGui.QColor.fromHsv(int(drillsize*255/3), 255, 196))

        # draw hole
        qp.drawEllipse(QRectF(x-4, y-4, 8, 8))

    def drawBoardOutline(self, qp, x, y, w, h):
        # set color of outline
        qp.setPen(QtCore.Qt.lightGray)
        qp.setBrush(QtCore.Qt.white)

        # draw outline
        qp.drawRect(x, y, w, h)