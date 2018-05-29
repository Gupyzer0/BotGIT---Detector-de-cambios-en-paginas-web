import sys

#obtiene el dominio de una página web
"""
def obtenerDominio(link):
	base = ''
	for pnt in range(8, len(link)):
		if link[pnt:pnt + 1] == '/':
			base = link[0:pnt]
			break
	return base
"""

def obtenerDominio(link):

	link = link.replace('http://','')
	link = link.replace('https://','')

	ptr = link.find('/')

	if link[ptr] == ('/'):
		posicion = link.find('/')
		link = link[0:posicion]

	return link

#la pagina base es de donde se estan sacando los vinculos

def moverUnNivelAtras(pagina_base, link):
	pBarra = pagina_base.rfind('/')# emula strrpos php
	paginaRaiz= pagina_base[0:pBarra]
	link= link[3: 3+(len(link)-3)]# emula substr php ojo >> -3
	lista= [paginaRaiz, link]
	return lista

def resolverDireccion(pagina_base, link):
	
	#print(pagina_base, 'pagina base')
	link = link.strip()
	#print(pagina_base, "pag base")
	pagina_base = pagina_base.strip()
	pagina_base = pagina_base + "/"


	#remover caracteres innecesarios
	link = link.replace(';', '')#emula str_replace
	link = link.replace('\\', '')
	link = link.replace('\'', '')

	direccionAbsoluta = pagina_base + link
	
	#corrigiendo direccion
	correcionFinalizada = False;

	#Si la direccion empieza con "/"
	if not correcionFinalizada:
		if direccionAbsoluta[0:1] == '/':
			direccionAbsoluta = pagina_base + link
			correcionFinalizada = True
			#print("Si la direccion empieza con barra")

	#Referencias a directorios más "arriba"
	if not correcionFinalizada:
		if link[0:3] == '../':
			direccionBaseDesajustada = ''

			posicionUltimoSlash = pagina_base.rfind('/')
			
			if posicionUltimoSlash == len(pagina_base)-1:
				pagina_base = pagina_base[0:len(pagina_base)-1]
				posicionBarra = pagina_base.rfind('/')
			if posicionBarra < 8:
				direccionBaseDesajustada = pagina_base

			no_Finalizado = True
			while no_Finalizado:
				pagina_base, link = moverUnNivelAtras(pagina_base,link)
			
				if link[0:3] != '../':
					no_Finalizado = False

			if direccionBaseDesajustada:
				direccionAbsoluta = direccionBaseDesajustada + "/" + link
			else:
				direccionAbsoluta = pagina_base + "/" + link
			#print("Referencias a Directorios Superiores")
			correcionFinalizada = True		

	#Buscando referencias al directorio base
	if not correcionFinalizada:
		if link[0:1] == '/':
			link = link[1: 1 + (len(link)-1)]
			direccionAbsoluta = pagina_base + link
			correcionFinalizada = True
			#print("Buscando referencias al directorio base")

	#Buscando referencias de que ya son absolutos
	if not correcionFinalizada:
		if link[0:4] == 'http':
			direccionAbsoluta = link
			correcionFinalizada = True
			#print("Referencias de que ya son absolutos")

	#Añadir protocolo si es necesario
	#No necesariamente pasaron por la ultima comprobacion
	if direccionAbsoluta[0:7] != 'http://' and direccionAbsoluta[0:8] != 'https://':
		direccionAbsoluta = 'http://' + direccionAbsoluta

	return direccionAbsoluta
