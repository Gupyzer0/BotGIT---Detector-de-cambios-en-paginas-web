# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_addCaja.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
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

class Ui_Dialogo_Add_Portal(object):
    def __init__(self, dialog):
        dialog.setObjectName(_fromUtf8("dialog"))
        dialog.resize(1000, 280)
        self.gridLayout = QtGui.QGridLayout(dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineEdit = QtGui.QLineEdit(dialog)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.plainTextEdit = QtGui.QPlainTextEdit(dialog)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.gridLayout.addWidget(self.plainTextEdit, 3, 0, 1, 2)
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)
        self.label = QtGui.QLabel(dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
       
        self.comboBox_ministerio = QtGui.QComboBox(dialog)
        self.comboBox_ministerio.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout.addWidget(self.comboBox_ministerio, 5, 0, 1, 1)

        self.comboBox_entes = QtGui.QComboBox(dialog)
        self.comboBox_entes.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout.addWidget(self.comboBox_entes, 6, 0, 1, 1) 

        self.buttonBox = QtGui.QDialogButtonBox(dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 1)

        self.retranslateUi(dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(_translate("dialog", "Añadir Portal", None))
        self.label.setText(_translate("dialog", "Nombre del nuevo portal", None))
        self.label_2.setText(_translate("dialog", "URL\'s a agregar separadas por comas, la primera será considerada como la \"semilla\". Ej: http://www.pagina.gob.ve,http://www.pagina.gob.ve/noticias", None))

