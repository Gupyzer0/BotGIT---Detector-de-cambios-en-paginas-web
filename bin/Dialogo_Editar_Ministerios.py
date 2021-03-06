#Widget para filtrar los portales vistos por ministerio
import sys, re, logging
sys.path.append("../interfaz")

from PyQt4 import QtCore, QtGui, QtSql
from qt4BaseDatos import db
from Ui_Dialogo_Editar_Ministerios import Ui_Dialogo_Editar_Ministerios

regexTextoNumeros = re.compile('^[a-zA-Z0-9áéíóú _.-]*$')
regexPaginaWeb = re.compile('(http|https|ftp|file):\/\/\S+')

class Dialogo_Editar_Ministerios(QtGui.QWidget):
	def __init__(self):
		super(Dialogo_Editar_Ministerios, self).__init__()

		self.msgBox = QtGui.QMessageBox()
		self.msgBox.setModal(True)
		self.dialogo = QtGui.QDialog()
		self.dialogo.setAttribute(QtCore.Qt.WA_DeleteOnClose)

		self.ui = Ui_Dialogo_Editar_Ministerios(self.dialogo)
		
		self.modeloBaseDatos = QtSql.QSqlTableModel(self, db)
		self.modeloBaseDatos.setTable("ministerios")
		self.modeloBaseDatos.select()
		self.modeloBaseDatos.setHeaderData(0, QtCore.Qt.Horizontal, "Ministerios")

		self.filtro = QtGui.QSortFilterProxyModel()
		self.filtro.setSourceModel(self.modeloBaseDatos)
		self.filtro.setFilterKeyColumn(1)

		self.ui.tableView.setModel(self.filtro)
		self.ui.tableView.hideColumn(0)
		self.ui.tableView.show()

		self.ui.pushButton.clicked.connect(self.eliminarMinisterios)
		self.ui.pushButton_2.clicked.connect(self.agregarMinisterio)

		self.ui.lineEdit.textChanged.connect(self.filtro.setFilterRegExp)
		self.modeloBaseDatos.beforeInsert.connect(self.verificarData)
		self.modeloBaseDatos.beforeUpdate.connect(self.verificarData)
		
	def agregarMinisterio(self):
		print("funcion agregar ministerio")
		nombre, ok = QtGui.QInputDialog.getText(self, 'Agregar Ministerio', 'Ingrese el nombre del ministerio a agregar.')

		if ok:
			if len(nombre) > 0:
				print("ingresando ministerio")
				nuevoRegistro = self.modeloBaseDatos.record()
				nuevoRegistro.remove(0) #Por que idministerio ya tiene autoincrement
				nuevoRegistro.setValue("nombre",nombre)

				if (self.modeloBaseDatos.insertRecord(-1,nuevoRegistro)):
					logging.info("Ministerio agregado agregado")
				else:
					logging.info("Ministerio no agregado")
					self.msgBox.setWindowTitle('Error')
					self.msgBox.setText('El ministerio no fué agregado, verifique la conexión con la base de datos.')
					self.msgBox.setIcon(QtGui.QMessageBox.Critical)
					self.msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
					self.msgBox.exec()
			else:
				self.msgBox.setWindowTitle('Error')
				self.msgBox.setText('El nombre del ministerio no puede quedar en blanco.')
				self.msgBox.setIcon(QtGui.QMessageBox.Critical)
				self.msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
				self.msgBox.exec()

	def eliminarMinisterios(self):
		filas = self.ui.tableView.selectionModel().selectedIndexes()
		numeroFilas = str(len(filas))
		
		self.msgBox.setWindowTitle('Eliminar Ministerios')
		self.msgBox.setText('¿Está seguro que desea eliminar ' + numeroFilas + ' ministerios?')
		self.msgBox.setIcon(QtGui.QMessageBox.Warning)
		self.msgBox.setStandardButtons(QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok )
		respuesta = self.msgBox.exec_()

		if respuesta == QtGui.QMessageBox.Ok:
						
			logging.info('Eliminando ' + numeroFilas + ' ministerios.')			
			
			filas = sorted(filas)
			filas = filas[::-1] #en reverso para que elimine de atrás hacia delante
			for idx in filas:
				index = self.filtro.mapToSource(idx) #para obtener el index del modelo y no del modelo filtrado
				self.modeloBaseDatos.removeRows(index.row(),1)

	#Si se intenta ingresar un valor nulo ... este motrará ***VALOR NULO*** al mas puro estilo de excel =)
	def verificarData(self,fila,record):

		if record.isNull('nombre') or record.value(1) == '':
			record.setValue(1,'**** VALOR NULO ***')
			
			self.msgBox.setWindowTitle('Valor nulo ingresado')
			self.msgBox.setText('Usted ingresó un nombre nulo en la fila ' + str(fila) + ', corrija si es necesario')
			self.msgBox.setIcon(QtGui.QMessageBox.Warning)
			self.msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
			self.msgBox.exec()
