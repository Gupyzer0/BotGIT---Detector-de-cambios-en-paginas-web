from PyQt4 import QtCore, QtGui

try:
	_fromUtf8 = QtCore.QString._fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

class Widget_Caja(QtGui.QWidget):
	def __init__(self, parent):
		super(Widget_Caja, self).__init__(parent)

		self.groupBox = QtGui.QGroupBox(self)
		self.groupBox.setMaximumSize(QtCore.QSize(16777215, 65))
		self.groupBox.setMinimumSize(QtCore.QSize(450, 70))
		self.groupBox.setCheckable(True)

		self.layout = QtGui.QGridLayout(self)
		self.layout.setContentsMargins (0,0,0,0)
		self.layout.addWidget(self.groupBox)

		self.layoutInterno = QtGui.QGridLayout(self.groupBox)
		self.groupBox2 = QtGui.QGroupBox(self.groupBox)
		self.groupBox2.setMinimumSize(QtCore.QSize(100, 50))
		self.layoutInterno2 = QtGui.QGridLayout(self.groupBox2)
		self.layoutInterno2.setVerticalSpacing(1)
		self.layoutInterno2.setContentsMargins (0,0,0,0)

		self.btn_mostrar = QtGui.QPushButton()
		self.btn_mostrar.setMinimumHeight(25)
		self.btn_mostrar.setMaximumWidth(35)
		iconoMostrar = QtGui.QIcon()
		iconoMostrar.addPixmap(QtGui.QPixmap(_fromUtf8("../interfaz/imagenes/mostrar.png")), QtGui.QIcon.Selected, QtGui.QIcon.On)
		self.btn_mostrar.setIcon(iconoMostrar)
		#self.btn_mostrar.setText(_translate("MainWindow", "Mostrar", None))

		self.btn_compararYa = QtGui.QPushButton()
		self.btn_compararYa.setMinimumHeight(25)
		self.btn_compararYa.setMaximumWidth(35)
		iconoComparar = QtGui.QIcon()
		iconoComparar.addPixmap(QtGui.QPixmap(_fromUtf8("../interfaz/imagenes/comparar.png")), QtGui.QIcon.Selected, QtGui.QIcon.On)
		self.btn_compararYa.setIcon(iconoComparar)		
		#self.btn_compararYa.setText(_translate("MainWindow", "Comparar Ya", None))

		self.btn_reIndexar = QtGui.QPushButton()
		self.btn_reIndexar.setMinimumHeight(25)
		self.btn_reIndexar.setMaximumWidth(35)
		iconoSpider = QtGui.QIcon()
		iconoSpider.addPixmap(QtGui.QPixmap(_fromUtf8("../interfaz/imagenes/spider.png")), QtGui.QIcon.Selected, QtGui.QIcon.On)
		self.btn_reIndexar.setIcon(iconoSpider)		
		#self.btn_reIndexar.setText(_translate("MainWindow", "Spider", None))

		self.btn_modificar = QtGui.QPushButton()
		self.btn_modificar.setMinimumHeight(25)
		self.btn_modificar.setMaximumWidth(35)
		iconoModificar = QtGui.QIcon()
		iconoModificar.addPixmap(QtGui.QPixmap(_fromUtf8("../interfaz/imagenes/modificar.png")), QtGui.QIcon.Selected, QtGui.QIcon.On)
		self.btn_modificar.setIcon(iconoModificar)
		#self.btn_modificar.setText(_translate("MainWindow", "M", None))  

		self.btn_eliminar = QtGui.QPushButton()
		self.btn_eliminar.setMinimumHeight(25)
		self.btn_eliminar.setMaximumWidth(35)
		iconoEliminar = QtGui.QIcon()
		iconoEliminar.addPixmap(QtGui.QPixmap(_fromUtf8("../interfaz/imagenes/eliminar.png")), QtGui.QIcon.Selected, QtGui.QIcon.On)
		self.btn_eliminar.setIcon(iconoEliminar)		
		#self.btn_eliminar.setText(_translate("MainWindow", "X", None))     

		self.dial_porcentaje = QtGui.QDial()
		self.dial_porcentaje.setNotchesVisible(True)
		self.dial_porcentaje.setMaximum(1000)
		self.dial_porcentaje.setMinimum(0)
		self.dial_porcentaje.setSingleStep(20)
		self.dial_porcentaje.setPageStep(1)
		self.dial_porcentaje.setMaximumHeight(35)
		self.dial_porcentaje.setMinimumHeight(35)
		self.dial_porcentaje.setMaximumWidth(50)
		self.dial_porcentaje.setTracking(False)#Solo emitir signal cuando se detenga el dial
		
		self.texto_porcentaje = QtGui.QLabel()

		self.descripcion_dial_porcentaje = QtGui.QLabel("porcentaje\nde deteccion")
		self.descripcion_porcentaje_cambio_promedio = QtGui.QLabel("Promedio de\n cambio")

		self.texto_porcentaje_cambio_promedio = QtGui.QLabel()

		self.btn_actualizar_porcentaje_portal = QtGui.QPushButton()
		self.btn_actualizar_porcentaje_portal.setMinimumHeight(25)
		self.btn_actualizar_porcentaje_portal.setMaximumWidth(100)
		self.btn_actualizar_porcentaje_portal.setText(_translate("MainWindow", "ACT. INDICE", None))

		self.layoutInterno.addWidget(self.btn_mostrar,0,0)
		self.layoutInterno.addWidget(self.btn_compararYa,0,1)
		self.layoutInterno.addWidget(self.btn_reIndexar,0,2)
		self.layoutInterno.addWidget(self.btn_modificar,0,3)
		self.layoutInterno.addWidget(self.btn_eliminar,0,4)
		
		self.layoutInterno.addWidget(self.groupBox2,0,5)
		#----------------Layout interno de los comboBox----------------------
		self.layoutInterno2.addWidget(self.descripcion_dial_porcentaje,0,0)
		self.layoutInterno2.addWidget(self.dial_porcentaje,0,1)
		self.layoutInterno2.addWidget(self.texto_porcentaje,0,2)
		#--------------------------------------------------------------------
		self.layoutInterno.addWidget(self.descripcion_porcentaje_cambio_promedio,0,6)
		self.layoutInterno.addWidget(self.texto_porcentaje_cambio_promedio,0,7)
		self.layoutInterno.addWidget(self.btn_actualizar_porcentaje_portal,0,8)
