#!/usr/bin/env python
import sys
import time
import os.path
import math
import numpy as np

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_plot 
import PyQt4.Qwt5 as Qwt

from Utils.NPBuffer import *
from Utils.ZMQListener import *

class Ui_Sampler_MainWindow(ui_plot.Ui_SamplerWindow):
    counter = 1
    N = 2000
    t = NPBuffer(N)
    x = NPBuffer(N)
    y = NPBuffer(N)
    z = NPBuffer(N)
    m = NPBuffer(N)
    listener = ZMQListener("tcp://localhost:5555")

    curveX   = Qwt.QwtPlotCurve()
    curveY   = Qwt.QwtPlotCurve()
    curveZ   = Qwt.QwtPlotCurve()
    curveMag = Qwt.QwtPlotCurve()
    grid    = Qwt.QwtPlotGrid()

    def update(self):
        data = self.listener.grab()
        for d in data:
            self.t.append(self.counter)
            x = int(d['x'])
            y = int(d['y'])
            z = int(d['z'])
            self.x.append(x)
            self.y.append(y)
            self.z.append(z)
            self.m.append(math.sqrt(x*x + y*y + z*z))
            self.counter += 1
        if self.t.length() > 0:
            tnp = self.t.as_np()
            self.curveX.setData(tnp, self.x.as_np())
            self.curveY.setData(tnp, self.y.as_np())
            self.curveZ.setData(tnp, self.z.as_np())
            self.curveMag.setData(tnp, self.m.as_np())
            self.setxlim(np.min(tnp), max(np.max(tnp), np.min(tnp) + self.N))
            self.plot.replot()   

    def __init__(self):
        super(Ui_Sampler_MainWindow, self).__init__()

    def setupUi(self,window):
        super(Ui_Sampler_MainWindow, self).setupUi(window)
        self.curveX.attach(self.plot) 
        self.curveY.attach(self.plot) 
        self.curveZ.attach(self.plot) 
        self.curveMag.attach(self.plot) 
        self.setylim(-2048, 2047)

        # pen color
        # http://doc.qt.io/qt-4.8/qpen.html
        # http://doc.qt.io/qt-4.8/qcolor.html
        self.curveX.setPen(QPen(Qt.blue, 1, Qt.SolidLine))
        self.curveY.setPen(QPen(Qt.darkMagenta, 1, Qt.SolidLine))
        self.curveZ.setPen(QPen(Qt.darkGreen, 1, Qt.SolidLine))
        self.curveMag.setPen(QPen(Qt.black, 2, Qt.SolidLine))

        # set grid lines in plot background
        self.grid.enableXMin(True)
        self.grid.setMajPen(QPen(Qt.white, 0, Qt.DotLine))
        self.grid.setMinPen(QPen(Qt.gray, 0 , Qt.DotLine))
        self.grid.attach(self.plot)

    def get_file_name(self):
        directory      = self.outputDirectory.text()
        sample_name    = self.sampleNameCB.currentText()
        count = 1
        filename = "%s/%s-%03d.txt" % (directory, sample_name, count)
        while os.path.isfile(filename):
            count = count + 1
            filename = "%s/%s-%03d.txt" % (directory, sample_name, count)
        return filename

    def log(self, msg):
        self.logWindow.appendPlainText(msg)

    def setxlim(self, xmin, xmax): 
        self.plot.setAxisScale(Qwt.QwtPlot.xBottom, xmin, xmax)

    def setylim(self, ymin, ymax): 
        self.plot.setAxisScale(Qwt.QwtPlot.yLeft, ymin, ymax)

    def collect(self):
        pass



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_Sampler_MainWindow()
    ui.setupUi(window)

    # ui.controlButton.clicked.connect(lambda: sample(ui))
    ui.log("welcome to the sampler")

    ui.timer = QTimer() #start a timer (to call replot events)
    ui.timer.start(25.0) #set the interval (in ms)
    window.connect(ui.timer, SIGNAL('timeout()'), lambda : ui.update())

    window.show()
    sys.exit(app.exec_())
