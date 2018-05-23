#Qt4 SQL

#my.conf max_allowed_packet = 64M

import sys,pprint,logging

sys.path.append("../bin")

from PyQt4 import QtCore,QtSql
from PyQt4.QtCore import QCoreApplication
from almacenador import Almacenador


base_de_datos = "proyectoprueba1"
hostname      = "localhost"
usuario       = "root"
password      = "qwerty"

db = QtSql.QSqlDatabase.addDatabase("QMYSQL","conexion1")
db.setHostName(hostname)
db.setDatabaseName(base_de_datos)
db.setUserName(usuario)
db.setPassword(password)

bdatos_ok = db.open()

if not bdatos_ok:
	print("No Funciona")
	sys.exit()
else:
	print("Funciona!")
	query = QtSql.QSqlQuery(db)
	query.exec('SET wait_timeout = 9000')
	
	"""
	sys.exit()
	"""
#---------------- MINISTERIOS ------------------
class baseDatos():

	@staticmethod
	def add_ministerio(nombre):
		query.prepare(""" INSERT INTO ministerios (idministerio, nombre) VALUES (NULL, ?)""")
		query.addBindValue(nombre)
		
		if query.exec_():
			return 1
		else:
			#return query.lastError()
			return 0
	#Retorna array con ministerios
	@staticmethod
	def seleccionar_ministerios():
		listaMinisterios = []

		if query.exec(""" SELECT nombre FROM ministerios """):
			while query.next():
				listaMinisterios.append(str(query.value(0)))
			return sorted(listaMinisterios)
		else:
			return 0

	@staticmethod
	def seleccionar_ministerio_portal(nombrePortal):
		query.prepare(""" SELECT nombre FROM ministerios WHERE idministerio = (SELECT ministerios_idministerios FROM entes WHERE identes = (SELECT entes_identes FROM portales WHERE nombre = ?) ) """)
		query.addBindValue(nombrePortal)

		if query.exec_():
			while query.next():
				return str(query.value(0))
		else:
			return 0

	@staticmethod
	def seleccionar_id_ministerio(nombreMinisterio):
		query.prepare(""" SELECT idministerio from ministerios WHERE nombre = ? """)
		query.addBindValue(nombreMinisterio)

		if query.exec_():
			while query.next():
				return str(query.value(0))
		else:
			return 0

	#------------------ ENTES ----------------------
	@staticmethod
	def seleccionar_todos_entes():
		listaEntes = []
		query.prepare(""" SELECT * FROM entes """)
		
		if query.exec_():
			while query.next():
				listaEntes.append(str(query.value(1)))
			return sorted(listaEntes)
		else:
			return 0
	
	@staticmethod
	def seleccionar_ente_portal(nombrePortal):
		query.prepare(""" SELECT nombre FROM entes WHERE identes = (SELECT entes_identes FROM portales WHERE nombre = ? )""")
		query.addBindValue(nombrePortal)

		if query.exec_():
			while query.next():
				portal = query.value(0)
				return portal
		else:
			return 0
	


	@staticmethod
	def seleccionar_entes(nombreMinisterio):
		listaEntes = []
		query.prepare(""" SELECT nombre FROM entes WHERE ministerios_idministerios = (SELECT idministerio FROM ministerios WHERE nombre = ? )""")
		query.addBindValue(nombreMinisterio)
		
		if query.exec_():
			while query.next():
				listaEntes.append(str(query.value(0)))
			return sorted(listaEntes)
		else:
			return 0

	"""
	@staticmethod
	def add_ente(idMinisterio,nombre):
		query.prepare("INSERT INTO entes (identes,nombre,ministerios_idministerios) VALUES (NULL,?,?)")
		query.addBindValue(nombre)
		query.addBindValue(idMinisterio)

		if query.exec_():
			return 1
		else:
			return 0
	"""

	@staticmethod
	def add_ente(nombre,nombreMinisterio):
		query.prepare("INSERT INTO entes (identes,nombre,ministerios_idministerios) VALUES (NULL,?,(SELECT nombre FROM ministerios WHERE idministerio = ? ))")
		query.addBindValue(nombre)
		query.addBindValue(nombreMinisterio)

		if query.exec_():
			return 1
		else:
			return 0

	#----------------- PORTALES --------------------
	@staticmethod
	def add_portal(nombreEnte,nombrePortal):#TRANSACCIONAR
		print("nombre ente",nombreEnte)
		query.prepare("INSERT INTO portales (idportales,nombre,entes_identes,porcDetectarDiferencia,porcCambioActual) VALUES(NULL,?,(SELECT identes FROM entes WHERE nombre = ?),0,0)")
		query.addBindValue(nombrePortal)
		query.addBindValue(nombreEnte)		

		if query.exec_():
			db.commit()
			print(query.lastError().text())
			print("Portal agregado")
			return 1
		else:
			print("Portal no agregado")
			print(query.lastError().text())
			return 0

	@staticmethod
	def eliminar_portal(nombrePortal):
		query.prepare('DELETE FROM portales WHERE nombre = ?')
		query.addBindValue(nombrePortal)
		if query.exec_():
			logging.info("Portal " + nombrePortal + " eliminado")
			return 1
		else:
			print("BD: Error seteando el porcentaje de diferencia, deffault a 0")
			return 0

	@staticmethod
	def seleccionar_portales():
		portales = []
		listaUrls = []
		query.prepare("SELECT portales.nombre, urls.url, urls.archivo, urls.md5, urls.diff, urls.ultimo_porcentaje_cambio, urls.porcentaje_deteccion_cambio, urls.diff_aceptado, urls.estatus FROM portales INNER JOIN urls ON portales.idportales = urls.portales_idportales INNER JOIN entes on entes.identes = portales.entes_identes INNER JOIN ministerios ON ministerios.idministerio = entes.ministerios_idministerios")
		#query.first()
		if query.exec_():
			#query.first()
			query.first()
			portal = str(query.value(0))
			portalActual = portal
			portales.append({portal:[]})
			#portales.append({portal:[],'ministerio':ministerio})
			#print(portales)
			contPortal = 0
			tam = query.size()

			for fila in range(0,tam):
				query.seek(fila)
				#print("debug->",str(query.value(0)))
				portalActual = str(query.value(0))

				#{'url': url,'direccionArchivo': direccionArchivo,'md5': paginaMd5,'diff': diff, 'ultPorcCambio':ultPorcCambio, 'porcDetectCambio':0, 'diffAceptado':True, 'estatus':estatus}

				if portalActual == portal:
					diff = str(query.value(4)).split('\n')
					for linea in diff: linea = linea + '\\n'
					portales[contPortal][portal].append({'url':str(query.value(1)),'direccionArchivo':str(query.value(2)),'md5':str(query.value(3)),'diff':diff,'ultPorcCambio':float(query.value(5)),'porcDetectCambio':float(query.value(6)),'diffAceptado':str(query.value(7)),'estatus':str(query.value(8))})
					
				else:
					contPortal = contPortal + 1
					portal = portalActual
					portales.append({portal:[]})
					diff = str(query.value(4)).split('\n')
					for linea in diff: linea = linea + '\\n'
					portales[contPortal][portal].append({'url':str(query.value(1)),'direccionArchivo':str(query.value(2)),'md5':str(query.value(3)),'diff':diff,'ultPorcCambio':float(query.value(5)),'porcDetectCambio':float(query.value(6)),'diffAceptado':str(query.value(7)),'estatus':str(query.value(8))})
			return portales
		else:
			return 0

	@staticmethod
	def seleccionar_porcentaje_diferencia_portal(nombrePortal):
		query.prepare("SELECT porcDetectarDiferencia FROM portales WHERE nombre = ?")
		query.addBindValue(nombrePortal)
		if query.exec_():
			query.first()
			#print(query.value(0))
			#print(float(query.value(0)))
			return float(query.value(0))
		else:
			print("Error encontrando el porcentaje de diferencia, deffault a 0")
			return 0

	@staticmethod
	def set_porcentaje_diferencia_portal(porcentaje,nombrePortal):
		query.prepare("UPDATE portales SET porcDetectarDiferencia = ? WHERE nombre = ?")
		query.addBindValue(porcentaje)
		query.addBindValue(nombrePortal)
		if query.exec_():
			return 1
		else:
			print("BD: Error seteando el porcentaje de diferencia, deffault a 0")
			return 0

	#El ultimo porcentaje calculado, para resumir el programa y que no aparezca como 0
	@staticmethod
	def set_porc_deteccion_cambio_actual(porcentaje,nombrePortal):
		query.prepare("UPDATE portales SET porcCambioActual = ? WHERE nombre = ?")
		query.addBindValue(porcentaje)
		query.addBindValue(nombrePortal)
		if query.exec_():
			return 1
		else:
			print("BD: Error seteando el porcentaje de diferencia actual, deffault a 0 TEST")
			return 0

	@staticmethod
	def seleccionar_deteccion_cambio_actual(nombrePortal):
		query.prepare("SELECT porcCambioActual FROM portales WHERE nombre = ?")
		query.addBindValue(nombrePortal)
		if query.exec_():
			query.first()
			#print(query.value(0))
			#print(float(query.value(0)))
			return float(query.value(0))
		else:
			print("Error encontrando el porcentaje de diferencia actual, deffault a 0")
			return 0		

	#-------PAGINAS -------------------------------------------------------

	@staticmethod
	def add_pagina(nombrePortal,url,direccionArchivo,md5,diff,ultPorcCambio,porcDetectCambio,diffAceptado,estatus):
		#print("ejecutando- nombre portal = ",nombrePortal)

		query.prepare("INSERT INTO urls (idurls,url,archivo,md5,diff,ultimo_porcentaje_cambio,porcentaje_deteccion_cambio,diff_aceptado,estatus,portales_idportales) VALUES(NULL,?,?,?,?,?,?,?,?,(SELECT idportales FROM portales WHERE nombre = ?)) ")
		
		query.addBindValue(url)
		query.addBindValue(direccionArchivo)
		query.addBindValue(md5)
		query.addBindValue(diff)
		query.addBindValue(ultPorcCambio)
		query.addBindValue(porcDetectCambio)
		query.addBindValue(diffAceptado)
		query.addBindValue(estatus)
		query.addBindValue(nombrePortal)		

		if query.exec_():
			db.commit()
			print(query.lastError().text())
			print("agregada url")
			return 1
		else:
			print("url no agregada")
			print(query.lastQuery())
			print(query.lastError().text())
			return 0

	@staticmethod
	def eliminar_pagina(url):
		query.prepare("DELETE FROM urls WHERE urls.url = ?")
		query.addBindValue(url)
		if query.exec_():
			print("URL:",url,"eliminada.")
			return 1
		else:
			print("url no eliminada")
			print(query.lastError().text())
			return 0

	@staticmethod
	def eliminar_urls_portal(portal):
		query.prepare("DELETE FROM urls.url WHERE urls.portales_idportales = (SELECT idportales FROM portales WHERE nombre = ?)")
		query.addBindValue(portal)
		if query.exec_():
			print("URLs del portal " + portal + " eliminadas")
			return 1
		else:
			print("No se pudieron eliminar las URLs del portal " + portal + ", es posible que aparezcan URLs duplicadas")
			print(query.lastError().text())
			return 0		

	@staticmethod 
	def set_porcentaje_cambio_pagina(url,porcentaje):
		query.prepare("UPDATE urls SET ultimo_porcentaje_cambio = ? WHERE url = ?")
		query.addBindValue(porcentaje)
		query.addBindValue(url)
		if query.exec_():
			return 1
		else:
			print("BD: Error seteando el porcentaje de diferencia actual en la URL, deffault a 0")
			print(query.lastError().text())
			return 0

	@staticmethod
	def cambiar_porcentaje_deteccion_cambio_pagina(url,porcentaje): #verificar luego posibilidad de urls dobles
		query.prepare("UPDATE urls SET porcentaje_deteccion_cambio = ? WHERE url = ?")
		query.addBindValue(porcentaje)
		query.addBindValue(url)

		if query.exec_():
			return 1
		else:
			print("ERROR: Porcentaje de deteccion en", url, "no modificado")
			print(query)
			return 0

	@staticmethod 
	def set_estatus_pagina(url,estatus):
		query.prepare("UPDATE urls SET estatus = ? WHERE url = ?")
		query.addBindValue(estatus)
		query.addBindValue(url)
		if query.exec_():
			return 1
		else:
			print("BD: Error seteando el estatus de la URL, no será cambiado en la base de datos")
			print(query.lastError().text())
			return 0

	@staticmethod
	def cambiar_diff_pagina(url,diff):
		diff = ''.join(diff)

		query.prepare("UPDATE urls SET diff = ? WHERE url = ?")
		query.addBindValue(diff)
		query.addBindValue(url)
		if query.exec_():
			return 1
		else:
			print("BD: Error seteando el diff de la URL en la base de datos, no será cambiado en esta")
			print(query.lastError().text())
			return 0

	@staticmethod
	def cambiar_md5_pagina(url,md5):
		query.prepare("UPDATE urls SET md5 = ? WHERE url = ?")
		query.addBindValue(md5)
		query.addBindValue(url)
		if query.exec_():
			return 1
		else:
			print("BD: Error seteando el md5 de la URL en la base de datos, no será cambiado en esta")
			print(query.lastError().text())
			return 0

	#-------------------------------------------
	@staticmethod
	def cambiar_estatus_paginas(lista):

		print("-------> Funcion cambiar estatus")

		query.prepare("UPDATE urls SET ultimo_porcentaje_cambio = ?, estatus = ?, diff = ?, md5 = ? WHERE url = ?")

		for i in range(len(lista)):
			diff = ''.join(lista[i]['diff'])
			query.addBindValue(lista[i]['ultPorcCambio'])
			query.addBindValue(lista[i]['estatus'])
			query.addBindValue(diff)
			query.addBindValue(lista[i]['md5'])
			
			query.addBindValue(lista[i]['url'])

			if query.exec_():
				print("Query ok")
			else:
				print(query.lastError().text())
				print("BD: Error cambiando el estado")
				
	#----------------------- cambios -----------------------------------

	@staticmethod
	def ingresar_cambio(porcentaje,estatus,palabras,url):
		query.prepare("INSERT INTO cambios (idcambios, fecha, porcentaje, estatus, palabras_clave_detectadas, urls_idurls) VALUES (NULL,NOW(),?,?,?,(SELECT idurls FROM urls WHERE url = ?))")
		#query.addBindValue(fecha)
		query.addBindValue(porcentaje)
		query.addBindValue(estatus)
		query.addBindValue(palabras)
		query.addBindValue(url)
		if query.exec_():
			return 1
		else:
			print("BD: Error almacenando cambio en la base de datos")
			print(query.lastError().text())
			return 0

	@staticmethod
	def seleccionar_urls_portales(id_portal):#Selecciona las url de in portal
		print("seleccionar_urls_portales")
		query.prepare("SELECT url FROM urls WHERE portales_idportales = ?")
		query.addBindValue(id_portal)
		if query.exec_():
			while query.next():
				print(str(query.value(1)))
			return True
		else:
			return False

	@staticmethod
	def seleccionar_cambios_idurl(id_url):#Selecciona los cambios de una url en particular
		print("seleccionar_cambios_idurl")
		query.prepare("SELECT fecha,porcentaje,diff FROM cambios WHERE urls_idurls = ?")
		query.addBindValue(id_url)
		if query.exec_():
			while query.next():
				print(str(query.value(0)),str(query.value(1)),str(query.value(2)))
			return True
		else:
			print("False")
			return False


app = QCoreApplication(sys.argv)#necesario para q funcione ...

#add_ministerio('Ministerio del Poder Popular del Despacho de la Presidencia y Seguimiento de la Gestión de Gobierno')
#ministerios = mostrar_ministerios()
#pprint.pprint(ministerios)

#add_ente(17,'SUSCERTE')
#entes = seleccionar_entes_todos()
#pprint.pprint(entes)

#add_portal(idEnte,nombrePortal,listaUrls)
#add_portal(5,'LOCALHOST',['http://localhost','http://localhost/prueba'])

"""
print("seleccionando portales")
portales = baseDatos.seleccionar_portales()
pprint.pprint(portales)
"""
nombreEnte = 'Ente de Prueba'
nombrePortal = 'MPPRE'

#nombrePortal = 'localhost'
url = 'http://www.mppre.gob.ve'
direccionArchivo = 'portales/MPPRE/http://www_mppre_gob_ve.txt'
md5 = 'adadasdasdada65asd65as'
diff = ''
ultPorcCambio = 0
porcDetectCambio = 0
diffAceptado = True
estatus = 'ok'

baseDatos.add_portal(nombreEnte,nombrePortal)
baseDatos.add_pagina(nombrePortal,url,direccionArchivo,md5,diff,ultPorcCambio,porcDetectCambio,diffAceptado,estatus)

#baseDatos.add_pagina('LOCALHOST','http://localhost/prueba',)


sys.exit()
sys.exit(app.exec_())
