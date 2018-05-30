#Widget para filtrar los portales vistos por ministerio
import sys, re, logging, webbrowser
sys.path.append("../interfaz")

from PyQt4 import QtCore, QtGui, Qt
from qt4BaseDatos import baseDatos
from Ui_Dialogo_Estadisticas_Cambios import Ui_Dialogo_Estadisticas_Cambios

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class Dialogo_Estadisticas_Cambios(QtGui.QWidget):
	def __init__(self):
		super(Dialogo_Estadisticas_Cambios, self).__init__()
		
		self.dialogo = QtGui.QDialog()
		self.dialogo.setModal(True)
		self.dialogo.setAttribute(QtCore.Qt.WA_DeleteOnClose)
				
		self.ui = Ui_Dialogo_Estadisticas_Cambios(self.dialogo)

		#Inicializando comboboxes
		arrMins = baseDatos.seleccionar_ministerios()
		self.ui.comboBox_ministerio.addItem("Todos")
		self.ui.comboBox_entes.addItem("Todos")
		self.ui.comboBox_portales.addItem("Todos")
		
		for ministerio in arrMins:
			self.ui.comboBox_ministerio.addItem(ministerio)

		self.ui.comboBox_ministerio.currentIndexChanged.connect(self.cargarEntes)
		self.ui.comboBox_entes.currentIndexChanged.connect(self.cargarPortales)
		self.ui.pushButton_3.clicked.connect(self.consultarBdatos)
		self.ui.pushButton_2.clicked.connect(self.dialogo.reject)
		self.ui.pushButton.clicked.connect(self.generarReporte)
		#deshabilitando boton de generar reportes hasta que se haya hecho alguna consulta
		self.ui.pushButton.setDisabled(1)

		"""
		Las siguientes variables guardan los nombres y fechas al momento que se consulta la base 
		de datos, esto debido a que si se obtienen los nombres directamente de los 'combobox' al 
		momento de generar el reporte, se podria ingresar datos erroneos de ministerio,ente y portal
		en este.
		"""
		self.ministerioConsultado = ""
		self.enteConsultado = ""
		self.portalConsultado  = ""
		self.fechaInicioConsultada = ""
		self.fechaFinalConsultada = ""


	def cargarEntes(self):
		self.ui.comboBox_entes.clear()
		arrEntes = baseDatos.seleccionar_entes(self.ui.comboBox_ministerio.currentText())
		self.ui.comboBox_entes.addItem("Todos")
		for ente in arrEntes:
			self.ui.comboBox_entes.addItem(ente)

	def cargarPortales(self):
		self.ui.comboBox_portales.clear()
		arrPortales = baseDatos.seleccionar_nombres_portales(self.ui.comboBox_entes.currentText())
		self.ui.comboBox_portales.addItem("Todos")
		for ente in arrPortales:
			self.ui.comboBox_portales.addItem(ente)

	def consultarBdatos(self):

		listaCambios = baseDatos.seleccionar_cambios(self.ui.dateEdit1.dateTime().toString("yyyy-MM-dd hh:mm"), self.ui.dateEdit2.dateTime().toString("yyyy-MM-dd hh:mm"),self.ui.comboBox_ministerio.currentText(),self.ui.comboBox_entes.currentText(),self.ui.comboBox_portales.currentText())

		self.ministerioConsultado = self.ui.comboBox_ministerio.currentText()
		self.enteConsultado = self.ui.comboBox_entes.currentText()
		self.portalConsultado  = self.ui.comboBox_portales.currentText()
		self.fechaInicioConsultada = self.ui.dateEdit1.dateTime().toString("dd-MM-yyyy hh:mm")
		self.fechaFinalConsultada = self.ui.dateEdit2.dateTime().toString("dd-MM-yyyy hh:mm")

		#Si existen cambios
		if listaCambios:
			self.ui.tableWidget.setRowCount(len(listaCambios))

			for i in range(len(listaCambios)):
				
				self.ui.tableWidget.setItem(i,0, QtGui.QTableWidgetItem(listaCambios[i]['url']))
				self.ui.tableWidget.setItem(i,1, QtGui.QTableWidgetItem(listaCambios[i]['fecha']))
				self.ui.tableWidget.setItem(i,2, QtGui.QTableWidgetItem(listaCambios[i]['porcentaje']))
				self.ui.tableWidget.setItem(i,3, QtGui.QTableWidgetItem(listaCambios[i]['estatus']))

			self.ui.pushButton.setDisabled(0)

		else:
			self.ui.tableWidget.setRowCount(0)
			msgBox = QtGui.QMessageBox()
			msgBox.setWindowTitle('No se encontraron cambios')
			msgBox.setText('No se encontraron cambios')
			msgBox.setModal(True)
			msgBox.setIcon(QtGui.QMessageBox.Information)
			msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
			msgBox.exec()

	def generarReporte(self):
		#ingresando elementos de la tabla a una lista para representarla facilmente en el pdf
		listaTabla = []
		listaTabla.append(["Url", "Fecha", "porcentaje", "Estatus"])

		for i in range(self.ui.tableWidget.rowCount()):
			listaTabla.append([self.ui.tableWidget.item(i,0).text(),self.ui.tableWidget.item(i,1).text(),self.ui.tableWidget.item(i,2).text(), self.ui.tableWidget.item(i,3).text()])


		doc = SimpleDocTemplate("../Reportes/reporte_cambios.pdf", pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
		doc.pagesize = landscape(A4)
		elementos = []

		style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
		               ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
		               ('VALIGN',(0,0),(0,-1),'TOP'),
		               ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
		               ('ALIGN',(0,-1),(-1,-1),'CENTER'),
		               ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
		               ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
		               ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
		               ('BOX', (0,0), (-1,-1), 0.25, colors.black),
		               ])

		#Configurar estilo y la envoltura de las palabras
		
		#Estilo texto de las tablas
		s = getSampleStyleSheet()
		s = s["BodyText"]
		s.wordWrap = 'CJK' #evita que las palabras excedan el largo y desborden/perturben otras secciones
		data = [[Paragraph(celda, s) for celda in row] for row in listaTabla]
		
		titulos = getSampleStyleSheet()
		titulos = titulos["title"]
		titulos.wordWrap = 'CJK'

		t=Table(data)
		t.setStyle(style)
		 
		#Enviar data y construir el archivo
		elementos.append(Paragraph("Reporte de cambios detectados",titulos))
		
		#agregando informacion de ministerio - ente - portal consultado
		if self.ministerioConsultado == "Todos":
			elementos.append(Paragraph("Ministerio seleccionado: Todos",s))
			elementos.append(Paragraph("Ente seleccionado: Todos",s))
			elementos.append(Paragraph("Portal seleccionado: Todos",s))
		elif self.ministerioConsultado != "Todos" and self.enteConsultado == "Todos":
			elementos.append(Paragraph("Ministerio seleccionado: " + self.ministerioConsultado,s))
			elementos.append(Paragraph("Ente seleccionado: Todos",s))
			elementos.append(Paragraph("Portal seleccionado: Todos",s))
		elif self.enteConsultado != "Todos" and self.portalConsultado == "Todos":
			elementos.append(Paragraph("Ministerio seleccionado: " + self.ministerioConsultado,s))
			elementos.append(Paragraph("Ente seleccionado: " + self.enteConsultado,s))
			elementos.append(Paragraph("Portal seleccionado: Todos",s))
		else:
			elementos.append(Paragraph("Ministerio seleccionado: " + self.ministerioConsultado,s))
			elementos.append(Paragraph("Ente seleccionado: " + self.enteConsultado,s))
			elementos.append(Paragraph("Portal seleccionado: " + self.portalConsultado,s))

		elementos.append(Paragraph("Cambios entre las fechas: " + self.fechaInicioConsultada + " y " + self.fechaFinalConsultada, s))
		elementos.append(t)
		doc.build(elementos)

		webbrowser.open_new_tab("../Reportes/reporte_cambios.pdf")
