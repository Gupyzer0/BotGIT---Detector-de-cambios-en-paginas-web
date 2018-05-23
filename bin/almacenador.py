#-----Almacenador-----

import requests, hashlib, pprint, os, html2text, logging, configparser

#from main import tiempoTimeout
#tiempoTimeout = 10

#print("Tiempo de timeout:"+str(opciones.tiempoTimeout))


class Almacenador():

	#portal es una variable "dummy" para obtener el nombre del portal. Recuerde que esta clase
	#es para poner a funcionar el modulo comparador sin base de datos o arana
	@staticmethod
	def guardarPaginas(listaUrls):
		baseDatos = {}

		for portal,valor in listaUrls.items():
			#print('------------>' + portal)

			try:
				os.makedirs(os.path.join('portales', portal))
			except OSError:
				pass
				#print('ya existe el directorio')

			baseDatos[portal] = []

			for elemento in valor:

				paginaMd5        = ""
				diff             = ""
				direccionArchivo = ""

				try:
					objetoRequests = requests.get(elemento, verify = False, timeout=10)
					objetoRequests.raise_for_status()
				
				#Error en http, devolvemos el codigo del error
				except requests.exceptions.HTTPError as error:
					#print("Error HTTP: \n" + str(error))
					estatus = objetoRequests.status_code
					diff = [str(objetoRequests.status_code)]
					#baseDatos[portal].append({'url': elemento,'direccionArchivo': direccionArchivo,'md5': '','diff': diff })								
					direccionArchivo = os.path.join('portales', portal, Almacenador.eliminarCaracteresProhibidos(elemento + ".txt"))
		
					archivo = open(os.path.join(direccionArchivo), 'wb')
					archivo.write("Error HTTP".encode('utf-8'))
					archivo.close()
					baseDatos[portal].append({'url': elemento,'direccionArchivo': direccionArchivo,'md5': '','diff': diff,  'ultPorcCambio': 100, 'porcDetectCambio':0, 'diffAceptado':True,'estatus':estatus })
				
				#Errores de conexion
				except requests.exceptions.ConnectionError as error:
					#print("Error de conexion: \n" + str(error))
					estatus = 'Error de Conexion'
					diff = ["Error de Conexion"]			

					direccionArchivo = os.path.join('portales', portal, Almacenador.eliminarCaracteresProhibidos(elemento + ".txt"))
		
					archivo = open(os.path.join(direccionArchivo), 'wb')
					archivo.write("Error de Conexion".encode('utf-8'))
					archivo.close()
					baseDatos[portal].append({'url': elemento,'direccionArchivo': direccionArchivo,'md5': '','diff': diff, 'ultPorcCambio': 100, 'porcDetectCambio':0, 'diffAceptado':True,'estatus':estatus })

				#Tiempo de espera agotado	
				except requests.exceptions.Timeout as error:
					#print("Tiempo de espera agotado: \n" + str(error))
					estatus = objetoRequests.status_code
					diff = ["Timeout"]					
					
					direccionArchivo = os.path.join('portales', portal, Almacenador.eliminarCaracteresProhibidos(elemento + ".txt"))
		
					archivo = open(os.path.join(direccionArchivo), 'wb')
					archivo.write("Timeout".encode('utf-8'))
					archivo.close()
					#baseDatos[portal].append({'url': elemento,'direccionArchivo': direccionArchivo,'md5': '','diff': diff, 'ultPorcCambio': 0 })
					baseDatos[portal].append({'url': elemento,'direccionArchivo': direccionArchivo,'md5': '','diff': diff, 'ultPorcCambio': 100, 'porcDetectCambio':0, 'diffAceptado':True, 'estatus':estatus })

				#Error no manejado
				except:
					#print("Error inesperado al conectar: " + elemento)
					estatus = objetoRequests.status_code
					direccionArchivo = os.path.join('portales', portal, Almacenador.eliminarCaracteresProhibidos(elemento + ".txt"))
					
					diff = ['Error Inesperado']
					archivo = open(os.path.join(direccionArchivo), 'wb')
					archivo.write("Error de Conexion Inesperado".encode('utf-8'))
					archivo.close()
					baseDatos[portal].append({'url': elemento,'direccionArchivo': direccionArchivo,'md5': '','diff': diff, 'ultPorcCambio': 100, 'porcDetectCambio':0, 'diffAceptado':True, 'estatus':estatus })

				else:
					#estatus = objetoRequests.status_code
					estatus = "ok " + str(objetoRequests.status_code)
					diff = ['']	
					paginaMd5 = hashlib.md5(objetoRequests.text.encode('utf-8')).hexdigest()
					listaTextoArchivo = objetoRequests.text.splitlines(keepends = True)
					
					direccionArchivo = os.path.join('portales', portal, Almacenador.eliminarCaracteresProhibidos(elemento + ".txt"))
					
					#print("Prueba elemento ->",len(elemento)/2)
					#print("tamaño",len(direccionArchivo))

					if len(direccionArchivo) > 260:
						#Si el tamaño de la dir. de l archivo es sueprior a los 260 bytes este será recortado
						#hasta ser menor que 260 bytes ... Evita errores en sistemas windows
						while True:
							elemento = elemento[int(len(elemento)/2):]
							direccionArchivo = os.path.join('portales', portal, Almacenador.eliminarCaracteresProhibidos(elemento + ".txt"))
							if not len(direccionArchivo) > 260:
								break					

					archivo = open(os.path.join(direccionArchivo), 'wb')
					
					for linea in listaTextoArchivo:				
						linea = linea.encode('utf-8')					
						archivo.write(linea)

					archivo.close()

					baseDatos[portal].append({'url': elemento,'direccionArchivo': direccionArchivo,'md5': paginaMd5,'diff': diff,'ultPorcCambio':0, 'porcDetectCambio':0, 'diffAceptado':True,'estatus':estatus})
		#print(baseDatos)
		return baseDatos

	@staticmethod
	def eliminarCaracteresProhibidos(linea):
		caracteresProhibidos = ['/','\0','<','>',':','"','\\','|','?','*']
		for caracter in caracteresProhibidos:
			linea = linea.replace(caracter,'_')

		return linea

	@staticmethod
	def guardarPagina(portal,url):
		
		direccionArchivo  = ""
		paginaMd5         = ""
		listaTextoArchivo = []

		try:
			os.makedirs(os.path.join('portales', portal))
		except OSError:
			pass
			#print('ya existe el directorio')

		try:
			#print("Tiempo Timeout Almacenador",str(opciones.tiempoTimeout))
			objetoRequests = requests.get(url, verify = False, timeout = 10)
			objetoRequests.raise_for_status()
		#Error en http, devolvemos el codigo del error

		except requests.exceptions.HTTPError as error:
			#print("Error HTTP: \n" + str(error))
			estatus = objetoRequests.status_code
			diff = [str(objetoRequests.status_code)]
			paginaMd5 = 'Error HTTP'
			ultPorcCambio = 100
			listaTextoArchivo = ['Error de conexion HTTP']
		#Errores de conexion
		except requests.exceptions.ConnectionError as error:
			#print("Error de conexion: \n" + str(error))
			estatus = "Error de Conexion"
			diff = ['Error de Conexion']
			paginaMd5 = 'Error de Conexion'
			ultPorcCambio = 100
			listaTextoArchivo = ['Error de conexion']
		#Tiempo de espera agotado	
		except requests.exceptions.Timeout as error:
			#print("Tiempo de espera agotado: \n" + str(error))
			estatus = "Timeout"
			diff = ['Timeout']
			paginaMd5 = 'Timeout'
			ultPorcCambio = 100
			listaTextoArchivo = ['Error de conexion, Timeout']
		#Error no manejado
		except requests.exceptions.RequestException as error:
			estatus = "Error de Conexion"
			diff = ['Error']
			paginaMd5 = 'Error'
			ultPorcCambio = 100
			listaTextoArchivo = ['Error de conexion Inesperado']

		else:
			#estatus = 'Error de conexion'
			estatus = "ok " + str(objetoRequests.status_code)	
			diff = ['']
			paginaMd5 = hashlib.md5(objetoRequests.text.encode('utf-8')).hexdigest()
			listaTextoArchivo = objetoRequests.text.splitlines(keepends = True)
			ultPorcCambio = 0
			logging.debug('Pagina agregada sin errores')
		
		finally:
			direccionArchivo = os.path.join('portales', portal, Almacenador.eliminarCaracteresProhibidos(url + ".txt"))
			if len(direccionArchivo) > 260:
				#Si el tamaño de la dir. de l archivo es sueprior a los 260 bytes este será recortado
				#hasta ser menor que 260 bytes ... Evita errores en sistemas windows
				while True:
					elemento = elemento[int(len(elemento)/2):]
					direccionArchivo = os.path.join('portales', portal, Almacenador.eliminarCaracteresProhibidos(elemento + ".txt"))
					if not len(direccionArchivo) > 260:
						break

			archivo = open(os.path.join(direccionArchivo), 'wb')
				
			for linea in listaTextoArchivo:				
				linea = linea.encode('utf-8')					
				archivo.write(linea)
		
			archivo.close()

		#pagina.append({'url': url,'direccionArchivo': direccionArchivo,'md5': paginaMd5})


		#return {'direccionArchivo':direccionArchivo, 'paginaMd5':paginaMd5}
		logging.debug("---->Porcentaje cambio:" + str(ultPorcCambio))						
		logging.debug("diff: " + str(diff))
		return {'url': url,'direccionArchivo': direccionArchivo,'md5': paginaMd5,'diff': diff, 'ultPorcCambio':ultPorcCambio, 'porcDetectCambio':0, 'diffAceptado':True, 'estatus':estatus}
		       
