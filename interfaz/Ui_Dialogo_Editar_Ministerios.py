# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_editar_ministerios.ui'
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

class Ui_Dialogo_Editar_Ministerios(object):
    def __init__(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1000, 450)
        Dialog.setMinimumSize(QtCore.QSize(800, 450))
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 4, 3, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 4, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        
        self.tableView = QtGui.QTableView(Dialog)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setColumnWidth(0,50)
        self.gridLayout.addWidget(self.tableView, 2, 0, 1, 4)
        
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setInputMask(_fromUtf8(""))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 4)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Editar lista de ministerios", None))
        self.pushButton.setText(_translate("Dialog", "Eliminar Seleccionados", None))
        self.pushButton_2.setText(_translate("Dialog", "Agregar", None))
        self.label.setText(_translate("Dialog", "Lista de Ministerios", None))
        self.lineEdit.setPlaceholderText(_translate("Dialog", "Filtrar Ministerios", None))
