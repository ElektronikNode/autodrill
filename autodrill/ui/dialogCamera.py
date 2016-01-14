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
from PyQt4.QtGui import QDialog, QMessageBox, QTableWidgetItem

from machineInterface import *

from ui_dialogCamera import Ui_DialogCamera

class DialogCamera(QDialog, Ui_DialogCamera):
	def __init__(self, parent=None):
		QDialog.__init__(self, parent)

		# Set up the user interface from Designer.
		self.setupUi(self)

		self.offset=(0, 0)

		self.pushButton_OK.clicked.connect(self.OK_clicked)
		self.pushButton_cancel.clicked.connect(self.cancel_clicked)



	def OK_clicked(self):
		try:
			self.offset=(float(self.lineEdit_offsetX.text()), float(self.lineEdit_offsetY.text()))
			self.accept()
		except:
			QMessageBox.critical(self, "Invalid Input", "Please enter numbers only.")

	def cancel_clicked(self):
		self.reject()


	def setOffset(self, offset):
		self.offset=offset
		x, y = offset
		self.lineEdit_offsetX.setText("{:.3f}".format(x))
		self.lineEdit_offsetY.setText("{:.3f}".format(y))

	def getOffset(self):
		return self.offset
