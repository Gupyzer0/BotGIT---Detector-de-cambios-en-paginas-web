# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'crawler!.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys

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

class InterfazCrawler(object):    
    def __init__(self,Dialog):
        #Dialog.setWindowModality(Qt.ApplicationModal)
        self.gridLayout_3 = QtGui.QGridLayout(Dialog)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        
        self.gridLayout_3.addWidget(self.label_5, 0, 0, 1, 1)
        
        #Tabla Paginas
        self.tablaPaginas = QtGui.QTableWidget(Dialog)
        self.tablaPaginas.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tablaPaginas.setColumnCount(3)
        self.tablaPaginas.setObjectName(_fromUtf8("tablaPaginas"))
        self.tablaPaginas.setRowCount(0)
        self.tablaPaginas.setHorizontalHeaderLabels(_fromUtf8("Dominio;Pagina;Profundidad").split(";"))
        self.tablaPaginas.horizontalHeader().setVisible(True)
        self.tablaPaginas.horizontalHeader().setCascadingSectionResizes(False)
        self.tablaPaginas.horizontalHeader().setMinimumSectionSize(27)
        self.tablaPaginas.horizontalHeader().setSortIndicatorShown(False)
        self.tablaPaginas.horizontalHeader().setStretchLastSection(True)
        self.tablaPaginas.verticalHeader().setCascadingSectionResizes(False)
        self.tablaPaginas.verticalHeader().setSortIndicatorShown(False)
        self.tablaPaginas.verticalHeader().setStretchLastSection(False)
        self.tablaPaginas.setColumnWidth(0,250)
        self.tablaPaginas.setColumnWidth(1,570)
        

        #item = QtGui.QTreeWidgetItem(self.arbol_paginas)
        #item.setText(0,'Pais')

        #itemsHijos = QtGui.QTreeWidgetItem()
        #itemsHijos.setText(1,'Venezuela')
        #item.addChild(itemsHijos)
              
        self.gridLayout_3.addWidget(self.tablaPaginas, 1, 0, 1, 3)
        
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        
        self.gridLayout_3.addLayout(self.gridLayout, 2, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))

        #--------Nivel de Profundidad----------------
        self.label_nivel_profundidad = QtGui.QLabel(Dialog)
        self.label_nivel_profundidad.setObjectName(_fromUtf8("label_nivel_profundidad"))        
        self.gridLayout.addWidget(self.label_nivel_profundidad, 0, 0, 1, 1)
        
        self.nivel_profundidad = QtGui.QLabel(Dialog)
        self.nivel_profundidad.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.nivel_profundidad, 0, 1, 1, 1)
        
        self.horizontalSlide_nivel_profundidad = QtGui.QSlider(Dialog)
        self.horizontalSlide_nivel_profundidad.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlide_nivel_profundidad.setObjectName(_fromUtf8("horizontalSlide_nivel_profundidad"))
        self.horizontalSlide_nivel_profundidad.setPageStep(1)
        self.horizontalSlide_nivel_profundidad.setMaximum(5)
        self.horizontalSlide_nivel_profundidad.setMinimum(0)
        self.gridLayout.addWidget(self.horizontalSlide_nivel_profundidad, 1, 0, 1, 2)

        #-------Numero de threads------------
        """
        self.label_numero_threads = QtGui.QLabel(Dialog)
        self.label_numero_threads.setObjectName(_fromUtf8("label_numero_threads"))        
        self.gridLayout_2.addWidget(self.label_numero_threads, 0, 2, 1, 1)

        self.numero_threads = QtGui.QLabel(Dialog)
        self.numero_threads.setMaximumSize(QtCore.QSize(20, 16777215))
        self.numero_threads.setObjectName(_fromUtf8("label_numero_threads"))        
        self.gridLayout_2.addWidget(self.numero_threads, 0, 3, 1, 1)        

        self.horizontalSlider_numero_threads = QtGui.QSlider(Dialog)
        self.horizontalSlider_numero_threads.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_numero_threads.setObjectName(_fromUtf8("horizontalSlider_numero_threads"))
        self.horizontalSlider_numero_threads.setMaximum(10) #Convertir en algo variable?
        self.horizontalSlider_numero_threads.setMinimum(0)
        self.gridLayout_2.addWidget(self.horizontalSlider_numero_threads, 1, 2, 1, 2)
        
        #------Numero Paginas----------------
        self.label_paginas_maximo = QtGui.QLabel(Dialog)
        self.label_paginas_maximo.setObjectName(_fromUtf8("Label_paginas_maximo"))
        self.gridLayout_2.addWidget(self.label_paginas_maximo, 0,4,1,1)

        self.paginas_maximo = QtGui.QLabel(Dialog)
        self.paginas_maximo.setObjectName(_fromUtf8("paginas_maximo"))
        self.gridLayout_2.addWidget(self.paginas_maximo, 0,5,1,1)

        self.horizontalSlider_numero_paginas = QtGui.QSlider(Dialog)
        self.horizontalSlider_numero_paginas.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_numero_paginas.setObjectName(_fromUtf8("horizontalSlider_numero_paginas"))
        self.gridLayout_2.addWidget(self.horizontalSlider_numero_paginas, 1, 4, 1, 2)
        """
        #------Layout magic... ------------------
        self.gridLayout_3.addLayout(self.gridLayout_2, 2, 1, 1, 1)
        self.botonIniciarCrawl = QtGui.QPushButton(Dialog)
        self.botonIniciarCrawl.setObjectName(_fromUtf8("botonIniciarCrawl"))
        self.gridLayout_3.addWidget(self.botonIniciarCrawl, 2, 2, 1, 1)

        self.retranslateUi(Dialog)
        #QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Crawling!", None))
        self.label_5.setText(_translate("Dialog", "Páginas a ser exploradas:", None))
        self.nivel_profundidad.setText(_translate("Dialog", "0", None))
        self.label_nivel_profundidad.setText(_translate("Dialog", "Nivel del Profundidad:", None))
        #self.numero_threads.setText(_translate("Dialog", "0", None))
        #self.label_numero_threads.setText(_translate("Dialog", "Número de Threads:", None))
        #self.label_paginas_maximo.setText(_translate("Dialog", "Número Máximo de páginas:",None))
        #self.paginas_maximo.setText(_translate("Dialog", "0", None))
        self.botonIniciarCrawl.setText(_translate("Dialog", "Iniciar Crawling", None))

