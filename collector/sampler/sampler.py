#!/usr/bin/env python
import sys
import collections
import time
import zmq
import numpy as np
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_plot 
import PyQt4.Qwt5 as Qwt
import os.path

class zmq_listener:
    context = None
    socket = None
    target = None

    def __init__(self, target):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.target = target
        self.socket.connect (self.target)
        self.socket.setsockopt(zmq.SUBSCRIBE, "")

    def grab(self):
        accum = []
        while (self.socket.poll(1)) :
            msg = self.socket.recv()
            # print '%s' % (msg)
            s = msg.split()
            if len(s) >= 5:
                accum.append({ 't': s[1], 'x': s[2], 'y': s[3], 'z': s[4], })
        return accum
    def close(self):
        self.socket.close()
        self.context.term()

class npbuffer:
    x = None
    def __init__(self, size):
        self.x = collections.deque([], size)
    def as_np(self, howmany = None):
        if howmany:
            return np.array(self.x[-howmany:], float)
        else:
            return np.array(self.x, float)
    def append(self, new):
        self.x.append(new)
    def length(self):
        return len(self.x)

class sampler:
    ui = None
    sample_size = None
    tbuf = None
    xbuf = None
    ybuf = None
    zbuf = None
    zmq  = None
    def __init__(self, ui): 
        self.ui = ui
        self.sample_size = self.ui.numSamples.value()
        self.tbuf = npbuffer(self.sample_size)
        self.xbuf = npbuffer(self.sample_size)
        self.ybuf = npbuffer(self.sample_size)
        self.zbuf = npbuffer(self.sample_size)
        self.zmq = zmq_listener("tcp://127.0.0.1:5555")

    # this is called every X ms
    def sample(self):
        # print "sample.sample()"
        for d in self.zmq.grab():
            if self.tbuf.length() < self.sample_size:
                self.tbuf.append(d['t'])
                self.xbuf.append(d['x'])
                self.ybuf.append(d['y'])
                self.zbuf.append(d['z'])
        self.ui.samplingProgress.setValue(100 * self.tbuf.length() / self.sample_size)
        self.ui.set_x(self.sample_size, self.tbuf, self.xbuf)
        self.ui.set_y(self.sample_size, self.tbuf, self.ybuf)
        self.ui.set_z(self.sample_size, self.tbuf, self.zbuf)
        if self.tbuf.length() == self.sample_size:
            window.disconnect(self.ui.timer, SIGNAL('timeout()'), tick)
            self.zmq.close()

            filename = self.ui.get_file_name()
            self.ui.log("wrote sample to " + filename)
            fh = open(filename, 'w')
            l = self.tbuf.length()
            t = self.tbuf.as_np()
            x = self.xbuf.as_np()
            y = self.ybuf.as_np()
            z = self.zbuf.as_np()
            for i in range(0, l):
                fh.write( "%0.4f\t%0.4f\t%0.4f\t%0.4f\n" % ( t[i], x[i], y[i], z[i]))
            fh.close()


s = None
def tick():
    s.sample()

def sample(ui):
    global s
    s = sampler(ui)
    ui.timer = QTimer() 
    ui.timer.start(100.0) 
    ui.log("grabbing sample...")
    window.connect(ui.timer, SIGNAL('timeout()'), tick)

class Ui_Sampler_MainWindow(ui_plot.Ui_MainWindow):
    curveX=Qwt.QwtPlotCurve()  #make a curve
    curveY=Qwt.QwtPlotCurve()  
    curveZ=Qwt.QwtPlotCurve() 
    def __init__(self):
        super(Ui_Sampler_MainWindow, self).__init__()

    def setupUi(self,window):
        super(Ui_Sampler_MainWindow, self).setupUi(window)
        self.curveX.attach(self.xPlot) 
        self.curveY.attach(self.yPlot) 
        self.curveZ.attach(self.zPlot) 
        self.setylim(self.xPlot, -4.0, 4.0)
        self.setylim(self.yPlot, -4.0, 4.0)
        self.setylim(self.zPlot, -4.0, 4.0)
        self.setgrid(self.xPlot)
        self.setgrid(self.yPlot)
        self.setgrid(self.zPlot)

    def set_x(self, maxwidth, tbuf, xbuf):
        self.set_data(self.xPlot, self.curveX, maxwidth, tbuf, xbuf)
    def set_y(self, maxwidth, tbuf, xbuf):
        self.set_data(self.yPlot, self.curveY, maxwidth, tbuf, xbuf)
    def set_z(self, maxwidth, tbuf, xbuf):
        self.set_data(self.zPlot, self.curveZ, maxwidth, tbuf, xbuf)

    def set_data(self, plot, curve, maxwidth, tbuf, xbuf):
        t = tbuf.as_np()
        x = xbuf.as_np()
        curve.setData(t, x)
        tmax = maxwidth + np.min(t)
        if len(t) > 0:
            tmax = max(np.max(t), tmax)
        self.setxlim(plot, np.min(t), tmax)
        plot.replot()   

    def get_file_name(self):
        directory      = self.outputDirectory.text()
        sample_name    = self.sampleNameCB.currentText()
        sample_subname = self.subname.currentText()
        count = 1
        filename = "%s/%s-%s-%03d.txt" % (directory, sample_name, sample_subname, count)
        while os.path.isfile(filename):
            count = count + 1
            filename = "%s/%s-%s-%03d.txt" % (directory, sample_name, sample_subname, count)
        return filename

    def log(self, msg):
        self.logWindow.appendPlainText(msg)

    def setxlim(self, plot, xmin, xmax): 
        plot.setAxisScale(Qwt.QwtPlot.xBottom, xmin, xmax)

    def setylim(self, plot, ymin, ymax): 
        plot.setAxisScale(Qwt.QwtPlot.yLeft, ymin, ymax)

    def setgrid(self, plot):
        gridX = Qwt.QwtPlotGrid()
        gridX.enableXMin(True)
        gridX.setMajPen(QPen(Qt.white, 0, Qt.DotLine))
        gridX.setMinPen(QPen(Qt.gray, 0 , Qt.DotLine))
        gridX.attach(plot)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_Sampler_MainWindow()
    ui.setupUi(window)

    ui.controlButton.clicked.connect(lambda: sample(ui))
    ui.log("welcome to the sampler")

    window.show()
    sys.exit(app.exec_())
