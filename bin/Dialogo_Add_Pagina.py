import sys, re, logging
sys.path.append("../interfaz")

from PyQt4 import QtCore, QtGui
from qt4BaseDatos import baseDatos
from Ui_Dialogo_Add_Pagina import Ui_Dialogo_Add_Pagina

regexTextoNumeros = re.compile('^[a-zA-Z0-9áéíóú _.-]*$')
regexPaginaWeb = re.compile('(http|https|ftp|file):\/\/\S+')

class Dialogo_Add_Pagina(QtGui.QWidget):
	def __init__(self):
		super(Dialogo_Add_Pagina, self).__init__()
		self.lista = []
		self.listaUrls = baseDatos.seleccionar_paginas_nombres()
		self.valido = False

		self.dialogo = QtGui.QDialog()
		self.dialogo.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		
		self.ui = Ui_Dialogo_Add_Pagina(self.dialogo)
		self.ui.textEdit.textChanged.connect(self.verificarLista)
		self.dialogo.setModal(True)
		self.dialogo.show()

	def verificarUrl(self,url):
		if regexPaginaWeb.match(url):						
			if url in self.listaUrls:
				logging.info("la url " + str(url) + " ya se encuentra en la base de datos")
				return(False)
			return(True)
		else:
			return(False)

	def verificarLista(self):
		self.valido = False
		texto = self.ui.textEdit.toPlainText()
		lista = texto.split(',')

		for i in range(len(lista)): lista[i] = lista[i].strip()

		for url in lista:
			if self.verificarUrl(url):				
				self.valido = True
			else:
				self.valido = False
				break	

		if self.valido:
			self.lista = lista
			self.ui.textEdit.setStyleSheet("border: 1px solid black")
		else:
			self.ui.textEdit.setStyleSheet("border: 2px solid red")

	def closeEvent(self,event):
		self.destroy()
