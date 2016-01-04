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
	
		
		
