import sys, re, logging
sys.path.append("../interfaz")

from PyQt4 import QtCore, QtGui
from qt4BaseDatos import baseDatos
from Ui_Dialogo_Add_Portal import Ui_Dialogo_Add_Portal

regexTextoNumeros = re.compile('^[a-zA-Z0-9áéíóú _.-]*$')
regexPaginaWeb = re.compile('(http|https|ftp|file):\/\/\S+')

class Dialogo_Add_Portal(QtGui.QWidget):
	def __init__(self):
		super(Dialogo_Add_Portal, self).__init__()
		self.portal = ''
		self.ente = '' #Para usar luego
		self.ministerio = ''
		self.lista = []
		self.valido = False

		self.dialogo = QtGui.QDialog()
		self.dialogo.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.dialogo.setMinimumSize(400,400)
		
		self.ui = Ui_Dialogo_Add_Portal(self.dialogo)
		self.ui.lineEdit.textChanged.connect(self.validar)
		self.ui.plainTextEdit.textChanged.connect(self.validar)
		self.ui.comboBox_entes.currentIndexChanged.connect(self.validar)
		self.ui.comboBox_entes.currentIndexChanged.connect(self.cambiarEnte)
		self.ui.comboBox_ministerio.currentIndexChanged.connect(self.cargar_combobox_entes)
		self.ui.comboBox_ministerio.currentIndexChanged.connect(self.cambiarMinisterio)

		#inicializando combobox de ministerios
		
		#arrMins = ['Ministerio de Prueba']
		arrMins = baseDatos.seleccionar_ministerios()
		for ministerio in arrMins:
			self.ui.comboBox_ministerio.addItem(ministerio)

		#del arrMins
		self.dialogo.setModal(True)
		self.dialogo.show()
		#self.valido = self.urlValida & self.listaValida

	def cambiarEnte(self):
		self.ente = self.ui.comboBox_entes.currentText()
		print("TIPO",type(self.ente))

	def cambiarMinisterio(self):
		self.ministerio = self.ui.comboBox_ministerio.currentText()

	def validar(self):
		#print(self.verificarNombrePortal() & self.verificarLista())
		nombre_lista = self.verificarNombrePortal() & self.verificarLista()
		if self.ui.comboBox_entes.currentText()!= '':
			#print(self.ui.comboBox_entes.currentText())
			#print(nombre_lista)
			enteValido = True
			self.valido =  nombre_lista & enteValido

	def verificarUrl(self,url):
		if regexPaginaWeb.match(url):						
			return(True)
		else:
			return(False)

	def verificarLista(self):
		resultado = False
		texto = self.ui.plainTextEdit.toPlainText()
		lista = texto.split(',')

		for i in range(len(lista)): lista[i] = lista[i].strip()

		for url in lista:
			if self.verificarUrl(url):				
				resultado = True
			else:
				resultado = False
				break	

		if resultado:
			print(self.lista)
			self.lista = lista
			self.ui.plainTextEdit.setStyleSheet("border: 1px solid black")
		else:
			self.ui.plainTextEdit.setStyleSheet("border: 2px solid red")
		return resultado

	def verificarNombrePortal(self):
		if len(str(self.ui.lineEdit.text())) < 1:
			self.ui.lineEdit.setStyleSheet("border: 2px solid red")
			return False
		elif not regexTextoNumeros.match(str(self.ui.lineEdit.text())):
			self.ui.lineEdit.setStyleSheet("border: 2px solid red")
			return False
		else:
			self.portal = self.ui.lineEdit.text()
			self.ui.lineEdit.setStyleSheet("border: 1px solid black")
			return True

	def closeEvent(self,event):
		self.destroy()

	def cargar_combobox_entes(self):
		self.ui.comboBox_entes.clear()
		
		arrEntes = baseDatos.seleccionar_entes(self.ui.comboBox_ministerio.currentText())
		
		for ente in arrEntes:
			self.ui.comboBox_entes.addItem(ente)
		