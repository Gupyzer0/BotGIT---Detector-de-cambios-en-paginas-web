import sys, requests, pprint, logging
sys.path.append("../interfaz")
#sys.path.append("../bd")

from PyQt4 import QtCore,QtGui
from qt4BaseDatos import baseDatos
from ventanaCrawl import InterfazCrawler
from bs4 import BeautifulSoup
import resolvedor_direcciones, requests, pprint, time, sys, logging, configparser, opciones

try:
	_fromUtf8 = QtCore.QString._fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

class Araña:
	def __init__(self,semilla,nivelMaximo,retardo):
		self.semilla = semilla
		#print(self.semilla)
		self.dominio = resolvedor_direcciones.obtenerDominio(self.semilla)
		#print("Dominio base: ",self.dominio)
		self.nivelMaximo = nivelMaximo
		self.arregloLinks = []
		self.retardo = retardo
		self.extensionesInvalidas = ['#',
            '.pdf',
            '.mp3',
            '.mp4',
            '.jpg',
            'jpeg',
            '.png',
            '.gif',
            '.doc',
            '.docx',
            '.zip',
            '.tar',
            '.gz',
            '.rar']

	#Siempre debe de llamarse a este metodo con una profundidad de 0 para iniciar
	def caminar(self, direccion = None, profundidad_actual = 0):
		primeraPagina = False
		if direccion == None:
			direccion = self.semilla
			self.arregloLinks.append(self.semilla)
			primeraPagina = True
		
		logging.info("direccion caminada:" + direccion)	
		#print("direccion caminada:", direccion)

		if(profundidad_actual > self.nivelMaximo):
			logging.debug("profundida maxima, saliendo")
			return
		
		try:
			logging.debug("Tiempo Timeout Crawler "+ str(opciones.tiempoTimeout))
			pagina = requests.get(direccion, verify=False, timeout = opciones.tiempoTimeout)
			pagina.raise_for_status()

		except requests.exceptions.HTTPError as error:
			logging.info('Error al intentar descargar la pagina ' + direccion + ' ' + str(error) )
			if primeraPagina: return
			pass
		#Errores de conexion
		except requests.exceptions.ConnectionError as error:
			logging.info('Error al intentar descargar la pagina ' + direccion + ' ' + str(error) )
			if primeraPagina: return
			pass
		#Tiempo de espera agotado	
		except requests.exceptions.Timeout as error:
			logging.info('Error al intentar descargar la pagina ' + direccion + ' ' + str(error) )
			if primeraPagina: return
			pass
		#Error no manejado
		except:
			logging.info('Error al intentar descargar la pagina ' + direccion + ' ' + str(error) )
			if primeraPagina: return
			pass
		else:
			#time.sleep(self.retardo) -> implementarlo en el worker
			if pagina.status_code == requests.codes.ok:
				sopa = BeautifulSoup(pagina.text, 'html.parser')
				if sopa:
					for link in sopa.find_all('a', href=True):
						link = link['href']
						#print("URL en proceso: ", link)
						direccionResuelta = resolvedor_direcciones.resolverDireccion(self.dominio,link)
						#print(direccionResuelta)

						if self.verificarDireccion(link,direccionResuelta):
							print("URL cosechada = " + direccionResuelta)
							self.arregloLinks.append(direccionResuelta)
							self.caminar(direccionResuelta, profundidad_actual + 1)				

	def verificarDireccion(self, link, direccionResuelta):
		print("verificando")

		valido = True
		
		if resolvedor_direcciones.obtenerDominio(direccionResuelta) != self.dominio:
			print('URL con dominio diferente' + direccionResuelta)
			valido = False

		if direccionResuelta in self.arregloLinks:
			print('URL repetida' + direccionResuelta)
			valido = False

		if 'javascript' in direccionResuelta:
			print('URL con palabra javascript' + direccionResuelta)
			valido = False

		if  direccionResuelta.endswith('//#' or '/#' or '//'):
			print('ext invalida 1')
			valido = False

		for extInvalida in self.extensionesInvalidas:
			if direccionResuelta.endswith(extInvalida):
				print('ext invalida 2')
				valido = False
				break
		#print(valido)
		return valido

class Crawler(QtGui.QWidget):
	#lista semillas = [{portal:nombrePortal, semilla:'http:// ...'}]
	def __init__(self, listaSemillas):
		super(Crawler, self).__init__()
		
		self.listaSemillas = listaSemillas
		#self.signals = Signals()
		self.opcionesCrawler = []

		self.dialogo = QtGui.QDialog()
		self.dialogo.setAttribute(QtCore.Qt.WA_DeleteOnClose)

		self.dialogo.setMinimumSize(950,400)
		self.ui = InterfazCrawler(self.dialogo)	
		#self.ui.setupUi(self.dialogo)
		self.ui.horizontalSlide_nivel_profundidad.valueChanged.connect(self.setNivelProfundidad)		
		#self.ui.horizontalSlider_numero_threads.valueChanged.connect(self.setNumeroThreads)

		for i in range(len(self.listaSemillas)):
			self.ui.tablaPaginas.setRowCount(len(self.listaSemillas))
			self.ui.tablaPaginas.setItem(i,0, QtGui.QTableWidgetItem(listaSemillas[i]['portal']))
			self.ui.tablaPaginas.setItem(i,1, QtGui.QTableWidgetItem(listaSemillas[i]['semilla']))
			comboBoxNiveles = QtGui.QComboBox()
			comboBoxNiveles.addItems(['0','1','2','3','4','5'])
			self.ui.tablaPaginas.setCellWidget(i,2,comboBoxNiveles)			
		
		self.ui.botonIniciarCrawl.clicked.connect(self.setOpcionesCrawler)

	def setSemillas(self, listaSemillas):
		self.listaSemillas = listaSemillas

	def setNivelProfundidad(self, valor):
		self.ui.nivel_profundidad.setText(str(valor))
		for i in range(self.ui.tablaPaginas.rowCount()):
			self.ui.tablaPaginas.cellWidget(i,2).setCurrentIndex(valor)

	def setOpcionesCrawler(self):
		for i in range(self.ui.tablaPaginas.rowCount()):
			portal = self.ui.tablaPaginas.item(i,0).text()
			semilla = self.ui.tablaPaginas.item(i,1).text()
			profundidad = self.ui.tablaPaginas.cellWidget(i,2).currentIndex()
			
			self.opcionesCrawler.append({'portal':portal, 'semilla':semilla, 'profundidad':profundidad})

		#pprint.pprint(self.opcionesCrawler)
		self.dialogo.accept() #Esconde la ventana y acepta el dialogo, destruir ?

	def closeEvent(self,event):
		self.destroy()