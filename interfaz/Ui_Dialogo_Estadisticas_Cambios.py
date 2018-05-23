# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_Estadísticas_cambios.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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

class Ui_Dialogo_Estadisticas_Cambios(object):
    def __init__(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(900, 600)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.comboBox_portales = QtGui.QComboBox(Dialog)
        self.comboBox_portales.setObjectName(_fromUtf8("comboBox_portales"))
        self.gridLayout.addWidget(self.comboBox_portales, 4, 1, 1, 3)
        self.comboBox_ministerio = QtGui.QComboBox(Dialog)
        self.comboBox_ministerio.setObjectName(_fromUtf8("comboBox_ministerio"))
        self.gridLayout.addWidget(self.comboBox_ministerio, 1, 1, 1, 3)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(_fromUtf8("Urls;Fecha;Porcentaje;Estatus").split(";"))
        self.tableWidget.setColumnWidth(0,330)
        self.tableWidget.setColumnWidth(1,150)
        self.tableWidget.setColumnWidth(2,90)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        
        self.gridLayout.addWidget(self.tableWidget, 9, 0, 1, 4)
        
        self.comboBox_entes = QtGui.QComboBox(Dialog)
        self.comboBox_entes.setObjectName(_fromUtf8("comboBox_entes"))
        self.gridLayout.addWidget(self.comboBox_entes, 3, 1, 1, 3)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        
        self.dateEdit2 = QtGui.QDateTimeEdit(Dialog)
        self.dateEdit2.setObjectName(_fromUtf8("dateEdit2"))
        self.dateEdit2.setCalendarPopup(True)
        self.dateEdit2.setDateTime(QtCore.QDateTime.currentDateTime())
        self.gridLayout.addWidget(self.dateEdit2, 7, 3, 1, 1)
        
        self.dateEdit1 = QtGui.QDateTimeEdit(Dialog)
        self.dateEdit1.setObjectName(_fromUtf8("dateEdit1"))
        self.dateEdit1.setCalendarPopup(True)
        self.dateEdit1.setDateTime(QtCore.QDateTime.currentDateTime())
        self.gridLayout.addWidget(self.dateEdit1, 7, 1, 1, 1)
        
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 7, 0, 1, 1)
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 7, 2, 1, 1)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 10, 3, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 10, 2, 1, 1)
        self.pushButton_3 = QtGui.QPushButton(Dialog)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout.addWidget(self.pushButton_3, 8, 0, 1, 4)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Estadística de cambios", None))
        self.label.setText(_translate("Dialog", "Portal", None))
        self.label_2.setText(_translate("Dialog", "Ente", None))
        self.label_3.setText(_translate("Dialog", "Ministerio", None))
        self.label_4.setText(_translate("Dialog", "Desde", None))
        self.label_5.setText(_translate("Dialog", "Hasta", None))
        self.pushButton.setText(_translate("Dialog", "Reporte", None))
        self.pushButton_2.setText(_translate("Dialog", "Cancelar", None))
        self.pushButton_3.setText(_translate("Dialog", "Consultar", None))

