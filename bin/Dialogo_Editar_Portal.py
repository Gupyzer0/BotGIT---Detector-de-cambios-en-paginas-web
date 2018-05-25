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

		self.listaPortales = baseDatos.seleccionar_portales_nombres()
		self.listaEntes = baseDatos.seleccionar_todos_entes()

		for ente in self.listaEntes:
			self.ui.comboBox.addItem(ente)
		
		#colocando valor por defecto del combobox
		self.ui.comboBox.setCurrentIndex(self.ui.comboBox.findText(nombreEnte))

		self.nombrePortalOriginal = nombrePortal
		self.nombrePortal = nombrePortal
		self.ente = nombreEnte
		
		self.ui.lineEdit.setText(self.nombrePortal)
		
		self.ui.lineEdit.textChanged.connect(self.cambiarNombreYEntePortal)
		self.ui.comboBox.currentIndexChanged.connect(self.cambiarNombreYEntePortal)
		self.ui.lineEdit.textChanged.connect(self.validarPortal)
		self.ui.comboBox.currentIndexChanged.connect(self.validarPortal)

	def cambiarNombreYEntePortal(self):
		self.nombrePortal = self.ui.lineEdit.text()
		self.ente = self.ui.comboBox.currentText()

	def validarPortal(self):
		if self.nombrePortal == '':
			self.ui.lineEdit.setStyleSheet("border: 2px solid red")
			self.valido = False
			return

		if self.nombrePortal != self.nombrePortalOriginal:
			if self.nombrePortal in self.listaPortales:
				self.ui.lineEdit.setStyleSheet("border: 2px solid red")
				self.valido = False
				return

		self.ui.lineEdit.setStyleSheet("border: 1px solid black")
		self.valido = True
