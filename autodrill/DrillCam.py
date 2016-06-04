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

from VideoWidget import VideoWidget, opencv_available
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


	def cameraAvailable(self):
		return opencv_available  # TODO: detect if camera gives frames
