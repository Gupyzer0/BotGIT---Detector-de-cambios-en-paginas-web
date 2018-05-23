#Widget para filtrar los portales vistos por ministerio
import sys, re, logging
sys.path.append("../interfaz")

from PyQt4 import QtCore, QtGui, Qt
from qt4BaseDatos import baseDatos
from Ui_Dialogo_Filtrar_Ministerios import Ui_Dialogo_Filtrar_Ministerios

regexTextoNumeros = re.compile('^[a-zA-Z0-9áéíóú _.-]*$')
regexPaginaWeb = re.compile('(http|https|ftp|file):\/\/\S+')

class Dialogo_Filtrar_Ministerios(QtGui.QWidget):
	def __init__(self):
		super(Dialogo_Filtrar_Ministerios, self).__init__()

		self.dialogo = QtGui.QDialog()
		self.dialogo.setModal(True)
		self.dialogo.setAttribute(QtCore.Qt.WA_DeleteOnClose)
				
		self.ui = Ui_Dialogo_Filtrar_Ministerios(self.dialogo)
		
		#obtener lista de ministerios
		self.listaMinisterios = baseDatos.seleccionar_ministerios()

		#Al inicio son iguales porque todos los ministerios por defecto aparece seleccionados
		self.listaMinisteriosFiltrada = self.listaMinisterios		
		
		#self.ui.tableWidget.setRowCount(len(listaMinisterios))
		for i in range(len(self.listaMinisterios)):
			self.ui.tableWidget.setRowCount(len(self.listaMinisterios))

			checkBox = QtGui.QTableWidgetItem()
			checkBox.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
			checkBox.setCheckState(QtCore.Qt.Checked)

			#Cuando el estado del checkbox cambia se conecta al metodo obtenerLista para actualizarla
			
			self.ui.tableWidget.setItem(i,0,checkBox)			
			#self.ui.tableWidget.itemChanged.connect(self.obtenerLista)
			
			self.ui.tableWidget.setItem(i,1, QtGui.QTableWidgetItem(self.listaMinisterios[i]))
			self.ui.tableWidget.item(i,1).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

		#Lo unico "cambiable" son los checkbox, cuando estos cambien, se ejecuta la funcion obtenerLista y
		#de esta forma se actualiza la lista de Ministerios
		self.ui.tableWidget.cellChanged.connect(self.obtenerLista)
		self.ui.pushButton.clicked.connect(self.seleccionarTodos)
		self.ui.pushButton_2.clicked.connect(self.desseleccionarTodos)

		#self.dialogo.show()

	def obtenerLista(self):
		self.listaMinisteriosFiltrada = []
		for i in range(len(self.listaMinisterios)):
			if self.ui.tableWidget.item(i,0).checkState() == QtCore.Qt.Checked:
				self.listaMinisteriosFiltrada.append(self.ui.tableWidget.item(i,1).text())

		#return self.listaMinisteriosFiltrada

	def seleccionarTodos(self):
		for i in range(len(self.listaMinisterios)):
			self.ui.tableWidget.item(i,0).setCheckState(QtCore.Qt.Checked)

	def desseleccionarTodos(self):
		for i in range(len(self.listaMinisterios)):
			self.ui.tableWidget.item(i,0).setCheckState(QtCore.Qt.Unchecked)





	#rellenar tabla con ministerios y checkbox

	#obtener ministerios con checkboxes
