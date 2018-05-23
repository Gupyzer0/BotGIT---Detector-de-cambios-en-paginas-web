import sys, re, logging
sys.path.append("../interfaz")

from PyQt4 import QtCore, QtGui
from qt4BaseDatos import baseDatos
from Ui_Dialogo_Agregar_Entes import Ui_Dialogo_Agregar_Entes

regexTextoNumeros = re.compile('^[a-zA-Z0-9áéíóú _.-]*$')
regexPaginaWeb = re.compile('(http|https|ftp|file):\/\/\S+')

class Dialogo_Agregar_Entes(QtGui.QWidget):
	def __init__(self):
		super(Dialogo_Agregar_Entes, self).__init__()
		self.ente = '' #Para usar luego
		self.ministerio = ''

		self.dialogo = QtGui.QDialog()
		self.dialogo.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.dialogo.setMinimumSize(400,400)
		
		self.ui = Ui_Dialogo_Agregar_Entes(self.dialogo)
		self.ui.comboBox.currentIndexChanged.connect(self.cambiarMinisterio)
		self.ui.lineEdit.textChanged.connect(self.cambiarEnte)

		#inicializando combobox de ministerios
		arrMins = baseDatos.seleccionar_ministerios()
		for ministerio in arrMins:
			self.ui.comboBox.addItem(ministerio)

		del arrMins
		self.dialogo.setModal(True)
		self.dialogo.show()

	def cambiarMinisterio(self):
		self.ministerio = self.ui.comboBox.currentText()

	def cambiarEnte(self):
		self.ente = self.ui.lineEdit.text()

	def closeEvent(self,event):
		self.destroy()


