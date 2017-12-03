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

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDialog, QMessageBox, QPixmap

from ui_dialogDrillParameter import Ui_DialogDrillParameter

import os


autodrill_root = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")


class DialogDrillParameter(QDialog, Ui_DialogDrillParameter):
	def __init__(self, parent=None):
		QDialog.__init__(self, parent)

		# Set up the user interface from Designer.
		self.setupUi(self)

		self.label_sketch.setPixmap(QPixmap(os.path.join(autodrill_root,"assets/images/drill_parameter.png")))
		self.pushButton_OK.clicked.connect(self.OK_clicked)
		self.pushButton_cancel.clicked.connect(self.cancel_clicked)



	def setFeedrate(self, feedrate):
		self.lineEdit_feedrate.setText("{:.2f}".format(feedrate))

	def setDepth(self, depth):
		self.lineEdit_depth.setText("{:.2f}".format(depth))

	def setSpacing(self, spacing):
		self.lineEdit_spacing.setText("{:.2f}".format(spacing))

	def getFeedrate(self):
		return float(self.lineEdit_feedrate.text())

	def getDepth(self):
		return float(self.lineEdit_depth.text())

	def getSpacing(self):
		return float(self.lineEdit_spacing.text())

	def OK_clicked(self):
		try:
			feedrate=float(self.lineEdit_feedrate.text())
			depth=float(self.lineEdit_depth.text())
			spacing=float(self.lineEdit_spacing.text())

			if feedrate<=0 or depth<0 or spacing<0:
				raise
			else:
				self.accept()

		except:
			QMessageBox.critical(self, "Invalid Input", "Please enter positive numbers only.")


	def cancel_clicked(self):
		self.reject()
