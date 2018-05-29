#Widget para filtrar los portales vistos por entes
import sys, re, logging, functools
sys.path.append("../interfaz")

from PyQt4 import QtCore, QtGui, QtSql
from qt4BaseDatos import baseDatos
from qt4BaseDatos import db
from Dialogo_Agregar_Entes import Dialogo_Agregar_Entes
from Ui_Dialogo_Editar_Entes import Ui_Dialogo_Editar_Entes #usa las misma interfaz que la edicion de ministerios


regexTextoNumeros = re.compile('^[a-zA-Z0-9áéíóú _.-]*$')
regexPaginaWeb = re.compile('(http|https|ftp|file):\/\/\S+')

class FlipProxyDelegate(QtSql.QSqlRelationalDelegate):
	def createEditor(self, parent, option, index):
		proxy = index.model()
		base_index = proxy.mapToSource(index)
		return super(FlipProxyDelegate, self).createEditor(parent, option, base_index)

	def setEditorData(self, editor, index):
		proxy = index.model()
		base_index = proxy.mapToSource(index)
		return super(FlipProxyDelegate, self).setEditorData(editor, base_index)

	def setModelData(self, editor, model, index):
		base_model = model.sourceModel()
		base_index = model.mapToSource(index)
		return super(FlipProxyDelegate, self).setModelData(editor, base_model, base_index)

class Dialogo_Editar_Entes(QtGui.QWidget):
	def __init__(self):
		super(Dialogo_Editar_Entes, self).__init__()

		self.msgBox = QtGui.QMessageBox()
		self.msgBox.setModal(True)
		self.dialogo = QtGui.QDialog()
		self.dialogo.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.dialogo.setModal(True)

		self.ui = Ui_Dialogo_Editar_Entes(self.dialogo)
		
		self.modeloBaseDatos = QtSql.QSqlRelationalTableModel(self, db)
		self.modeloBaseDatos.setTable("entes")
		self.modeloBaseDatos.setEditStrategy(QtSql.QSqlRelationalTableModel.OnFieldChange)
		#la segunda columna de entes es una clave foranea, especificamente idminsiterio de la tabla minsiterios y queremos
		#colocar en este modelo la columna nombre de esa tabla
		self.modeloBaseDatos.setRelation(2, QtSql.QSqlRelation('ministerios','idministerio','nombre'))
		self.modeloBaseDatos.select()
		self.modeloBaseDatos.setHeaderData(1, QtCore.Qt.Horizontal, "Nombre del ente")
		self.modeloBaseDatos.setHeaderData(2, QtCore.Qt.Horizontal, "Ministerio del ente")
		#Creando el modelo para filtrar data
		self.filtro = QtGui.QSortFilterProxyModel()
		self.filtro.setSourceModel(self.modeloBaseDatos)
		self.filtro.setFilterKeyColumn(1)
		#Se coloca el modelo del proxy en lugar del modelo de base de datos
		self.ui.tableView.setModel(self.filtro)
		self.ui.tableView.hideColumn(0)
		#self.ui.tableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.ui.tableView))
		self.ui.tableView.setItemDelegate(FlipProxyDelegate(self.ui.tableView))
		self.ui.tableView.setColumnWidth(1,300)
		self.ui.tableView.show()

		self.ui.pushButton.clicked.connect(self.eliminarEntes)
		self.ui.pushButton_2.clicked.connect(self.agregarEnte)
		self.ui.lineEdit.textChanged.connect(self.filtro.setFilterRegExp)
		
	def agregarEnte(self):
		dialogoAgregarEntes = Dialogo_Agregar_Entes()
		respuestaDialogo = dialogoAgregarEntes.dialogo.exec_()
		
		if respuestaDialogo:
			ministerio = dialogoAgregarEntes.ministerio
			idMinisterio = baseDatos.seleccionar_id_ministerio(ministerio)
			ente = dialogoAgregarEntes.ente

			if ente:

				print("nombre del ente : " + ente)
				print("nombre del ministerio : " + ministerio)

				fila = self.modeloBaseDatos.rowCount()
				self.modeloBaseDatos.insertRows(fila,1)
				self.modeloBaseDatos.setData(self.modeloBaseDatos.index(fila,1),ente)
				#A pesar de lo que es intuitivo ... es necesario buscar el ID del ministerio. El delegate no funciona con el nombre
				#http://www.qtcentre.org/threads/7215-Editing-QSqlRelationalTableModel-but-not-through-the-usual-way
				self.modeloBaseDatos.setData(self.modeloBaseDatos.index(fila,2),idMinisterio)
				if self.modeloBaseDatos.submitAll():
					logging.info("Ente agregado")
				else:
					logging.warning("Ente no agregado")
					self.msgBox.setWindowTitle('Error')
					self.msgBox.setText('El Ente no fué agregado, verifique la conexión con la base de datos.')
					self.msgBox.setIcon(QtGui.QMessageBox.Critical)
					self.msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
					self.msgBox.exec()
			else:
				self.msgBox.setWindowTitle('Error')
				self.msgBox.setText('El nombre del Ente no puede quedar en blanco.')
				self.msgBox.setIcon(QtGui.QMessageBox.Critical)
				self.msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
				self.msgBox.exec()

	def eliminarEntes(self):
		filas = self.ui.tableView.selectionModel().selectedIndexes()
		numeroFilas = str(len(filas))
		
		self.msgBox.setWindowTitle('Eliminar Entes')
		self.msgBox.setText('¿Está seguro que desea eliminar ' + numeroFilas + ' entes?')
		self.msgBox.setIcon(QtGui.QMessageBox.Warning)
		self.msgBox.setStandardButtons(QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok )
		respuesta = self.msgBox.exec_()

		if respuesta == QtGui.QMessageBox.Ok:
			logging.info('Eliminando ' + numeroFilas + ' entes.')
			
			filas = sorted(filas)
			filas = filas[::-1] #en reverso para que elimine de atrás hacia delante
			for idx in filas:
				index = self.filtro.mapToSource(idx) #para obtener el index del modelo y no del modelo filtrado
				self.modeloBaseDatos.removeRows(index.row(),1)
