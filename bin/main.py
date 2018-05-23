#!/usr/bin/python3

"""
BotGIT!
"""

import os, sys, threading, requests, hashlib, pprint, pyperclip, webbrowser, functools, re, logging, traceback, difflib, hashlib,time,sip,datetime,opciones
sys.path.append("../interfaz")
sys.path.append("../bdatos")

#Qt4
from PyQt4 import Qt
from PyQt4       import QtCore,QtGui, QtSql
from PyQt4.QtCore import QThreadPool
#Obj
from Crawler import Crawler,Araña
from almacenador import Almacenador
from caja        import Caja
#Ui's
from Ui_Main  import Ui_Main
from Ui_Dialogo_Diff import Ui_Dialogo_Diff
from Ui_Dialogo_Add_Pagina import Ui_Dialogo_Add_Pagina
#Dialogos - SubClassing de QWidget
from Dialogo_Add_Pagina 			import Dialogo_Add_Pagina
from Dialogo_Add_Portal 			import Dialogo_Add_Portal
from Dialogo_Editar_Ministerios 	import Dialogo_Editar_Ministerios
from Dialogo_Editar_Entes 			import Dialogo_Editar_Entes
from Dialogo_Filtrar_Ministerios 	import Dialogo_Filtrar_Ministerios
from Dialogo_Filtrar_Entes 			import Dialogo_Filtrar_Entes
from Dialogo_Progreso 				import Dialogo_Progreso
from Dialogo_Palabras_Clave 		import Dialogo_Palabras_Clave
from Dialogo_Estadisticas_Cambios	import Dialogo_Estadisticas_Cambios
from Dialogo_Editar_Portal			import Dialogo_Editar_Portal

#Base de datos
from qt4BaseDatos import baseDatos
from queue import Queue
#Opciones

#--------------Desactiva el "insecure request warning" de urllib3 incluido en requests --------
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#----------------------------------------------------------------------------------------------

"""
Referencia Stack Overflow: https://stackoverflow.com/questions/31952711/threading-pyqt-crashes-with-unknown-request-in-queue-while-dequeuing

Las funciones X11 para ventanas aparentemento no son seguras al usarse con threads a menos que se les 
diga explicitamente que si lo sean. Por alguna razon PYQT tampoco coloca estas funciones explicitamente,
asi que hay que agregar lo siguiente al constructor de la aplicacion: 
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads)

"""
regexTextoNumeros = re.compile('^[a-zA-Z0-9áéíóú _.-]*$')

regexHttp = re.compile('\d\d\d\Z')
regexErrCon = re.compile('Error de Conexion') 
regexTimeout = re.compile('Timeout')

regexTextoAgregado = re.compile('^\s*\+')
regexTextoEliminado = re.compile('^\s*\-')
regexDiffPedazo = re.compile('@@(.*)@@')
#regexPaginaWeb = re.compile('(http|https|ftp|file):\/\/\S+\.\S+')
regexPaginaWeb = re.compile('(http|https|file):\/\/\S+')

#Señales de los workers
class WorkerSignals(QtCore.QObject):
	finished = QtCore.pyqtSignal()
	error    = QtCore.pyqtSignal(tuple)
	mensaje  = QtCore.pyqtSignal(str)
	progreso = QtCore.pyqtSignal(float)
	paginaLista = QtCore.pyqtSignal(dict)
	resultadoDiccionario = QtCore.pyqtSignal(list)

class WorkerComparador(QtCore.QRunnable):
	def __init__(self, fn, caja):
		super(WorkerComparador,self).__init__()
		self.fn      = fn
		self.caja    = caja
		self.banderaMonitoreo = True
		self.signals = WorkerSignals()

	def run(self):
		try:
			self.signals.mensaje.emit('Iniciando comparacion en: ' + self.caja.portal)
			listaResultado = self.fn(self.caja)
			#self.signals.resultadoDiccionario.emit(listaResultado)
		except:
			traceback.print_exc()
			exctype, value = sys.exc_info()[:2]
			self.signals.error.emit((exctype, value, traceback.format_exc()))
		finally:
			self.signals.finished.emit()

class WorkerMonitorear(QtCore.QRunnable):
	def __init__(self, fn, listaCajas, tiempo):	
		super(WorkerMonitorear,self).__init__()
		self.fn         = fn
		self.listaCajas = listaCajas
		self.tiempo     = tiempo
		self.signals    = WorkerSignals()

	def run(self):
		try:
			#resultado = self.fn(self.listaCajas, self.tiempo)
			self.fn(self.listaCajas, self.tiempo)
		except:
			traceback.print_exc()
			exctype, value = sys.exc_info()[:2]
			self.signals.error.emit((exctype, value, traceback.format_exc()))
		finally:
			self.signals.finished.emit()

class WorkerCrawler(QtCore.QRunnable):
	def __init__(self, opcionesCrawler, listaCajas, funcionAlmacenarBd, funcionEliminarBd):
		super(WorkerCrawler,self).__init__()
		self.opcionesCrawler = opcionesCrawler
		self.listaCajas = listaCajas
		self.almacenarBaseDatos = funcionAlmacenarBd
		self.eliminarUrlsPortal = funcionEliminarBd
		self.signals = WorkerSignals()

	def run(self):
		try:
			progreso = 0

			for i in range(len(self.opcionesCrawler)):
				spider = Araña(self.opcionesCrawler[i]['semilla'],self.opcionesCrawler[i]['profundidad'],5)
				spider.caminar()
				for caja in self.listaCajas:
					self.eliminarUrlsPortal(caja.portal) #Reiniciando portal
					if caja.portal == self.opcionesCrawler[i]['portal']:
						caja.lista = []
						for pagina in spider.arregloLinks:							
							resultadoAlmacenador = Almacenador.guardarPagina(caja.portal, pagina)
							if resultadoAlmacenador['diff'][0]:					
								self.almacenarBaseDatos(caja.portal,pagina,resultadoAlmacenador['direccionArchivo'],resultadoAlmacenador['md5'],resultadoAlmacenador['diff'],resultadoAlmacenador['ultPorcCambio'],0,False,resultadoAlmacenador['estatus'])
								caja.lista.append({'url':pagina, 'md5':resultadoAlmacenador['md5'],'direccionArchivo':resultadoAlmacenador['direccionArchivo'],'diff':resultadoAlmacenador['diff'],'ultPorcCambio':resultadoAlmacenador['ultPorcCambio'], 'porcDetectCambio':0, 'diffAceptado':False, 'estatus': resultadoAlmacenador['estatus']})
							else:
								self.almacenarBaseDatos(caja.portal,pagina,resultadoAlmacenador['direccionArchivo'],resultadoAlmacenador['md5'],resultadoAlmacenador['diff'],resultadoAlmacenador['ultPorcCambio'],0,True,resultadoAlmacenador['estatus'])
								caja.lista.append({'url':pagina, 'md5':resultadoAlmacenador['md5'],'direccionArchivo':resultadoAlmacenador['direccionArchivo'],'diff':resultadoAlmacenador['diff'],'ultPorcCambio':resultadoAlmacenador['ultPorcCambio'], 'porcDetectCambio':0, 'diffAceptado':True, 'estatus': resultadoAlmacenador['estatus']})
							
				self.signals.progreso.emit(progreso)
				progreso = progreso + 1
					
		except:
			traceback.print_exc()
			exctype, value = sys.exc_info()[:2]
			self.signals.error.emit((exctype, value, traceback.format_exc()))
			#logging.debug('--------------Error------------')
		finally:
			#logging.debug("Worker Crawling finalizado")
			self.signals.finished.emit()

class WorkerAddPortal(QtCore.QRunnable):
	def __init__(self, nombrePortal, ente, arrUrls, fnAlmacenador, fnAddPortalBd, fnAddPaginaBd):
		super(WorkerAddPortal,self).__init__()
		self.nombrePortal = nombrePortal
		self.arrUrls = arrUrls
		self.ente = ente
		self.fnAlmacenador = fnAlmacenador
		self.fnAddPortalBd = fnAddPortalBd
		self.fnAddPaginaBd = fnAddPaginaBd
		self.signals = WorkerSignals()

	def run(self):
		try:
			#Usando una nueva conexion a base de datos desde este nuevo thread,
			#es necesario para evitar una falla de segmento. Llamaremos a las funciones de
			#la base de datos pero sobrecargando la conexion a base de datos en uso.

			base_de_datos = "proyectoprueba1"
			hostname      = "localhost"
			usuario       = "root"
			password      = "123456"

			db2 = QtSql.QSqlDatabase.addDatabase("QMYSQL","conexion2")
			db2.setHostName(hostname)
			db2.setDatabaseName(base_de_datos)
			db2.setUserName(usuario)
			db2.setPassword(password)

			bdatos_ok = db2.open()
			if bdatos_ok:
				query = QtSql.QSqlQuery(db2)
				query.exec('SET wait_timeout = 9000')
			else:
				logging.error("Error de conexión a la base de datos.")
				print(query.lastError().text())
				return 0

			resultado = []
			if self.fnAddPortalBd(self.ente,self.nombrePortal,db=db2):

				for url in self.arrUrls:
					pagina = self.fnAlmacenador(self.nombrePortal,str(url))
					#print(pagina)
					self.fnAddPaginaBd(self.nombrePortal,url,pagina['direccionArchivo'],pagina['md5'],pagina['diff'],pagina['ultPorcCambio'],pagina['porcDetectCambio'],pagina['diffAceptado'],pagina['estatus'],db=db2)
					self.signals.paginaLista.emit(pagina)

			else:
				logging.error("Portal no agregado")
				print(query.lastError().text())
				return 0
						
		except:
			traceback.print_exc()
			exctype, value = sys.exc_info()[:2]
			self.signals.error.emit((exctype, value, traceback.format_exc()))
		finally:
			self.signals.finished.emit()

class WorkerAddPaginas(QtCore.QRunnable):
	def __init__(self,caja, arrUrls, fnAlmacenador, fnBaseDatosAddPagina):
		super(WorkerAddPaginas,self).__init__()
		self.caja = caja
		self.urls = arrUrls
		self.fnAlmacenador = fnAlmacenador
		self.fnBaseDatosAddPagina = fnBaseDatosAddPagina
		self.signals = WorkerSignals()

	def run(self):
		try:
			for url in self.urls:
				#return {'url': url,'direccionArchivo': direccionArchivo,'md5': paginaMd5,'diff': diff, 'ultPorcCambio':ultPorcCambio, 'porcDetectCambio':0, 'diffAceptado':True, 'estatus':estatus}
				pagina = self.fnAlmacenador(self.caja.portal,url)
				#def add_pagina(nombrePortal,url,direccionArchivo,md5,diff,ultPorcCambio,porcDetectCambio,diffAceptado,estatus):
				self.fnBaseDatosAddPagina(self.caja.portal,url,pagina['direccionArchivo'],pagina['md5'],pagina['diff'],pagina['ultPorcCambio'],pagina['porcDetectCambio'],pagina['diffAceptado'],pagina['estatus'] )
				self.caja.lista.append(pagina)

		except:
			traceback.print_exc()
			exctype, value = sys.exc_info()[:2]
			self.signals.error.emit((exctype, value, traceback.format_exc()))
		finally:
			self.signals.finished.emit()

#Para redirigir elementos de salida estandar a la consola -----------------------------------------------------------
#Ingresa elementos al texto de la consola
#https://stackoverflow.com/questions/21071448/redirecting-stdout-and-stderr-to-a-pyqt4-qtextedit-from-a-secondary-thread
class StreamEscritura(object):
	def __init__(self,queue):
		self.queue = queue

	def write(self, text):
		self.queue.put(text)

class Receptor(QtCore.QObject):
	signal = QtCore.pyqtSignal(str)
	def __init__(self, queue, *args,**kwargs):
		QtCore.QObject.__init__(self, *args,**kwargs)
		self.queue = queue
	
	def run(self):
		while True:
			text = self.queue.get()
			self.signal.emit(text)

class VentanaMain(QtGui.QMainWindow):
	def __init__(self, parent = None):
		super(VentanaMain, self).__init__(parent)		
		#Atributos
		
		self.threadpool = QThreadPool()
		#Mantiene una lista de todos las cajas (portales)
		self.listaCajasPermanente = []
		#Mantiene las cajas (portales) en uso al momento
		self.listaCajas = []
		self.listaCajasChequeadas = []
		self.contadorPrueba = 0
		self.cajaActual = ''
		
		#Interfaz grafica
		self.ui = Ui_Main()
		self.ui.setupUi(self)

		#Palabras clave a detectar
		#self.palabras = ['hacked','hackeado','anonymous','vene10', 'Vene 10','kaked','kacked']
		self.palabrasClave = []

		try:
			with open("../bdatos/palabrasClave.txt",'r') as archivoPalabras:
				for palabra in archivoPalabras:
					self.palabrasClave.append(palabra.strip())
		except IOError:
			print("Creando archivo")
			archivoPalabras = open("../bdatos/palabrasClave.txt",'w')

		finally:
			archivoPalabras.close()

		print(self.palabrasClave)

		#Barra de Menu--------------------------------------------------------------------------------------
		#-Acciones
		self.accion_set_timeout = QtGui.QAction("Tiempo de Timeout", self.ui)
		self.accion_set_timeout.setShortcut('Ctrl+Shift+T')
		self.accion_set_timeout.setStatusTip('Cambiar el tiempo de espera para las peticiones.')
		self.accion_set_timeout.setToolTip("Cambiar el tiempo de espera para las peticiones.")
		self.accion_set_timeout.triggered.connect(self.setTimeout)

		self.accion_filtrar_portales_ministerios = QtGui.QAction("Filtrar portales por Ministerio", self.ui)
		self.accion_filtrar_portales_ministerios.setStatusTip("Filtrar portales por Minsiterios")
		self.accion_filtrar_portales_ministerios.setToolTip("Filtrar portales por Ministerios")
		self.accion_filtrar_portales_ministerios.triggered.connect(self.filtrarPortalesPorMinisterios)

		self.accion_editar_ministerios = QtGui.QAction("Editar Ministerios", self.ui)
		self.accion_editar_ministerios.setStatusTip("Editar la lista de ministerios")
		self.accion_editar_ministerios.setToolTip("Editar la lista de ministerios")
		self.accion_editar_ministerios.triggered.connect(self.editarMinisterios)

		self.accion_filtrar_portales_entes = QtGui.QAction("Filtrar portales por entes", self.ui)
		self.accion_filtrar_portales_entes.setStatusTip("Filtrar la lista de entes")
		self.accion_filtrar_portales_entes.setToolTip("Filtrar la lista de entes")
		self.accion_filtrar_portales_entes.triggered.connect(self.filtrarPortalesPorEntes)

		self.accion_editar_entes = QtGui.QAction("Editar Entes", self.ui)
		self.accion_editar_entes.setStatusTip("Editar la lista de Entes")
		self.accion_editar_entes.setToolTip("Editar la lista de Entes")
		self.accion_editar_entes.triggered.connect(self.editarEntes)

		self.accion_editar_palabras_clave = QtGui.QAction("Editar palabras clave",self.ui)
		self.accion_editar_palabras_clave.setStatusTip("Editar la lista de palabras clave a detectar por el comparador")
		self.accion_editar_palabras_clave.setToolTip("Editar la lista de palabras clave a detectar por el comparador")
		self.accion_editar_palabras_clave.triggered.connect(self.editarPalabrasClave)

		self.accion_mostrar_estadisticas_cambios = QtGui.QAction("Cambios detectados",self.ui)
		self.accion_mostrar_estadisticas_cambios.setStatusTip("Mostrar cambios detectados")
		self.accion_mostrar_estadisticas_cambios.setToolTip("Mostrar cambios detectados")
		self.accion_mostrar_estadisticas_cambios.triggered.connect(self.mostrarEstadisticasCambios)

		#-Add acciones
		self.ui.menuOpciones.addAction(self.accion_set_timeout)
		#Ministerios
		self.ui.menuOpciones.addSeparator()
		self.ui.menuOpciones.addAction(self.accion_filtrar_portales_ministerios)
		self.ui.menuOpciones.addAction(self.accion_editar_ministerios)
		#Entes
		self.ui.menuOpciones.addSeparator()
		self.ui.menuOpciones.addAction(self.accion_filtrar_portales_entes)
		self.ui.menuOpciones.addAction(self.accion_editar_entes)
		#palabras clave
		self.ui.menuOpciones.addSeparator()
		self.ui.menuOpciones.addAction(self.accion_editar_palabras_clave)

		self.ui.menuEstadisticas.addAction(self.accion_mostrar_estadisticas_cambios)

		#---------------------------------------------------------------------------------------------------

		#Dialogos reusables
		self.msgBox = QtGui.QMessageBox()
		self.barraProgreso = Dialogo_Progreso()
		#self.barraProgreso.dialogo.hide()
		
		#Conectando botones
		self.ui.btn_seleccionar_todos.clicked.connect(self.boton_seleccionar_todos_clicked)
		self.ui.btn_comparacion_seleccion.clicked.connect(self.boton_comparar_clicked)
		self.ui.btn_monitoreo_seleccion.clicked.connect(self.boton_monitorear_clicked)
		self.ui.btn_monitoreo_detener.clicked.connect(self.boton_monitorear_detener_clicked)
		self.ui.btn_araña.clicked.connect(self.boton_crawl_clicked)
		self.ui.btn_ordenar_nombre.clicked.connect(self.ordenar_lista_cajas)
		self.ui.btn_ordenar_estatus.clicked.connect(self.ordenar_lista_cajas_estatus)
		self.ui.btn_add_caja.clicked.connect(self.agregarCajas)

		#Botones Derecha
		self.ui.btn_añadir_paginas.clicked.connect(self.boton_add_pagina_clicked)
		self.ui.btn_eliminar_paginas.clicked.connect(self.boton_eliminar_paginas_clicked)
		
		#bd = almacenarPaginas()
		
		bd = baseDatos.seleccionar_portales()
		#if not bd: #Base de datos vacia, posible priemr uso o todos los portales están eliminados
		for portal in bd:
			#logging.debug(bd)
			for k,v in portal.items():				
				nombrePortal = str(k)
				logging.debug("cargando el portal " + nombrePortal)
				ente = baseDatos.seleccionar_ente_portal(nombrePortal)
				lista = v
				ministerio = baseDatos.seleccionar_ministerio_portal(nombrePortal)
				#Creando una caja por cada elemento de la lista (por cada portal)
				#caja = Caja(nombrePortal, lista, self)
				caja = Caja(nombrePortal,ente, lista, ministerio, self.ui.scrollAreaWidgetContents)
				#cargando porcentaje de deteccion de diferencias
				porcentaje = baseDatos.seleccionar_porcentaje_diferencia_portal(nombrePortal)
				caja.setPorcDetectarDiferenciaBd(porcentaje)

				#incializando color del texto de la caja
				for elem in caja.lista:					
					#Si el elemento diff contiene informacion al momento de la creacion ... Entonces es un error de conexion
					#print("diff:", str(elem['diff']))
				
					if elem['diff'][0]:
						if elem['ultPorcCambio'] > float(elem['porcDetectCambio']):
							caja.ui.setStyleSheet('QGroupBox{color: red;\nfont: bold;}')
							caja.estatus = "mal"
						
							#regex = re.compile('\d\d\d\Z')
							if regexHttp.match(str(elem['diff'][0])):
								caja.ui.setStyleSheet('QGroupBox{color: #FF8C00;\nfont: bold;}')
							
							#regex = re.compile('Error de Conexion')
							elif regexErrCon.match(str(elem['diff'][0])):
								caja.ui.setStyleSheet('QGroupBox{color: #FF8C00;\nfont: bold;}')
							
							#regex = re.compile('Timeout')
							elif regexTimeout.match(str(elem['diff'][0])):
								caja.ui.setStyleSheet('QGroupBox{color: #FF8C00;\nfont: bold;}')
						if elem['estatus']=='hacked':
							caja.ui.setStyleSheet('QGroupBox{color: magenta;\nfont: bold;}')
								
			#Conectando botones de cada caja a su funcion respectiva
			caja.ui.btn_actualizar_porcentaje_portal.clicked.connect(functools.partial(self.boton_caja_porc_promedio_actual_set,caja))
			caja.ui.btn_compararYa.clicked.connect(functools.partial(self.boton_caja_comparar_clicked, caja))
			caja.ui.btn_mostrar.clicked.connect(functools.partial(self.boton_caja_mostrar_clicked, caja))
			caja.ui.btn_reIndexar.clicked.connect(functools.partial(self.boton_reIndexar_clicked, caja))
			caja.ui.btn_modificar.clicked.connect(functools.partial(self.editarPortal, caja))
			caja.ui.btn_eliminar.clicked.connect(functools.partial(self.eliminarCaja, caja))
			caja.ui.groupBox.update()

			self.addCaja(caja)
			#actualizando interfaz de las cajas
			self.boton_caja_mostrar_clicked(caja)

	#Ordenar cajas por estatus al final ...

	def agregarTextoConsola(self, text):
		self.ui.consola.moveCursor(QtGui.QTextCursor.End)
		self.ui.consola.insertPlainText(text)

	def actualizarStatusBar(self,texto):
		self.ui.statusbar.showMessage(texto)
	
	def addCaja(self, caja):
		self.ui.layoutScrollArea.addWidget(caja.ui)
		self.listaCajas.append(caja)
		self.listaCajasPermanente.append(caja)

	def agregarCajaInterfaz(self,listaAddInterfaz):		
		nombrePortal = listaAddInterfaz[0]
		ente = listaAddInterfaz[1]
		lista = listaAddInterfaz[2]
		ministerio = listaAddInterfaz[3]

		caja = Caja(nombrePortal,ente, lista, ministerio, self)	
		#Conectando botones
		caja.ui.btn_actualizar_porcentaje_portal.clicked.connect(functools.partial(self.boton_caja_porc_promedio_actual_set,caja))
		caja.ui.btn_compararYa.clicked.connect(functools.partial(self.boton_caja_comparar_clicked, caja))
		caja.ui.btn_mostrar.clicked.connect(functools.partial(self.boton_caja_mostrar_clicked, caja))
		caja.ui.btn_reIndexar.clicked.connect(functools.partial(self.boton_reIndexar_clicked, caja))
		caja.ui.btn_eliminar.clicked.connect(functools.partial(self.eliminarCaja, caja))
		caja.ui.groupBox.update()
		self.addCaja(caja)
		self.boton_caja_mostrar_clicked(caja)

	def agregarCajas(self):#Para añadir en duplas de *portal - url| lista = {'nombrePortal':['semilla','dir2','dir_n']}*
		#TODO: iniciar interfaz para añadir cajas
		addCajaDialogo = Dialogo_Add_Portal()

		respuestaDialogo = addCajaDialogo.dialogo.exec_()

		if addCajaDialogo.valido & respuestaDialogo:
		
			ente = addCajaDialogo.ente
			listaPortal = addCajaDialogo.lista
			nombrePortal = addCajaDialogo.portal
			ministerio = addCajaDialogo.ministerio
			listaPaginas = []
			lista = []
			
			self.barraProgreso.ui.progressBar.setRange(0,0)
			self.barraProgreso.ui.label.setText("Agregando Portal, por favor espere...")
			self.barraProgreso.dialogo.show()

			listaAddInterfaz = [nombrePortal,ente, lista, ministerio]

			worker = WorkerAddPortal(nombrePortal,ente,listaPortal,Almacenador.guardarPagina,baseDatos.add_portal,baseDatos.add_pagina)
			worker.signals.finished.connect(functools.partial(self.barraProgreso.dialogo.hide))
			worker.signals.finished.connect(functools.partial(self.agregarCajaInterfaz, listaAddInterfaz))
			worker.signals.paginaLista.connect(lista.append)
			self.threadpool.start(worker)

		elif respuestaDialogo == QtGui.QDialog.Rejected:
			pass

		else:
			logging.warnign("Error, Una de las opciones era incorrecta, No se agregará el portal")			
			self.msgBox.setWindowTitle('Error')
			self.msgBox.setText('Error: Una de las opciones era incorrecta, No se agregará el portal.')
			self.msgBox.setIcon(QtGui.QMessageBox.Critical)
			self.msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
			self.msgBox.exec()

		#del ente			
				
	def eliminarCaja(self,caja):
		self.msgBox.setWindowTitle('¿Desea eliminar el portal?')
		self.msgBox.setText('¿Está seguro que desea eliminar el portal ' + caja.portal + ' ?')
		self.msgBox.setModal(True)
		self.msgBox.setIcon(QtGui.QMessageBox.Warning)
		self.msgBox.setStandardButtons(QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
		#self.msgBox.setStandardButtons()		
		respuesta = self.msgBox.exec_()

		if respuesta == QtGui.QMessageBox.Ok:
			baseDatos.eliminar_portal(caja.portal)
			if caja == self.cajaActual:
				self.cajaActual = ''
				for i in range(len(caja.lista)):
					self.ui.tableWidget.removeRow(i)
			index = self.listaCajas.index(caja)
			caja.ui.setParent(None)
			del self.listaCajas[index]
			index2 = self.listaCajasPermanente.index(caja)
			del self.listaCajasPermanente[index2]
			logging.info("Portal eliminado.")
		
	def seleccionarCajasTodas(self):
		self.ui.statusbar.showMessage("Listo")
		for caja in self.listaCajas:
			caja.ui.groupBox.setChecked(True)

	def resetear_lista_cajas_chequeadas(self):
		self.listaCajasChequeadas = []

	def ordenar_lista_cajas(self):
		for caja in self.listaCajas:
			caja.ui.setParent(None)

		self.listaCajas.sort(key=lambda x: x.portal)

		for caja in self.listaCajas:
			self.ui.layoutScrollArea.addWidget(caja.ui)

	def ordenar_lista_cajas_estatus(self):
		for caja in self.listaCajas:
			caja.ui.setParent(None)

		self.listaCajas.sort(key=lambda x: x.estatus)

		for caja in self.listaCajas:
			self.ui.layoutScrollArea.addWidget(caja.ui)

	def Comparar(self, caja):
		logging.info("Comparando " + caja.portal)
		for i in range(len(caja.lista)):
			try:
				req = requests.get(caja.lista[i]['url'], verify = False, timeout = opciones.tiempoTimeout)
				req.raise_for_status()

			except requests.exceptions.HTTPError as error:
				logging.warning("Error de conexión")
				print("Error: \n" + str(error))
				caja.lista[i]['diff'] = str([req.status_code])
				caja.lista[i]['estatus'] = req.status_code
				caja.lista[i]['md5'] = "Error HTTP"
				caja.lista[i]['ultPorcCambio'] = 100
				
			except requests.exceptions.ConnectionError as error:
				logging.warning("Error de conexión")
				print(str(error))
				caja.lista[i]['diff'] = ['Error de Conexion']
				caja.lista[i]['estatus'] = "Error de Conexion"
				caja.lista[i]['md5'] = 'Error de Conexion'
				caja.lista[i]['ultPorcCambio'] = 100
				
			except requests.exceptions.Timeout as error:
				logging.warning("Error de conexión, tiempo de espera agotado.")
				print("Tiempo de espera agotado: \n" + str(error))
				caja.lista[i]['diff'] = ['Timeout']
				caja.lista[i]['estatus'] = 'Timeout'
				caja.lista[i]['md5'] = 'Timeout'
				caja.lista[i]['ultPorcCambio'] = 100
							
			else:
				caja.lista[i]['diff'] = ['']
				caja.lista[i]['estatus'] = "ok " + str(req.status_code)

				webEnLinea = req.text
				
				md5WebEnLinea = hashlib.md5(webEnLinea.encode('utf-8')).hexdigest()
				
				porcDetectarDiferencia = caja.lista[i]['ultPorcCambio']
				md5webAlmacenada       = caja.lista[i]['md5']
				dirWebAlmacenada       = caja.lista[i]['direccionArchivo']

				if(md5webAlmacenada != md5WebEnLinea):
					
					#Busqueda de palabras clave
					#Sale automaticamente al encontrar una palabra clave
					for palabra in self.palabrasClave:
						if palabra in webEnLinea:
							print("Palabra clave encontrada " + palabra)
							caja.lista[i]['estatus'] = 'hacked' + ' ' + palabra
							break
					
					#Normalizando las direcciones para usar direcciones con '/' en windows de ser necesario
					#---------------------------------------------------
					dirWebAlmacenada = os.path.normcase(dirWebAlmacenada)
					#---------------------------------------------------
					
					archivoAlmacenado = open(dirWebAlmacenada, 'rb')
					listaTextoAlmacenado = archivoAlmacenado.readlines()
					archivoAlmacenado.close()
						
					listaWebEnLinea = webEnLinea.splitlines(keepends = True)

					for j in range(len(listaTextoAlmacenado)):
						listaTextoAlmacenado[j]  = listaTextoAlmacenado[j].decode()

					diff = difflib.unified_diff(listaTextoAlmacenado, listaWebEnLinea)

					listaDiff = []
					for elem in diff:
						listaDiff.append(str(elem))

					porcentajeDiferencia = len(listaDiff) * 100 / len(listaTextoAlmacenado)
					#Definiendo porcentaje del ultimo cambio
					caja.lista[i]['ultPorcCambio'] = porcentajeDiferencia

					#if porcentajeDiferencia >= porcDetectarDiferencia:
					if porcDetectarDiferencia >= float(caja.lista[i]['porcDetectCambio']):
						logging.info("Diferencia detectada en " + caja.lista[i]['url'])

						caja.lista[i]['md5'] = hashlib.md5(req.text.encode('utf-8')).hexdigest()
						caja.lista[i]['diff'] = []
						caja.lista[i]['diff'].append(str(datetime.datetime.now()) + '\n' )
						caja.lista[i]['diff'].extend(listaDiff)

						listaTextoArchivo = req.text.splitlines(keepends = True)
						archivo = open(caja.lista[i]['direccionArchivo'],'wb')
						for linea in listaTextoArchivo:
							linea = linea.encode('utf-8')
							archivo.write(linea)					
							
						archivo.close()
				else:
					caja.lista[i]['ultPorcCambio'] = 0

			finally:
				logging.debug("Comparacion terminada")
			
	def actualizarInterfazCaja(self,caja):
		#print("act int caja")
		cambio = False

		for i in range(len(caja.lista)):
			if caja.lista[i]['diff'][0]:
				if str(caja.lista[i]['estatus'])[0:2] != "ok":
					caja.ui.setStyleSheet('QGroupBox{color: #FF8C00;\nfont: bold;}')
					cambio = True

			if	not caja.lista[i]['diffAceptado']:
				#print("Pasamos pro aca")
				caja.ui.setStyleSheet('QGroupBox{color: red;\nfont: bold;}')
				cambio = True

			if caja.lista[i]['estatus'] == 'hacked':
				print('hackeada')
				caja.ui.setStyleSheet('QGroupBox{color: magenta;\nfont: bold;}')
				caja.ui.texto_porcentaje_cambio_promedio.setStyleSheet('QLabel {color : red; }')
				cambio = True
		
		if caja.porcPromedioCambio > caja.porcDetectarDiferencia:			
			caja.ui.setStyleSheet('QGroupBox{color: red;\nfont: bold;}')
			caja.ui.texto_porcentaje_cambio_promedio.setStyleSheet('QLabel {color : red; }')
			cambio = True
		else:
			caja.ui.texto_porcentaje_cambio_promedio.setStyleSheet('QLabel {color : white; }')

		
	
		#estatus caja
		if not cambio:
			caja.estatus = "ok"
			caja.ui.setStyleSheet('QGroupBox{color: white;\nfont: normal}')
		else:
			caja.estatus = "mal"

	def Monitorear(self, listaCajas, tiempo):
		timer = QtCore.QElapsedTimer()
		timer.start()
		#self.consola.mostrar("Iniciando monitoreo de "+ str(len(listaCajas)) + " portales.")
		#logging.info("Iniciando Monitoreo de " + str(len(listaCajas)) + " portales")
		#print("Iniciando Monitoreo")
		tiempoRestante = tiempo

		for caja in listaCajas:
			#print("Iteracion lista cajas")
			caja.ui.btn_compararYa.setDisabled(1)
			worker = WorkerComparador(self.Comparar,caja)
			if (self.cajaActual == caja):
				worker.signals.finished.connect(functools.partial(self.boton_caja_mostrar_clicked,caja))
			worker.signals.finished.connect(functools.partial(self.handler_funcion_cambiar_estatus_bd,caja.lista))
			worker.signals.finished.connect(functools.partial(self.actualizarInterfazCaja, caja))
			worker.signals.finished.connect(functools.partial(caja.ui.btn_compararYa.setDisabled, 0))
			
			self.threadpool.start(worker)
			
			timer.restart()

		while self.banderaMonitoreo:
			tiempoRestante = tiempo - timer.elapsed()
			time.sleep(1)#evita que el CPU llegue al 100%
			#print(self.banderaMonitoreo)
			if tiempoRestante <= 0:
				#print(tiempoRestante)
				
				for caja in listaCajas:
					#print("Iteracion lista cajas")
					caja.ui.btn_compararYa.setDisabled(1)

					worker = WorkerComparador(self.Comparar,caja)
					if (self.cajaActual == caja):
						worker.signals.finished.connect(functools.partial(self.boton_caja_mostrar_clicked,caja))
					worker.signals.finished.connect(functools.partial(self.handler_funcion_cambiar_estatus_bd,caja.lista))
					worker.signals.finished.connect(functools.partial(self.actualizarInterfazCaja, caja))
					worker.signals.finished.connect(functools.partial(caja.ui.btn_compararYa.setDisabled, 0))
					
					self.threadpool.start(worker)

					timer.restart()
				
		#self.consola.mostrar("Fin del Monitoreo")
		#logging.info("Final del monitoreo")
		#self.signals.finished.emit()

	def Crawl(self, listaSemillas):
		crawler = Crawler(listaSemillas)
		crawler.destroyed.connect(self.resetear_lista_cajas_chequeadas)

		empezarCrawl = crawler.dialogo.exec_()
		
		if empezarCrawl:

			self.barraProgreso.ui.progressBar.setRange(0,len(listaSemillas)-1)
			self.barraProgreso.ui.label.setText("Araña explorando (crawling), por favor espere...")
			self.barraProgreso.dialogo.show()

			worker = WorkerCrawler(crawler.opcionesCrawler, self.listaCajasChequeadas, baseDatos.add_pagina, baseDatos.eliminar_urls_portal)
			
			#worker.signals.progreso.connect(functools.partial(self.boton_caja_comparar_clicked, caja))
			#worker.signals.progreso.connect(functools.partial(self.barraProgreso,))
			worker.signals.progreso.connect(self.barraProgreso.ui.progressBar.setValue)
			worker.signals.finished.connect(self.resetear_lista_cajas_chequeadas)
			worker.signals.finished.connect(self.barraProgreso.dialogo.hide)
			#Esperamos a que terminen todos los threads para iniciar
			#Detener el monitoreo
			self.boton_monitorear_detener_clicked()
			#Esperar a que terminen los threads abiertos
			self.threadpool.waitForDone()
			#Iniciamos el worker
			self.threadpool.start(worker)

	#------Botones Caja --------------------------------------

	def boton_caja_mostrar_clicked(self, caja):
		#print(caja.lista)
		print("boton caja")
		self.cajaActual = caja

		self.ui.label_caja_seleccioanda.setText('Caja Seleccionada: ' + self.cajaActual.portal)

		#logging.debug('caja actual:' + caja.portal)
		#Desconectando slots para evitar una llamada doble a la misma funcion
		try: self.ui.tableWidget.cellDoubleClicked.disconnect()
		#Pasar la excepcion en caso de que no existan slots conectados
		except Exception: pass
		
		try: self.ui.tableWidget.cellClicked.disconnect()
		except Exception: pass

		try:self.ui.tableWidget.cellChanged.disconnect()
		except Exception: pass

		for i in range(len(caja.lista)):
			self.ui.tableWidget.setRowCount(len(caja.lista))
			self.ui.tableWidget.setItem(i,0, QtGui.QTableWidgetItem(caja.lista[i]['url']))
			self.ui.tableWidget.item(i,0).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
			self.ui.tableWidget.setItem(i,1, QtGui.QTableWidgetItem(caja.lista[i]['direccionArchivo']))
			self.ui.tableWidget.item(i,1).setFlags(QtCore.Qt.ItemIsEnabled)
			self.ui.tableWidget.setItem(i,2, QtGui.QTableWidgetItem(str(caja.lista[i]['porcDetectCambio'])))			
			self.ui.tableWidget.setItem(i,3, QtGui.QTableWidgetItem(str(caja.lista[i]['ultPorcCambio'])))
			self.ui.tableWidget.item(i,3).setFlags(QtCore.Qt.ItemIsEnabled)
			#Solo para inicialiar el objeto y luego ...
			self.ui.tableWidget.setItem(i,4, QtGui.QTableWidgetItem())
			self.ui.tableWidget.item(i,4).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
			#Verificar si el diff debe ser mostrado o si es un codigo de error
			#Darle color ... dependiendo de si diff esta o no esta vacio. Ademas de anadir la propiedad para
			#que muestre el diff unificado de existir.
			
			#TODO llamar funcion actualizar interfaz caja
		
		for i in range(len(caja.lista)):
			
			if str(caja.lista[i]['estatus'])[0:2] != "ok":
				if str(caja.lista[i]['estatus'])[:6] == 'hacked':
					self.ui.tableWidget.setItem(i,4, QtGui.QTableWidgetItem(str(caja.lista[i]['estatus'])))
					self.ui.tableWidget.item(i,4).setBackground(QtGui.QColor(244,66,229))
					caja.lista[i]['diffAceptado'] = False
					continue
				self.ui.tableWidget.setItem(i,4, QtGui.QTableWidgetItem(str(caja.lista[i]['estatus'])))
				self.ui.tableWidget.item(i,4).setBackground(QtGui.QColor(255,188,0))
				continue
			else:
				self.ui.tableWidget.item(i,4).setBackground(QtGui.QColor(14,173,0))

			if caja.lista[i]['ultPorcCambio'] > float(caja.lista[i]['porcDetectCambio']):
				caja.lista[i]['diffAceptado'] = False
				self.ui.tableWidget.item(i,4).setBackground(QtGui.QColor(173,0,0))
			elif not caja.lista[i]['diffAceptado']:
				self.ui.tableWidget.item(i,4).setBackground(QtGui.QColor(173,0,0))
			else:
				self.ui.tableWidget.item(i,4).setBackground(QtGui.QColor(14,173,0))			

		self.ui.tableWidget.cellDoubleClicked.connect(lambda fila, columna: self.tabla_dobleClick(fila, columna, caja))
		self.ui.tableWidget.cellClicked.connect(lambda fila, columna: self.tabla_click(fila, columna, caja))
		self.ui.tableWidget.cellChanged.connect(lambda fila, columna: self.setPorcDif(fila, columna, caja))
		self.actualizarInterfazCaja(caja)
		
	def boton_caja_comparar_clicked(self, caja):
		
		#inhabilitando el boton de comparar del widget caja
		caja.ui.btn_compararYa.setDisabled(1)
		#Creamos el worker
		worker = WorkerComparador(self.Comparar,caja)
		#Señales a activarse una vez concluida la labor del worker
		#worker.signals.finished.connect(functools.partial(self.boton_caja_mostrar_clicked, caja))
		worker.signals.mensaje.connect(self.actualizarStatusBar)
		worker.signals.finished.connect(functools.partial(caja.ui.btn_compararYa.setDisabled, 0))
		if (self.cajaActual == caja):
			worker.signals.finished.connect(functools.partial(self.boton_caja_mostrar_clicked,caja))
			worker.signals.finished.connect(functools.partial(baseDatos.cambiar_estatus_paginas, caja.lista))
			worker.signals.finished.connect(functools.partial(self.handler_insertar_cambio_bd, caja.lista))
			worker.signals.finished.connect(caja.setGetPorcPromedioCambio)
		else:
			worker.signals.finished.connect(functools.partial(self.actualizarInterfazCaja,caja))
			worker.signals.finished.connect(functools.partial(baseDatos.cambiar_estatus_paginas, caja.lista))
			worker.signals.finished.connect(caja.setGetPorcPromedioCambio)
		#Ingresamos al worker a la threadpool para su posterior ejecución
		self.threadpool.start(worker)
		#self.progreso

	def boton_reIndexar_clicked(self, caja):
		self.listaCajasChequeadas.append(caja)

		listaSemillas = [{'portal':caja.portal,'semilla':caja.lista[0]['url']} for caja in self.listaCajasChequeadas]

		self.Crawl(listaSemillas)

	def boton_caja_porc_promedio_actual_set(self,caja):
		caja.porc_promedio_actual_set()
		self.actualizarInterfazCaja(caja)

	#------Botones Generales-----------------------------------
	
	def boton_seleccionar_todos_clicked(self):
		self.seleccionarCajasTodas()

	def boton_comparar_clicked(self):
		for caja in self.listaCajas:
			if caja.ui.groupBox.isChecked():
				self.listaCajasChequeadas.append(caja)

		for caja in self.listaCajasChequeadas:
			worker = WorkerComparador(self.Comparar,caja)
			worker.signals.finished.connect(functools.partial(baseDatos.cambiar_estatus_paginas, caja.lista))
			worker.signals.finished.connect(functools.partial(self.handler_insertar_cambio_bd, caja.lista))
			worker.signals.finished.connect(functools.partial(caja.ui.btn_compararYa.setDisabled, 0))
			worker.signals.finished.connect(caja.setGetPorcPromedioCambio)
			
			if (self.cajaActual == caja):
				worker.signals.finished.connect(functools.partial(self.boton_caja_mostrar_clicked,caja))
			else:
				worker.signals.finished.connect(functools.partial(self.actualizarInterfazCaja,caja))

			self.threadpool.start(worker)

		self.listaCajasChequeadas = []

	def boton_monitorear_clicked(self):
		self.ui.btn_monitoreo_seleccion.setDisabled(0)
		self.banderaMonitoreo = True
		
		tiempo = (((self.ui.widget_tiempo_monitoreo.time().hour() * 60) + self.ui.widget_tiempo_monitoreo.time().minute()) * 60000)
		listaCajasMonitorear = []
		self.ui.btn_monitoreo_seleccion.setDisabled(1)
		
		for caja in self.listaCajas:
			if caja.ui.groupBox.isChecked():
				listaCajasMonitorear.append(caja)
				#----- layout izquierdo ---------------
				#Evitar que las cajas sean eliminadas mientras se monitorean
				caja.ui.btn_eliminar.setDisabled(True)
				caja.ui.btn_reIndexar.setDisabled(True)
				#-----botones layout derecha ----------
				self.ui.btn_añadir_paginas.setDisabled(True)
				self.ui.btn_eliminar_paginas.setDisabled(True)

		worker = WorkerMonitorear(self.Monitorear,listaCajasMonitorear, tiempo)
		worker.signals.finished.connect(self.boton_monitorear_enable)		
		worker.signals.finished.connect(functools.partial(self.ui.btn_añadir_paginas.setDisabled, False))
		worker.signals.finished.connect(functools.partial(self.ui.btn_eliminar_paginas.setDisabled, False))

		for caja in listaCajasMonitorear:
			worker.signals.finished.connect(functools.partial(caja.ui.btn_eliminar.setDisabled, False))	
			worker.signals.finished.connect(functools.partial(caja.ui.btn_reIndexar.setDisabled, False))

		self.threadpool.start(worker)
		
		del listaCajasMonitorear

	def boton_monitorear_detener_clicked(self):
		self.banderaMonitoreo = False
		self.boton_monitorear_enable()
		#self.consola.mostrar("Deteniendo el monitoreo ...")
		logging.info("Deteniendo el monitoreo...")

	def boton_monitorear_enable(self):
		self.ui.btn_monitoreo_seleccion.setDisabled(0)
		#for caja in self.listaCajas : caja.ui.btn_compararYa.setDisabled(0)

	def boton_crawl_clicked(self):		
		for caja in self.listaCajas:
			if caja.ui.groupBox.isChecked():
				self.listaCajasChequeadas.append(caja)

		listaSemillas = [{'portal':caja.portal,'semilla':caja.lista[0]['url']} for caja in self.listaCajasChequeadas]

		self.Crawl(listaSemillas)
		
	#------Layout Derecha-------------------------------------

	def boton_add_pagina_clicked(self):
		#Matar dialogos al final ?
		#Clase Dialogo de error. Solo modificarlo cada vez que se le llame
		if not self.cajaActual:
			self.msgBox.setWindowTitle('Error')
			self.msgBox.setText('Error: Seleccione un portal para agregar una pagina a este. ')
			self.msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
			self.msgBox.exec()
			return	
		else:
			arreglo_direcciones = []
			addPaginaDialogo = Dialogo_Add_Pagina()
			respuestaDialogo = addPaginaDialogo.dialogo.exec_()

			if addPaginaDialogo.valido & respuestaDialogo:
				arreglo_direcciones = addPaginaDialogo.lista
				self.barraProgreso.ui.progressBar.setRange(0,0)
				self.barraProgreso.ui.label.setText("Agregando página, por favor espere...")
				self.barraProgreso.dialogo.show()

				worker = WorkerAddPaginas(self.cajaActual, arreglo_direcciones, Almacenador.guardarPagina, baseDatos.add_pagina)
				worker.signals.finished.connect(self.barraProgreso.dialogo.hide)
				worker.signals.finished.connect(functools.partial(self.boton_caja_mostrar_clicked, self.cajaActual))
				#worker.run()
				self.threadpool.start(worker)

			elif respuestaDialogo:
				self.msgBox.setWindowTitle('URLs invalidas')
				self.msgBox.setText('Error, verifique que las URLs a agregar sean correctas.')
				self.msgBox.setModal(True)
				self.msgBox.setIcon(QtGui.QMessageBox.Warning)
				self.msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
				self.msgBox.exec()
				return

	def boton_eliminar_paginas_clicked(self):
		#TODO: Eliminacion en base de datos
		#pagSeleccionadas = self.ui.tableWidget.selectionModel().selectedRows()

		if not self.ui.tableWidget.selectedIndexes():
			self.msgBox.setWindowTitle('No hay páginas seleccionadas para eliminar')
			self.msgBox.setText('No hay páginas seleccionadas para eliminar')
			self.msgBox.setModal(True)
			self.msgBox.setIcon(QtGui.QMessageBox.Warning)
			self.msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
			self.msgBox.exec_()
			return

		self.msgBox.setWindowTitle('Eliminar páginas')
		self.msgBox.setText('¿Está seguro que desea eliminar las páginas seleccionadas?')
		self.msgBox.setModal(True)
		self.msgBox.setIcon(QtGui.QMessageBox.Warning)
		self.msgBox.setStandardButtons(QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
		#self.msgBox.setStandardButtons()		
		respuesta = self.msgBox.exec_()
		
		if respuesta == QtGui.QMessageBox.Ok:

			indices = []

			#Ordenando en reverso los elementos, necesario para la correcta eliminacion en el widget de tabla
			for pagina in self.ui.tableWidget.selectedIndexes():
				indices.append(pagina.row())
			indices.sort(reverse=True)

			#Removiendo de la lista de la caja
			for i in indices:
				baseDatos.eliminar_pagina(self.cajaActual.lista[int(i)]['url'])
				del self.cajaActual.lista[int(i)]

			#Removiendo del widget tabla
			for indice in indices: 
				self.ui.tableWidget.removeRow(indice)

			#logging.debug(self.cajaActual.lista)
			self.boton_caja_mostrar_clicked(self.cajaActual)
		

	def tabla_click(self, fila, columna, caja):
		if columna == 0:
			pyperclip.copy(caja.lista[fila]['url'])
			#print(caja.lista[fila])
		if columna == 1:
			pyperclip.copy(caja.lista[fila]['direccionArchivo'])

	def tabla_dobleClick(self, fila, columna, caja):
		if columna == 0:
			webbrowser.open(caja.lista[fila]['url'])
		if columna == 4:
			diff = ""
	
			verde   = QtGui.QColor("#03a300")
			rojo    = QtGui.QColor("#ff1e36")
			azul    = QtGui.QColor("#194cff")
			naranja = QtGui.QColor("#ffab35")
			
			colorVerde = QtGui.QTextCharFormat()
			colorVerde.setBackground(verde)

			colorRojo = QtGui.QTextCharFormat()
			colorRojo.setBackground(rojo)

			colorAzul = QtGui.QTextCharFormat()
			colorAzul.setBackground(azul)

			colorNaranja = QtGui.QTextCharFormat()
			colorNaranja.setBackground(naranja)

			dialogo = QtGui.QDialog()
			ventana = Ui_Dialogo_Diff()
			ventana.setupUi(dialogo)
			
			cursor_texto = QtGui.QTextCursor(ventana.textEdit.textCursor())

			for linea in caja.lista[fila]['diff']:
				if regexTextoAgregado.match(str(linea)):
					cursor_texto.insertText(str(linea),colorVerde)
				elif regexTextoEliminado.match(str(linea)):
					cursor_texto.insertText(str(linea),colorRojo)
				elif regexDiffPedazo.match(str(linea)):
					cursor_texto.insertText(str(linea),colorAzul)
				elif regexHttp.match(str(linea)) or regexTimeout.match(str(linea)) or regexErrCon.match(str(linea)):
					cursor_texto.insertText(str(linea),colorNaranja)
				else:
					cursor_texto.insertText(str(linea))

			dialogo.show()				
			respuestaDialogo = dialogo.exec_()

			if respuestaDialogo == QtGui.QDialog.Accepted:
				caja.lista[fila]['diffAceptado'] = True							
				
				if str(caja.lista[fila]['estatus'])[0:2] == 'ok':
					caja.lista[fila]['diff'] = ['']
					caja.lista[fila]['estatus'] = 'ok'
					baseDatos.cambiar_diff_pagina(caja.lista[fila]['url'],'')
					self.ui.tableWidget.item(fila,4).setBackground(QtGui.QColor(14,173,0))
					
				elif caja.lista[fila]['estatus'][:6] == 'hacked':
					caja.lista[fila]['diff'] = ['']
					caja.lista[fila]['estatus'] = 'ok'
					self.ui.tableWidget.setItem(fila,4, QtGui.QTableWidgetItem(''))					
					self.ui.tableWidget.item(fila,4).setBackground(QtGui.QColor(14,173,0))
					baseDatos.cambiar_diff_pagina(caja.lista[fila]['url'],'')
					baseDatos.set_estatus_pagina(caja.lista[fila]['url'],'ok')
				else:
					caja.lista[fila]['diff'] = caja.lista[fila]['estatus']
					baseDatos.cambiar_diff_pagina(caja.lista[fila]['url'],caja.lista[fila]['estatus'])
					self.ui.tableWidget.item(fila,4).setBackground(QtGui.QColor(255,188,0))
									
				completo = True

				for i in range(len(caja.lista)):
					if not caja.lista[i]['diffAceptado']:
						completo = False

				if completo:
					self.actualizarInterfazCaja(caja)

			else:
				logging.info("Dialogo diff negado")

	#--------------------------------------------

	def setPorcDif(self, fila, columna, caja):
		
		#print(self.ui.tableWidget.item(fila,columna).text())
		if columna == 2:
			try:
				float(self.ui.tableWidget.item(fila,columna).text())
			except ValueError:
				logging.error("Error, ingrese un número válido")
				self.msgBox.setWindowTitle('Error, ingrese un número válido')
				self.msgBox.setText('Ingrese un número válido como porcentaje mínimo')
				self.msgBox.setIcon(QtGui.QMessageBox.Critical)
				self.msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
				self.msgBox.exec()
				self.ui.tableWidget.setItem(fila,columna,QtGui.QTableWidgetItem('0'))
				baseDatos.cambiar_porcentaje_deteccion_cambio_pagina(caja.lista[fila]['url'],self.ui.tableWidget.item(fila,columna).text())
			else:
				baseDatos.cambiar_porcentaje_deteccion_cambio_pagina(caja.lista[fila]['url'],self.ui.tableWidget.item(fila,columna).text())
				caja.lista[fila]['porcDetectCambio'] = self.ui.tableWidget.item(fila,columna).text()
			
	#-------------Acciones Menu --------------------
	
	#>Opciones
	def setTimeout(self):
		texto, ok = QtGui.QInputDialog.getText(self, 'Tiempo de timeout', 'Ingrese el nuevo tiempo de timeout, igual o mayor a 5 segundos.')

		if ok & len(texto):
			try:
				numero = int(texto)
			except ValueError:
				logging.warning("Error, ingrese un número")
				self.msgBox.setWindowTitle('Error, tiempo de timeout')
				self.msgBox.setText('El tiempo de timeout debe ser un número')
				self.msgBox.setIcon(QtGui.QMessageBox.Critical)
				self.msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
				self.msgBox.exec()
			else:
				if numero < 5:
					logging.warning("Error, Ingrese un tiempo de timeout igual o superior a 5 segundos.")
					self.msgBox.setWindowTitle('Error, tiempo de timeout')
					self.msgBox.setText('El tiempo de timeout debe ser igual o mayor a 5 segundos.')
					self.msgBox.setIcon(QtGui.QMessageBox.Critical)
					self.msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
					self.msgBox.exec()
				else:
					opciones.tiempoTimeout = numero

		logging.debug("Tiempo de timeout: " + str(opciones.tiempoTimeout))

	#Ministerios
	def filtrarPortalesPorMinisterios(self):
		dialogoFiltrarCajas = Dialogo_Filtrar_Ministerios()
		#dialogoFiltrarCajas.dialogo.exec_()		
		listaMinisterios = []
		respuestaDialogo = dialogoFiltrarCajas.dialogo.exec()
		if respuestaDialogo:
			listaMinisterios = dialogoFiltrarCajas.listaMinisteriosFiltrada
		else:
			return
		
		listaCajasFiltrada = []

		for caja in self.listaCajasPermanente:
			if caja.ministerio in listaMinisterios:
				listaCajasFiltrada.append(caja)

		#print("**********Lista filtrados************")
		#print(listaCajasFiltrada)
		#Reseteando interfaz de cajas de portales

		for caja in self.listaCajas:
			#index = self.listaCajas.index(caja)
			caja.ui.setParent(None)
			#del self.listaCajas[index]

		self.listaCajas = listaCajasFiltrada

		for caja in self.listaCajas:
			for elem in caja.lista:					
				#Si el elemento diff contiene informacion al momento de la creacion ... Entonces es un error de conexion
				#print("diff:", str(elem['diff']))			
				if elem['diff'][0]:
					if elem['ultPorcCambio'] > float(elem['porcDetectCambio']):
						caja.ui.setStyleSheet('QGroupBox{color: red;\nfont: bold;}')
						caja.estatus = "mal"
					
						if regexHttp.match(str(elem['diff'][0])):
							caja.ui.setStyleSheet('QGroupBox{color: #FF8C00;\nfont: bold;}')
						
						elif regexErrCon.match(str(elem['diff'][0])):
							caja.ui.setStyleSheet('QGroupBox{color: #FF8C00;\nfont: bold;}')
						
						elif regexTimeout.match(str(elem['diff'][0])):
							caja.ui.setStyleSheet('QGroupBox{color: #FF8C00;\nfont: bold;}')

			self.ui.layoutScrollArea.addWidget(caja.ui)

	
	def editarPortal(self, caja):
		editarPortalDialogo = Dialogo_Editar_Portal(caja.portal, caja.ente)
		respuestaDialogo = editarPortalDialogo.dialogo.exec()
		if respuestaDialogo:
			if editarPortalDialogo.nombrePortal != '':
				print("Si va")
			else:
				print("No puede tener nombre vacio")



	def editarMinisterios(self):
		dialogoEditarMinisterios = Dialogo_Editar_Ministerios()
		dialogoEditarMinisterios.dialogo.exec_()
		
	def agregarMinisterio(self):
		nombre, ok = QtGui.QInputDialog.getText(self, 'Agregar Ministerio', 'Ingrese el nombre del ministerio a agregar.')

		if ok & len(nombre):
			if baseDatos.add_ministerio(nombre):
				logging.info("Ministerio " + nombre + " agregado")
				return 1
			else:
				logging.error("No se pudo agregar el " + nombre + " a la lista de ministerio de la base de datos." )
				return 0

	# Entes
	def filtrarPortalesPorEntes(self):
		dialogoFiltrarCajas = Dialogo_Filtrar_Entes()
		listaEntes = []
		respuestaDialogo = dialogoFiltrarCajas.dialogo.exec()
		if respuestaDialogo:
			listaEntes = dialogoFiltrarCajas.listaEntesFiltrados
		else:
			return
		
		listaCajasFiltrada = []

		for caja in self.listaCajasPermanente:
			if caja.ente in listaEntes:
				listaCajasFiltrada.append(caja)

		#print("**********Lista filtrados************")
		#print(listaCajasFiltrada)
		#Reseteando interfaz de cajas de portales

		for caja in self.listaCajas:
			caja.ui.setParent(None)

		self.listaCajas = listaCajasFiltrada
		
		for caja in self.listaCajas:
			for elem in caja.lista:					
				#Si el elemento diff contiene informacion al momento de la creacion ... Entonces es un error de conexion
				#print("diff:", str(elem['diff']))			
				if elem['diff'][0]:
					if elem['ultPorcCambio'] > float(elem['porcDetectCambio']):
						caja.ui.setStyleSheet('QGroupBox{color: red;\nfont: bold;}')
						caja.estatus = "mal"
					
						if regexHttp.match(str(elem['diff'][0])):
							caja.ui.setStyleSheet('QGroupBox{color: #FF8C00;\nfont: bold;}')
						
						elif regexErrCon.match(str(elem['diff'][0])):
							caja.ui.setStyleSheet('QGroupBox{color: #FF8C00;\nfont: bold;}')
						
						elif regexTimeout.match(str(elem['diff'][0])):
							caja.ui.setStyleSheet('QGroupBox{color: #FF8C00;\nfont: bold;}')

			self.ui.layoutScrollArea.addWidget(caja.ui)

	def editarEntes(self):
		dialogoEditarEntes = Dialogo_Editar_Entes()
		dialogoEditarEntes.dialogo.exec()

	def editarPalabrasClave(self):
		dialogoPalabrasClave = Dialogo_Palabras_Clave(self.palabrasClave)
		dialogoPalabrasClave.dialogo.exec_()
		self.palabrasClave = dialogoPalabrasClave.palabrasClave

	def mostrarEstadisticasCambios(self):
		dialogoMostrarEstadisticasCambios = Dialogo_Estadisticas_Cambios()
		dialogoMostrarEstadisticasCambios.dialogo.exec()



	#def agregarEnte(self):
		#stub

	#------------handlers -------------------------
	"""
	Este handler fue defeinido para poder llamar a la funcion baseDatos.cambiar_estatus_paginas desde el thread
	comparador creado dentro de la funcion Monitorear que corre dentro de un thread distinto al principal
	"""
	def handler_funcion_cambiar_estatus_bd(self, lista):
		baseDatos.cambiar_estatus_paginas(lista)

	def handler_insertar_cambio_bd(self, lista):
		for i in range(len(lista)):
			if  str(lista[i]['estatus'])[0:2] != "ok":
				if(lista[i]['estatus'] == 'hacked'):
					baseDatos.ingresar_cambio(lista[i]['ultPorcCambio'],lista[i]['estatus'],lista[i]['url'])
				else:
					baseDatos.ingresar_cambio(lista[i]['ultPorcCambio'],lista[i]['estatus'],lista[i]['url'])
			elif lista[i]['ultPorcCambio'] > float(lista[i]['porcDetectCambio']):
				#if not lista[i]['diffAceptado']:
				#print("*******entra cambio con",lista[i]['url'])
				baseDatos.ingresar_cambio(lista[i]['ultPorcCambio'],lista[i]['estatus'],lista[i]['url'])

	def pruebas(self):
		logging.debug("Función de pruebas")
		print("Funcion de prueba !")

#-------------Funciones para la prueba del comaparador sin base de datos ni aranha web ----------
"""
def almacenarPaginas():
	lista = obtenerLista()
	baseDatos = Almacenador.guardarPaginas(lista)
	#pprint(baseDatos)

	return baseDatos

def obtenerLista():
	#lista = {}

	lista = {'VenCERT':['http://www.vencert.gob.ve'],
		 'SUSCERTE':['http//www.suscerte.gob.ve'],
		 'ABAE':['http://www.abae.gob.ve'],
		'CNTI':['http://www.cnti.gob.ve'],
		'BANDES':['http://www.bandes.gob.ve'],
		'BOLIPUERTOS':['http://www.bolipuertos.gob.ve'],
		'METRO Ccs':['http://metrodecaracas.com.ve'],
		'CIDA':['http://www.cida.gob.ve'],
		'CNTQ':['http://www.cntq.gob.ve'],
		'CENCOEX':['http//www.cencoex.gob.ve'],
		'CIEPE':['http://www.ciepe.gob.ve'],
		'CGR':['http://www.cgr.gob.ve'],
		'CMC':['http://www.cmc.gob.ve'],
		'CORPOSALUD Aragua':['http://www.corposaludaragua.gob.ve'],
		'OPSU':['http://www.opsu.gob.ve'],
		'FIDETEL':['http://www.fidetel.gob.ve'],
		'CFG':['http://www.cfg.gob.ve'],
		'FONACIT':['http://www.fonacit.gob.ve'],
		'CENDITEL':['http://www.cenditel.gob.ve'],
		'Fundación Editorial El Perro y la Rana':['http://www.elperroylarana.gob.ve'],
		'FUNDAYACUCHO':['http://www.fundayacucho.gob.ve'],
		'FII':['http://www.fii.gob.ve'],
		'FUNDAPROAL':['http://www.fundaproal.gob.ve'],
		'FUNVISIS':['http://www.funvisis.gob.ve'],
		'ALBATEL':['http://www.telecomunicianesalba.com'],
		'INVEPAL':['http://www.invepal.com.ve'],
		'BNV':['http://www.bnv.gob.ve'],
		'INAC':['http://www.inac.gob.ve'],
		'IFE':['http://www.ife.gob.ve'],
		'INHRR':['http://www.inhrr.gob.ve'],
		'INAMEH':['http://www.inameh.gob.ve'],
		'IPOSTEL':['http://www.ipostel.gob.ve'],
		'INPSASEL':['http://www.inpsasel.gob.ve'],
		'INTT':['http://www.intt.gob.ve'],
		'IVIC':['http://www.ivic.go.ve'],
		'CENDIT':['http://www.cendit.gob.ve'],
		'INFOCENTRO':['http://www.infocentro.gob.ve'],
		'MERCAL':['http://www.mercal.gob.ve'],
		'MINCI':['http://minci.gob.ve'],
		'MPPEE':['http://www.mppee.gob.ve'],
		'M.P.P.Comunas':['http://www.mpcomunas.gob.ve'],
		'MPPEUCT':['http://www.mppeuct.gob.ve'],
		'MPPRIJ':['http://www.mpprij.gob.ve'],
		'MPPRE':['http://mppre.gob.ve'],
		'MINPI':['http://www.minpi.gob.ve'],
		'MINPPTRASS':['http://www.minpptrass.gob.ve'],
		'ONCTI':['http://www.oncti.gob.ve'],
		'ONCOP':['http://www.oncop.gob.ve'],
		'QUIMBIOTEC':['http://www.quimbiotec.gob.ve'],
		'Red TV':['http://www.redtv.gob.ve'],
		'IAESP':['http://www.iaesp.edu.ve'],
		'SAIME':['http://www.saime.gob.ve'],
		'SUDEBAN':['http://sudeban.gob.ve'],
		'SNC':['http://www.snc.gob.ve'],
		'SUNAGRO':['http://www.sunagro.gob.ve'],
		'SUNAI':['http://www.sunai.gob.ve'],
		'TELECOM':['http://www.telecom.gob.ve'],
		'UNES':['http://www.unes.edu.ve'],
		'UNESR':['http://www.unesr.edu.ve'],
		'UNELLEZ':['http://www.unellez.edu.ve'],
		'UNEFA':['http://www.unefa.edu.ve'],
		'LUZ':['http://www.luz.edu.ve'],
		'Laboratorios Miranda':['http://www.laboratoriosmiranda.gob.ve'],
		'Metro Maracaibo':['http://www.metrodemaracaibo.gob.ve'],
		'Defensa Pública':['http://www.defensapublica.gob.ve'],
		'IND':['http://www.ind.gob.ve'],
		'Presidencia':['http://www.presidencia.gob.ve'],
		'FARMAPTRIA':['http://www.farmapatria.gob.ve'],
		'TSS':['http://www.tss.gob.ve'],
		'PNB':['http://cpnb.gob.ve'],
		'TSJ':['http://www.tsj.gob.ve']
	}
"""

def my_excepthook(type, value, tback):
    # log the exception here

    # then call the default handler
    sys.__excepthook__(type, value, tback)

#----------------------Iniciando-----------------------------------
def main():
	
	QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads)
	app = QtGui.QApplication(sys.argv)
	app.setStyle("cleanlooks") #o plastique?
	
	#----aplicando hoja de estilo
	archivoEstilo = '../interfaz/estilo.qss'
	#archivoEstilo = '../interfaz/estilo1.qss'
	with open(archivoEstilo,'r') as archivo:
		app.setStyleSheet(archivo.read())
	


	logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
	logging.info("Iniciando BotGIT ...")

	myapp = VentanaMain()
	myapp.show()

	"""
	queue = Queue()
	sys.stdout = StreamEscritura(queue)
	
	thread = QtCore.QThread()
	receptor = Receptor(queue)
	receptor.signal.connect(myapp.agregarTextoConsola)
	receptor.moveToThread(thread)
	thread.started.connect(receptor.run)
	thread.start()
	"""
	
	sys.exit(app.exec_())
if __name__ == '__main__':
	main();

