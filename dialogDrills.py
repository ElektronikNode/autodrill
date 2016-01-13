
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

