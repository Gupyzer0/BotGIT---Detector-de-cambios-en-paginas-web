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

class Mensaje_Diff(QtGui.QMessageBox):
	def __init__(self, direccion,textoDiff):
		self.setText("Modificacion detectada")
		self.setInformativetext("Elija que desea hacer con esta modificacion")
		self.setStandardButtons(self.mostrarDiff, self.aceptar, self.abrirPagina)
		self.setDefaultButton(self.mostrarDiff)
		self.detailedText = QtCore.QString(textoDiff)