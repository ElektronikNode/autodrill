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

		# set up the user interface from Designer.
		self.setupUi(self)

		self.tableWidget_drills.cellChanged.connect(self.cellChanged)
		self.pushButton_OK.clicked.connect(self.OK_clicked)
		self.pushButton_cancel.clicked.connect(self.cancel_clicked)

		self.drills={}		# dictionary diameter ->toolNr.
		self.diaTol=None	# diameter tolerance


	def cellChanged(self, row, column):

		# append rows if necessary
		rowCount=self.tableWidget_drills.rowCount()
		text=self.tableWidget_drills.item(row, column).text()

		if row == rowCount-1 and text:
			self.tableWidget_drills.setRowCount(rowCount+1)

	def OK_clicked(self):
		try:
			# try to read diameters and toolNrs from table
			drills={}
			for row in range(self.tableWidget_drills.rowCount()):
				
				if self.tableWidget_drills.item(row, 0) and self.tableWidget_drills.item(row, 1):
					
					diaStr=self.tableWidget_drills.item(row, 0).text()
					toolNrStr=self.tableWidget_drills.item(row, 1).text()
					
					if diaStr and toolNrStr:
						dia=float(diaStr)
						toolNr=int(toolNrStr)
						
						# check for positive toolNr and dia
						if dia>0 and toolNr>0:
							
							# check for double drills 
							if not dia in drills:
								drills[dia]=toolNr
							else:
								raise
						else:
							raise
							
			# try to read diameter tolerance
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

		# write drills back to table, sorted by toolNr
		self.tableWidget_drills.clearContents()
		self.tableWidget_drills.setRowCount(len(drills)+1)

		dias=drills.keys()
		dias.sort()
		
		for i in range(len(dias)):
			dia=dias[i]
			item=QTableWidgetItem(str(dia))
			self.tableWidget_drills.setItem(i, 0, item)
			item=QTableWidgetItem(str(drills[dia]))
			self.tableWidget_drills.setItem(i, 1, item)

	def setHoleTol(self, diaTol):
		self.diaTol=diaTol

		self.lineEdit_holeTol.setText(str(diaTol))
