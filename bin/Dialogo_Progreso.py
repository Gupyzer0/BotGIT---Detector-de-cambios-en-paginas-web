#Dialogo progress bar

import sys, re, logging
sys.path.append("../interfaz")

from PyQt4 import QtCore, QtGui
from Ui_Dialogo_Progreso import Ui_Dialogo_Progreso

class Dialogo_Progreso(QtGui.QWidget):
	def __init__(self):
		super(Dialogo_Progreso, self).__init__()
		self.dialogo = QtGui.QDialog()
		self.dialogo.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.dialogo.setModal(True)
		self.ui = Ui_Dialogo_Progreso(self.dialogo)
