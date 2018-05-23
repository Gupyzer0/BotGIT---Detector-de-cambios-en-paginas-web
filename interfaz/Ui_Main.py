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

class Ui_Main(QtGui.QMainWindow):
	def setupUi(self, MainWindow):
		super(Ui_Main, self).__init__()
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.setMaximumWidth(1440)
		MainWindow.setMinimumWidth(1200)
		MainWindow.resize(1440, 600)

		#widget central------------------------------------------------------------------------
		#self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		#self.centralwidget.resize(0,0)
		self.centrallayout = QtGui.QGridLayout(self.centralwidget)
		self.centrallayout.setObjectName(_fromUtf8("centrallayout"))

		#Widget Comaparador--------------------------------------------------------------------
		self.widgetComparador = QtGui.QWidget(self.centralwidget)
		self.widgetComparador.setObjectName(_fromUtf8("widgetComparador"))
		self.centrallayout.addWidget(self.widgetComparador)
		self.layoutWidgetComparador = QtGui.QGridLayout(self.widgetComparador)
		self.layoutWidgetComparador.setObjectName(_fromUtf8("layoutWidgetComparador"))

		#Area de scrolling, para poder anadir layout donde van los widgets de "cajas"
		#self.scrollArea = QtGui.QScrollArea(self.widgetComparador)
		self.scrollArea = QtGui.QScrollArea(self.widgetComparador)
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
		self.scrollAreaWidgetContents = QtGui.QWidget()
		self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 382, 290))
		self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
		self.scrollArea.setWidget(self.scrollAreaWidgetContents)
		self.layoutWidgetComparador.addWidget(self.scrollArea, 1,0)

		#layout donde van los widgets de caja (los que contienen botones para cada ente)
		self.layoutScrollArea = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
		self.layoutScrollArea.setContentsMargins(1,1,1,1)
		self.layoutScrollArea.setSpacing(1)
		
		#Layout grupo de botones superior izquierda
		
		self.grupo_botones = QtGui.QHBoxLayout()
		
	
		#Boton Seleccionar todos
		self.btn_seleccionar_todos = QtGui.QPushButton()
		self.btn_seleccionar_todos.setMinimumHeight(28)
		self.btn_seleccionar_todos.setText(_translate("MainWindow", "Sel.Todos", None))
		self.grupo_botones.addWidget(self.btn_seleccionar_todos)		

		#Boton Comparacion General
		self.btn_comparacion_seleccion = QtGui.QPushButton()
		self.btn_comparacion_seleccion.setMinimumHeight(28)
		self.btn_comparacion_seleccion.setText(_translate("MainWindow", "Comparar", None))
		self.grupo_botones.addWidget(self.btn_comparacion_seleccion)

		#Boton Monitoreo
		self.btn_monitoreo_seleccion = QtGui.QPushButton()
		self.btn_monitoreo_seleccion.setMinimumHeight(28)
		self.btn_monitoreo_seleccion.setText(_translate("MainWindow", "Monitorear", None))
		self.grupo_botones.addWidget(self.btn_monitoreo_seleccion)

		#Boton detener Monitoreo
		self.btn_monitoreo_detener = QtGui.QPushButton()
		self.btn_monitoreo_detener.setMinimumHeight(28)
		self.btn_monitoreo_detener.setText(_translate("MainWindow", "Det.Monitor", None))
		self.grupo_botones.addWidget(self.btn_monitoreo_detener)

		#Boton Araña
		self.btn_araña = QtGui.QPushButton()
		self.btn_araña.setMinimumHeight(28)
		self.btn_araña.setText(_translate("MainWindow", "Crawl Selec.", None))
		self.grupo_botones.addWidget(self.btn_araña)

		#Widget para colocar tiempo al monitoreo
		self.widget_tiempo_monitoreo = QtGui.QTimeEdit()
		self.widget_tiempo_monitoreo.setDisplayFormat("hh:mm")
		tiempoMinimo = QtCore.QTime(0,5)#HH:mm
		self.widget_tiempo_monitoreo.setMinimumTime(tiempoMinimo)
		self.grupo_botones.addWidget(self.widget_tiempo_monitoreo)

		#Boton ordenar por nombre
		self.btn_ordenar_nombre = QtGui.QPushButton()
		self.btn_ordenar_nombre.setMinimumHeight(28)
		#self.btn_ordenar_nombre.setText(_translate("MainWindow", "Ordenar", None))
		iconoOrdenar = QtGui.QIcon()
		iconoOrdenar.addPixmap(QtGui.QPixmap(_fromUtf8("../interfaz/imagenes/A-Z.GIF")), QtGui.QIcon.Selected, QtGui.QIcon.On)
		self.btn_ordenar_nombre.setIcon(iconoOrdenar)
		self.grupo_botones.addWidget(self.btn_ordenar_nombre)

		#Boton ordenar por estatus
		self.btn_ordenar_estatus = QtGui.QPushButton()
		self.btn_ordenar_estatus.setMinimumHeight(28)
		#self.btn_ordenar_nombre.setText(_translate("MainWindow", "Ordenar", None))
		#iconoOrdenar = QtGui.QIcon()
		#iconoOrdenar.addPixmap(QtGui.QPixmap(_fromUtf8("../interfaz/imagenes/A-Z.GIF")), QtGui.QIcon.Selected, QtGui.QIcon.On)
		#self.btn_ordenar_nombre.setIcon(iconoOrdenar)
		self.btn_ordenar_estatus.setText(_translate("MainWindow", "Ord. Estatus", None))
		self.grupo_botones.addWidget(self.btn_ordenar_estatus)

		self.btn_add_caja = QtGui.QPushButton()
		self.btn_add_caja.setMinimumHeight(28)
		self.btn_add_caja.setText(_translate("Add_cajas", "+", None))
		self.grupo_botones.addWidget(self.btn_add_caja)

		#---------------------------------------

		#Tabla con las direcciones y estatus de comparacion
		self.tableWidget = QtGui.QTableWidget(self.widgetComparador)
		#self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		self.tableWidget.setMinimumWidth(690)
		self.tableWidget.setMinimumHeight(400)
		self.tableWidget.setColumnCount(5)
		self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
		self.tableWidget.setRowCount(0)
		self.tableWidget.setHorizontalHeaderLabels(_fromUtf8("URL;Direccion Archivo;Det. Cambio;Ult. Cambio;Diff").split(";"))
		self.tableWidget.horizontalHeader().setVisible(True)
		self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
		self.tableWidget.horizontalHeader().setMinimumSectionSize(27)
		self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
		self.tableWidget.horizontalHeader().setStretchLastSection(True)
		self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
		self.tableWidget.verticalHeader().setSortIndicatorShown(False)
		self.tableWidget.verticalHeader().setStretchLastSection(False)
		self.tableWidget.setColumnWidth(0,330)
		self.tableWidget.setColumnWidth(1,100)
		self.tableWidget.setColumnWidth(2,90)
		self.tableWidget.setColumnWidth(3,90)
		#self.tableWidget.setColumnWidth(4,60)
		self.layoutWidgetComparador.addWidget(self.tableWidget,1,1,1,1)

		#layout botones superior derecha
		self.grupo_botones_derecha = QtGui.QHBoxLayout()

		#Label Caja Seleccioanda
		self.label_caja_seleccioanda = QtGui.QLabel()
		self.label_caja_seleccioanda.setText('Caja Seleccionada:')
		self.grupo_botones_derecha.addWidget(self.label_caja_seleccioanda)

		#Boton añadir pagina
		self.btn_añadir_paginas = QtGui.QPushButton()
		self.btn_añadir_paginas.setMaximumWidth(50)
		self.btn_añadir_paginas.setMinimumWidth(50)
		self.btn_añadir_paginas.setMinimumHeight(28)
		self.btn_añadir_paginas.setText(_translate("MainWindow", "+", None))
		self.grupo_botones_derecha.addWidget(self.btn_añadir_paginas)

		#Boton eliminar paginas
		self.btn_eliminar_paginas = QtGui.QPushButton()
		self.btn_eliminar_paginas.setMaximumWidth(50)
		self.btn_eliminar_paginas.setMinimumWidth(50)
		self.btn_eliminar_paginas.setMinimumHeight(28)
		self.btn_eliminar_paginas.setText(_translate("MainWindow", '-', None))
		self.grupo_botones_derecha.addWidget(self.btn_eliminar_paginas)

		#consola de texto con el "log" de actividades
		self.consola = QtGui.QTextEdit()
		self.consola.setReadOnly(True)
		self.consola.setMaximumHeight(250)
		self.consola.setMinimumHeight(100)
		self.layoutWidgetComparador.addWidget(self.consola,3,0,2,0)

		self.layoutWidgetComparador.addLayout(self.grupo_botones,0,0)
		self.layoutWidgetComparador.addLayout(self.grupo_botones_derecha,0,1)

		MainWindow.setCentralWidget(self.centralwidget)


		#Barra inferior de estatus --------------------------------
		self.statusbar = QtGui.QStatusBar()
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)

		#Barra de menu --------------------------------------------
		self.menubar = QtGui.QMenuBar(MainWindow)		
		
		#SubMenu opciones
		self.menuOpciones 		= self.menubar.addMenu('&Opciones')
		self.menuEstadisticas 	= self.menubar.addMenu('&Estadísticas')
		self.menuAyuda			= self.menubar.addMenu('&Ayuda')

		MainWindow.setMenuBar(self.menubar)
		
		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("BotGit", "BotGit", None))	
		#self.menuOpciones.setTitle(_translate("MainWindow", "Opciones", None))
		#self.actionCambiar_Timeout.setText(_translate("MainWindow", "Cambiar Timeout", None))

