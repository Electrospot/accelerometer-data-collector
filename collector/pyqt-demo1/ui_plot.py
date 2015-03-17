# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_plot.ui'
#
# Created: Tue Mar 17 11:25:37 2015
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(808, 769)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.xPlot = QwtPlot(self.centralwidget)
        self.xPlot.setObjectName(_fromUtf8("xPlot"))
        self.gridLayout.addWidget(self.xPlot, 0, 0, 1, 1)
        self.yPlot = QwtPlot(self.centralwidget)
        self.yPlot.setObjectName(_fromUtf8("yPlot"))
        self.gridLayout.addWidget(self.yPlot, 1, 0, 1, 1)
        self.zPlot = QwtPlot(self.centralwidget)
        self.zPlot.setObjectName(_fromUtf8("zPlot"))
        self.gridLayout.addWidget(self.zPlot, 2, 0, 1, 1)
        self.xSpecPlot = QwtPlot(self.centralwidget)
        self.xSpecPlot.setObjectName(_fromUtf8("xSpecPlot"))
        self.gridLayout.addWidget(self.xSpecPlot, 0, 1, 1, 1)
        self.ySpecPlot = QwtPlot(self.centralwidget)
        self.ySpecPlot.setObjectName(_fromUtf8("ySpecPlot"))
        self.gridLayout.addWidget(self.ySpecPlot, 1, 1, 1, 1)
        self.zSpecPlot = QwtPlot(self.centralwidget)
        self.zSpecPlot.setObjectName(_fromUtf8("zSpecPlot"))
        self.gridLayout.addWidget(self.zSpecPlot, 2, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 6)
        self.gridLayout.setColumnStretch(1, 4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 808, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))

from Qwt import *
