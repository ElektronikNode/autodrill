import cv
from VideoWidget import VideoWidget
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication, QImage, QPainter, QWidget
from PyQt4.QtCore import QRectF


class DrillCam(VideoWidget):
    """ A class for rendering video coming from OpenCV and drawing a center grid """

    def __init__(self, parent=None):
        VideoWidget.__init__(self, parent)


    def paintEvent(self, event):
        VideoWidget.paintEvent(self, event)

        if not self.is_connected:
            return

        qp = QPainter(self)
        qp.setRenderHints(QPainter.Antialiasing)
        #painter.begin(self)
        qp.setPen(QtGui.QColor(255, 255, 0))
        self.drawCenterGrid(qp)


    def drawCenterGrid(self, qp):
        size = self.size()
        mid_x = size.width()/2
        mid_y = size.height()/2

        max_radius = min([size.width()/2, size.height()/2])-5
        spacing = 30

        for radius in range(20, max_radius, spacing):
            qp.drawEllipse(mid_x-radius, mid_y-radius, 2*radius, 2*radius)
            qp.drawLine(mid_x-radius-spacing/2, mid_y-spacing/2 , mid_x-radius-spacing/2, mid_y+spacing/2)
            qp.drawLine(mid_x+radius+spacing/2, mid_y-spacing/2 , mid_x+radius+spacing/2, mid_y+spacing/2)
            qp.drawLine(mid_x-spacing/2, mid_y-radius-spacing/2 , mid_x+spacing/2, mid_y-radius-spacing/2)
            qp.drawLine(mid_x-spacing/2, mid_y+radius+spacing/2 , mid_x+spacing/2, mid_y+radius+spacing/2)

        qp.drawLine(mid_x, 0 , mid_x, size.height())
        qp.drawLine(0, mid_y , size.width(), mid_y)
