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

from ui_dialogDrills import Ui_DialogDrills

class DialogDrills(QDialog, Ui_DialogDrills):
	def __init__(self, parent=None):
		QDialog.__init__(self, parent)

		# Set up the user interface from Designer.
		self.setupUi(self)

		self.tableWidget_drills.cellChanged.connect(self.cellChanged)
		self.pushButton_OK.clicked.connect(self.OK_clicked)
		self.pushButton_cancel.clicked.connect(self.cancel_clicked)

		self.drills=list()
		self.diaTol=None


	def cellChanged(self, row, column):

		rowCount=self.tableWidget_drills.rowCount()
		text=self.tableWidget_drills.item(row, column).text()

		if row == rowCount-1 and text:
			self.tableWidget_drills.setRowCount(rowCount+1)

	def OK_clicked(self):
		try:
			drills=list()
			for row in range(self.tableWidget_drills.rowCount()):
				if self.tableWidget_drills.item(row, 0):
					text=self.tableWidget_drills.item(row, 0).text()
					if text:
						dia=float(text)
						if dia>0:
							drills.append(dia)
						else:
							raise

			diaTol=float(self.lineEdit_holeTol.text())
			if diaTol<0:
				raise

			self.drills=drills
			self.diaTol=diaTol
			if not drills:
				raise

			self.accept()
		except:
			QMessageBox.critical(self, "Invalid Input", "Please enter positive numbers only. Define at least one drill.")

	def cancel_clicked(self):
		self.reject()


	def getDrills(self):
		return self.drills

	def getHoleTol(self):
		return self.diaTol

	def setDrills(self, drills):
		self.drills=drills

		self.tableWidget_drills.clearContents()
		self.tableWidget_drills.setRowCount(len(drills)+1)

		for i in range(len(drills)):
			item=QTableWidgetItem(str(drills[i]))
			self.tableWidget_drills.setItem(i, 0, item)

	def setHoleTol(self, diaTol):
		self.diaTol=diaTol

		self.lineEdit_holeTol.setText(str(diaTol))
