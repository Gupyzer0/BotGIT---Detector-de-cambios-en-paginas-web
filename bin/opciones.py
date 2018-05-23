import configparser

configuracion = configparser.ConfigParser()
configuracion.sections()
configuracion.read('opciones.ini')

#Variables globales
tiempoTimeout = int(configuracion['opciones']['timeout'])