import cv
import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication, QImage, QPainter, QWidget, QMessageBox
from PyQt4.QtCore import QObject, SIGNAL, SLOT, QPointF, QRectF, QPointF, QPoint, QTimer


class IplQImage(QImage):
	"""
	http://matthewshotton.wordpress.com/2011/03/31/python-opencv-iplimage-to-pyqt-qimage/
	A class for converting iplimages to qimages
	"""

	def __init__(self,iplimage):
		# Rough-n-ready but it works dammit
		alpha = cv.CreateMat(iplimage.height,iplimage.width, cv.CV_8UC1)
		cv.Rectangle(alpha, (0, 0), (iplimage.width,iplimage.height), cv.ScalarAll(255) ,-1)
		rgba = cv.CreateMat(iplimage.height, iplimage.width, cv.CV_8UC4)
		cv.Set(rgba, (1, 2, 3, 4))
		cv.MixChannels([iplimage, alpha],[rgba], [
		(0, 0), # rgba[0] -> bgr[2]
		(1, 1), # rgba[1] -> bgr[1]
		(2, 2), # rgba[2] -> bgr[0]
		(3, 3)  # rgba[3] -> alpha[0]
		])
		self.__imagedata = rgba.tostring()
		super(IplQImage,self).__init__(self.__imagedata, iplimage.width, iplimage.height, QImage.Format_RGB32)


class VideoWidget(QWidget):
	""" A class for rendering video coming from OpenCV """

	def __init__(self, parent=None):
		QWidget.__init__(self)

		self.zoom = 1
		self.is_connected = False

		self._capture = cv.CaptureFromCAM(0)

		# Take one frame to query height
		frame = cv.QueryFrame(self._capture)
		if frame is None:
			QMessageBox.information(self, "Could not open camera", "Please configure/enable camera");
			return

		self.is_connected = True
		self.setMinimumSize(300,300)
		self._frame = None
		self._image = self._build_image(frame)

		# Paint every 50 ms
		self._timer = QTimer(self)
		self._timer.timeout.connect(self.queryFrame)
		self._timer.start(50)
		
			
	def setZoom(self, zoom):
		self.zoom=zoom


	def _build_image(self, frame):
		# TODO: don't user member variable self._frame
		if not self._frame:
			self._frame = cv.CreateImage((frame.width, frame.height), cv.IPL_DEPTH_8U, frame.nChannels)

		if frame.origin == cv.IPL_ORIGIN_TL:
			cv.Copy(frame, self._frame)
		else:
			cv.Flip(frame, self._frame, 0)

		dst_frame = cv.CreateImage(cv.GetSize(self._frame), self._frame.depth, self._frame.nChannels)

		width_height_ratio = float(self.width())/float(self.height()) #()/

		center_width = self._frame.width/2.
		center_height = self._frame.height/2.
		delta_width = float(self._frame.width)/self.zoom

		# calculate region of interrest using widget size
		if width_height_ratio >= float(self._frame.width)/float(self._frame.height):
			delta_height = float(self._frame.height)/self.zoom
			delta_width = delta_height*width_height_ratio
		else:
			delta_width = float(self._frame.width)/self.zoom
			delta_height = delta_width/width_height_ratio

		# fix delta, if delta is greater than image size
		if delta_height > self._frame.height:
			delta_width *= self._frame.height/delta_height
			delta_height = self._frame.height
		if delta_width > self._frame.width:
			delta_height *= self._frame.width/delta_width
			delta_width = self._frame.width

		# TODO: fix zoom inaccuracy (+-1px)
		cv.SetImageROI(self._frame, (int(center_width-delta_width/2.), int(center_height-delta_height/2.), int(delta_width), int(delta_height)))

		dst_frame = cv.CreateImage((self.width(), self.height()), cv.IPL_DEPTH_8U, frame.nChannels)
		cv.Resize(self._frame, dst_frame)

		cv.ResetImageROI(self._frame)

		return IplQImage(dst_frame)


	def paintEvent(self, event):
		qp = QPainter(self)

		if not self.is_connected:
			# fill background grey
			qp.setPen(QtCore.Qt.gray)
			qp.setBrush(QtCore.Qt.gray)
			qp.drawRect(0, 0, self.width(), self.height())
			# draw text
			qp.setPen(QtCore.Qt.white)
			qp.drawText(QRectF(0, 0, self.width(), self.height()), QtCore.Qt.AlignCenter, "Device not found!")
			return

		qp.drawImage(QPoint(0, 0), self._image)


	def queryFrame(self):
		frame = cv.QueryFrame(self._capture)
		if frame is None:
			if self.is_connected:
				self.is_connected = False
				self.update()
			self.is_connected = False
			return
		self.is_connected = True
		self._image = self._build_image(frame)
		self.update()
		
		
	def pause(self):
		self._timer.stop()
		
	def resume(self):
		self._timer.start()
