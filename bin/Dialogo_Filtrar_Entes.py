#Widget para filtrar los portales vistos por ministerio
import sys, re, logging
sys.path.append("../interfaz")
sys.path.append("../bdatos")

from PyQt4 import QtCore, QtGui, Qt, QtSql
from qt4BaseDatos import db
from Ui_Dialogo_Filtrar_Entes import Ui_Dialogo_Filtrar_Entes

regexTextoNumeros = re.compile('^[a-zA-Z0-9áéíóú _.-]*$')
regexPaginaWeb = re.compile('(http|https|ftp|file):\/\/\S+')

class Dialogo_Filtrar_Entes(QtGui.QWidget):
	def __init__(self):
		super(Dialogo_Filtrar_Entes, self).__init__()
		self.dialogo = QtGui.QDialog()
		self.dialogo.setModal(True)
		self.dialogo.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		
		self.ui = Ui_Dialogo_Filtrar_Entes(self.dialogo)
		self.modeloBaseDatos = QtSql.QSqlRelationalTableModel(self, db)
		self.modeloBaseDatos.setTable("entes")
		self.modeloBaseDatos.setEditStrategy(QtSql.QSqlRelationalTableModel.OnFieldChange)
		#la segunda columna de entes es una clave foranea, especificamente idminsiterio de la tabla minsiterios y queremos
		#colocar en este modelo la columna nombre de esa tabla
		self.modeloBaseDatos.setRelation(2, QtSql.QSqlRelation('ministerios','idministerio','nombre'))
		self.modeloBaseDatos.select()

		#Creando el modelo para filtrar data
		self.filtro = QtGui.QSortFilterProxyModel()
		self.filtro.setSourceModel(self.modeloBaseDatos)
		self.filtro.setFilterKeyColumn(1)
		#Se coloca el modelo del proxy en lugar del modelo de base de datos
		self.ui.tableView.setModel(self.filtro)
		self.ui.tableView.hideColumn(0)
		self.ui.tableView.hideColumn(2)
		self.ui.tableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.ui.tableView))
		self.ui.tableView.setSortingEnabled(True)

		self.listaEntesFiltrados = []#self.ui.tableView.selectionModel().selectedIndexes()
		
		#print(self.listaEntesFiltrados)
		#print("numero = " + str(self.filtro.rowCount()))
		for n in range(self.filtro.rowCount()):
			index = self.filtro.index(n,1)
			self.listaEntesFiltrados.append(str(self.filtro.data(index)))
					
		self.ui.lineEdit.textChanged.connect(self.filtro.setFilterWildcard)
		self.ui.lineEdit.textChanged.connect(self.filtrarLista)
		self.ui.comboBox.currentIndexChanged.connect(self.cambiarFiltro)

		#self.dialogo.show()

	def cambiarFiltro(self, valorComboBox):
		self.ui.lineEdit.textChanged.disconnect()
		
		#0 == Wildcard - 1 == regex
		if valorComboBox == 0:
			print("wildcard")
			self.ui.lineEdit.textChanged.connect(self.filtro.setFilterWildcard)
		else:
			print('regex')
			self.ui.lineEdit.textChanged.connect(self.filtro.setFilterRegExp)

	def filtrarLista(self):
		self.listaEntesFiltrados = []
		for n in range(self.filtro.rowCount()):
			index = self.filtro.index(n,1)
			self.listaEntesFiltrados.append(str(self.filtro.data(index)))
