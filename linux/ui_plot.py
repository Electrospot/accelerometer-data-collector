# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_plot/ui_plot.ui'
#
# Created: Wed Mar 11 13:56:30 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import PyQt4.Qwt5 as Qwt

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
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.xPlot = Qwt.QwtPlot(self.centralwidget)
        self.xPlot.setObjectName(_fromUtf8("xPlot"))
        self.verticalLayout.addWidget(self.xPlot)
        self.yPlot = Qwt.QwtPlot(self.centralwidget)
        self.yPlot.setObjectName(_fromUtf8("yPlot"))
        self.verticalLayout.addWidget(self.yPlot)
        self.zPlot = Qwt.QwtPlot(self.centralwidget)
        self.zPlot.setObjectName(_fromUtf8("zPlot"))
        self.verticalLayout.addWidget(self.zPlot)
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

