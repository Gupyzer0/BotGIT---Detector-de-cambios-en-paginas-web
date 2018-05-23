import sys, re, logging
sys.path.append("../interfaz")

from PyQt4 import QtCore, QtGui
from qt4BaseDatos import baseDatos
from Ui_Dialogo_Editar_Portal import Ui_Dialogo_Editar_Portal

class Dialogo_Editar_Portal(QtGui.QWidget):
	def __init__(self,nombrePortal,nombreEnte):
		super(Dialogo_Editar_Portal, self).__init__()
		self.dialogo = QtGui.QDialog()
		self.dialogo.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.dialogo.setModal(True)
		self.ui = Ui_Dialogo_Editar_Portal(self.dialogo)
		self.msgBox = QtGui.QMessageBox()
		self.msgBox.setIcon(QtGui.QMessageBox.Warning)
		self.msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
		self.msgBox.setModal(True)
		self.valido = False
		self.arrPortales = baseDatos.seleccionar_nombres_portales(nombreEnte)
		for portal in self.arrPortales:
			self.ui.comboBox.addItem(portal)
		self.nombrePortal = nombrePortal
		self.ui.lineEdit.setText(self.nombrePortal)

		self.ui.lineEdit.textChanged.connect(self.cambiarNombrePortal)

	def cambiarNombrePortal(self):
		self.nombrePortal = self.ui.lineEdit.text()















