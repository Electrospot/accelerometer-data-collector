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
    window = None
    counter = 0
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
    grid     = Qwt.QwtPlotGrid()

    curveX_capture   = Qwt.QwtPlotCurve()
    curveY_capture   = Qwt.QwtPlotCurve()
    curveZ_capture   = Qwt.QwtPlotCurve()
    curveMag_capture = Qwt.QwtPlotCurve()
    grid_capture     = Qwt.QwtPlotGrid()

    #######################################################################

    def __init__(self):
        super(Ui_Sampler_MainWindow, self).__init__()

    def setupUi(self,window):
        super(Ui_Sampler_MainWindow, self).setupUi(window)
        self.window = window

        self.startCaptureButton.clicked.connect(lambda: self.startCapture())
        self.cancelButton.clicked.connect(lambda: self.cancel_last_capture())

        # save some space
        self.previewPlot.enableAxis(Qwt.QwtPlot.yLeft, False)
        self.previewPlot.enableAxis(Qwt.QwtPlot.xBottom, False)

        QObject.connect(self.xCalScaling, SIGNAL('valueChanged(double)'), lambda : self.calibration_changed())
        QObject.connect(self.yCalScaling, SIGNAL('valueChanged(double)'), lambda : self.calibration_changed())
        QObject.connect(self.zCalScaling, SIGNAL('valueChanged(double)'), lambda : self.calibration_changed())
        QObject.connect(self.xCalOffset, SIGNAL('valueChanged(double)'), lambda : self.calibration_changed())
        QObject.connect(self.yCalOffset, SIGNAL('valueChanged(double)'), lambda : self.calibration_changed())
        QObject.connect(self.zCalOffset, SIGNAL('valueChanged(double)'), lambda : self.calibration_changed())

        # background capture
        self.timer = QTimer() 
        self.timer.start(25.0) 
        self.window.connect(self.timer, SIGNAL('timeout()'), lambda : self.update())

        # update rate
        self.update_rate_timer = QTimer() 
        self.update_rate_timer.start(1000.0) 
        self.window.connect(self.update_rate_timer, SIGNAL('timeout()'), lambda : self.update_rate())

        # two timers for waiting to capture and capturing
        self.waiting_timer = QTimer()
        self.window.connect(self.waiting_timer, SIGNAL('timeout()'), lambda : self.waiting_callback())
        self.capture_timer = QTimer() 
        self.window.connect(self.capture_timer, SIGNAL('timeout()'), lambda : self.capture_callback())

        # main plot window
        self.curveX.attach(self.plot) 
        self.curveY.attach(self.plot) 
        self.curveZ.attach(self.plot) 
        self.curveMag.attach(self.plot) 
        self.plot.setAxisScale(Qwt.QwtPlot.yLeft, -8, 8)

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

        # same for capture window
        self.curveX_capture.attach(self.previewPlot) 
        self.curveY_capture.attach(self.previewPlot) 
        self.curveZ_capture.attach(self.previewPlot) 
        self.curveMag_capture.attach(self.previewPlot) 
        self.previewPlot.setAxisScale(Qwt.QwtPlot.yLeft, -8, 8)

        self.curveX_capture.setPen(QPen(Qt.blue, 1, Qt.SolidLine))
        self.curveY_capture.setPen(QPen(Qt.darkMagenta, 1, Qt.SolidLine))
        self.curveZ_capture.setPen(QPen(Qt.darkGreen, 1, Qt.SolidLine))
        self.curveMag_capture.setPen(QPen(Qt.black, 2, Qt.SolidLine))

        self.grid_capture.enableXMin(True)
        self.grid_capture.setMajPen(QPen(Qt.white, 0, Qt.DotLine))
        self.grid_capture.setMinPen(QPen(Qt.gray, 0 , Qt.DotLine))
        self.grid_capture.attach(self.previewPlot)

    #######################################################################
    # util

    def log(self, msg):
        self.logWindow.appendPlainText(msg)

    last_file_name = None
    def get_next_file_name(self):
        directory   = self.outputDirectory.text()
        sample_name = self.sampleName.currentText()
        count = 1
        filename = os.path.expanduser("%s/%s-%03d.txt" % (directory, sample_name, count))
        while os.path.isfile(filename):
            count = count + 1
            filename = os.path.expanduser("%s/%s-%03d.txt" % (directory, sample_name, count))
        self.last_file_name = filename
        return filename

    #######################################################################
    # main plot window

    def update(self):
        data = self.listener.grab()
        for d in data:
            self.t.append(self.counter)
            x = float(d['x'])
            y = float(d['y'])
            z = float(d['z'])
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
            self.plot.setAxisScale(Qwt.QwtPlot.xBottom, np.min(tnp), max(np.max(tnp), np.min(tnp) + self.N))
            self.plot.replot()   

    #######################################################################
    # update_rate

    last_count = None
    def update_rate(self):
        if self.last_count is not None:
            estimated_rate = self.counter - self.last_count
            self.rateLabel.setText("%d samples per second" % estimated_rate)
        self.last_count = self.counter

    #######################################################################
    # calibration

    def calibration_changed(self):
        self.listener.set_x_scaling(self.xCalScaling.value())
        self.listener.set_y_scaling(self.yCalScaling.value())
        self.listener.set_z_scaling(self.zCalScaling.value())
        self.listener.set_x_offset(self.xCalOffset.value())
        self.listener.set_y_offset(self.yCalOffset.value())
        self.listener.set_z_offset(self.zCalOffset.value())

    #######################################################################
    # capture

    def startCapture(self):
        self.waitProgress.setMaximum(100)
        self.captureProgress.setMaximum(100)
        self.waitProgress.setValue(0)
        self.captureProgress.setValue(0)

        self.time_at_start = time.time()
        self.waiting_timer.start(100)
        self.startCaptureButton.setEnabled(False)

    def waiting_callback(self):
        time_elapsed = time.time() - self.time_at_start
        needed = self.delay.value() 
        self.waitProgress.setValue(100.0 * time_elapsed/needed) 

        if (time_elapsed >= needed):
            self.waiting_timer.stop()
            self.counter_at_start_time = self.counter
            self.capture_timer.start(100.0) 

    def capture_callback(self):
        captured_since_start = self.counter - self.counter_at_start_time
        needed = self.numSamples.value()
        fraction_captured = min(1.0, float(captured_since_start) / needed)
        self.captureProgress.setValue(100.0 * fraction_captured) 

        if captured_since_start >= needed:
            self.capture_timer.stop()
            # show the data in the preview window and write it to disk
            tnp = self.t.as_np(needed)
            xnp = self.x.as_np(needed)
            ynp = self.y.as_np(needed)
            znp = self.z.as_np(needed)
            self.curveX_capture.setData(tnp, xnp)
            self.curveY_capture.setData(tnp, ynp)
            self.curveZ_capture.setData(tnp, znp)
            self.curveMag_capture.setData(tnp, self.m.as_np())
            self.previewPlot.setAxisScale(Qwt.QwtPlot.xBottom, np.min(tnp), np.max(tnp))
            self.previewPlot.replot()   
            write_xyz(self.get_next_file_name(), tnp, xnp, ynp, znp)
            self.log("wrote %d samples to %s" % (needed, self.last_file_name))
            self.cancelButton.setEnabled(True)
            self.startCaptureButton.setEnabled(True)

    def cancel_last_capture(self):
        if self.last_file_name is not None:
            self.log("removed %s" % self.last_file_name)
            os.remove(self.last_file_name)
            self.cancelButton.setEnabled(False)

def write_xyz(file_name, t,x,y,z):
    f = open(file_name, 'w')
    assert t.size == x.size
    assert t.size == y.size
    assert t.size == z.size
    for i in range(0,t.size):
        f.write("%0.3f\t%0.3f\t%0.3f\t%0.3f\n" % (t[i], x[i], y[i], z[i]))
    f.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_Sampler_MainWindow()
    ui.setupUi(window)

    # ui.controlButton.clicked.connect(lambda: sample(ui))
    # ui.log("welcome to the sampler")

    window.show()
    sys.exit(app.exec_())
