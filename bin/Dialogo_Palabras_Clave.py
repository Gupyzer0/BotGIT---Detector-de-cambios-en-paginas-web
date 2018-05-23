import sys, re, logging, functools
sys.path.append("../interfaz")

from PyQt4 import QtCore, QtGui
from Ui_Dialogo_Palabras_Clave import Ui_Dialogo_Palabras_Clave #usa las misma interfaz que la edicion de ministerios

class Dialogo_Palabras_Clave(QtGui.QWidget):
	def __init__(self, arrPalabras):
		super(Dialogo_Palabras_Clave, self).__init__()	
		
		self.palabrasClave = arrPalabras

		self.dialogo = QtGui.QDialog()
		self.dialogo.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.dialogo.setModal(True)
		self.ui = Ui_Dialogo_Palabras_Clave()
		self.ui.setupUi(self.dialogo)
		self.ui.listWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

		self.ui.pushButton_2.clicked.connect(self.addpalabrasClave)
		self.ui.pushButton.clicked.connect(self.eliminarPalabrasClave)
		
		for palabra in self.palabrasClave:self.ui.listWidget.addItem(palabra)
		
		self.dialogo.setModal(True)
		self.dialogo.show()

	def addpalabrasClave(self):
		#separando cadena de texto ingresada usando como delimitador las comas (',')
		arrNuevasPalabras = [palabra.strip() for palabra in self.ui.lineEdit.text().split(',')]
		#self.palabrasClave = []

		#agregando elementos validos a arrNuevasPalabrasVerficadas
		for palabra in arrNuevasPalabras: 
			if palabra != '':
				if palabra not in self.palabrasClave:
					self.palabrasClave.append(palabra)

		#actualizando vista con palabras clave nuevas
		self.ui.listWidget.clear()

		for palabra in self.palabrasClave: self.ui.listWidget.addItem(palabra)

		#actualizando archivo con palabras clave
		try:

			print(self.palabrasClave)

			with open("../bdatos/palabrasClave.txt",'w') as archivoPalabras:
				for palabra in self.palabrasClave:
					archivoPalabras.write(palabra + '\n')

		except IOError:
			print("No se pudo acceder al archivo para guardar las palabras clave")

		finally:
			archivoPalabras.close()

	def eliminarPalabrasClave(self):
		#removiendo widgetItems de la lista
		for item in self.ui.listWidget.selectedItems():		
			self.ui.listWidget.takeItem(self.ui.listWidget.row(item))
			self.palabrasClave.remove(item.text())

		print("palabras luego de removerse",self.palabrasClave)
		
		try:
			with open("../bdatos/palabrasClave.txt",'w') as archivoPalabras:
				for palabra in self.palabrasClave:
					archivoPalabras.write(palabra + '\n')
		except IOError:
			print("No se pudo acceder al archivo para guardar las palabras clave")

		finally:
			archivoPalabras.close()





		

