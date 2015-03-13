import sys
import collections
import time
import zmq
import numpy as np
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_plot 
import PyQt4.Qwt5 as Qwt

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

socket.connect ("tcp://localhost:5555")

socket.setsockopt(zmq.SUBSCRIBE, "")

N = 512
tbuf = collections.deque([], N)
xbuf = collections.deque([], N)
ybuf = collections.deque([], N)
zbuf = collections.deque([], N)
t = np.array(xbuf, float)
x = np.array(xbuf, float)
y = np.array(ybuf, float)
z = np.array(zbuf, float)

def update():
    global t,x,y,z,tbuf,xbuf,ybuf,zbuf
    while (socket.poll(1)) :
        msg = socket.recv()
        # print '%s' % (msg)
        s = msg.split()
        tbuf.append(s[1])
        xbuf.append(s[2])
        ybuf.append(s[3])
        zbuf.append(s[4])
        t = np.array(tbuf, float)
        x = np.array(xbuf, float)
        y = np.array(ybuf, float)
        z = np.array(zbuf, float)

def plotSomething():
    global t,x,y,z,L
    update()
    #print "PLOTTING"
    curveX.setData(t, x)
    curveY.setData(t, y)
    curveZ.setData(t, z)
    # print t.shape, x.shape, y.shape, z.shape
    tmax = N + np.min(t)
    if len(t) > 0:
        tmax = max(np.max(t), tmax)

    ui.xPlot.setAxisScale(Qwt.QwtPlot.xBottom, np.min(t), tmax)
    ui.yPlot.setAxisScale(Qwt.QwtPlot.xBottom, np.min(t), tmax)
    ui.zPlot.setAxisScale(Qwt.QwtPlot.xBottom, np.min(t), tmax)
    ui.xPlot.replot()   
    ui.yPlot.replot()   
    ui.zPlot.replot()   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = ui_plot.Ui_MainWindow()
    ui.setupUi(window)

    ui.xPlot.axisEnabled(Qwt.QwtPlot.yLeft)

    ui.xPlot.setAxisScale(Qwt.QwtPlot.yLeft, -4.0, 4.0)
    ui.yPlot.setAxisScale(Qwt.QwtPlot.yLeft, -4.0, 4.0)
    ui.zPlot.setAxisScale(Qwt.QwtPlot.yLeft, -4.0, 4.0)

    # set up the QwtPlot (pay attention!)
    curveX=Qwt.QwtPlotCurve()  #make a curve
    curveY=Qwt.QwtPlotCurve()  
    curveZ=Qwt.QwtPlotCurve() 

    curveX.attach(ui.xPlot) #attach it to the qwtPlot object
    curveY.attach(ui.yPlot) 
    curveZ.attach(ui.zPlot) 

    gridX = Qwt.QwtPlotGrid()
    gridX.enableXMin(True)
    gridX.setMajPen(QPen(Qt.white, 0, Qt.DotLine))
    gridX.setMinPen(QPen(Qt.gray, 0 , Qt.DotLine))
    gridX.attach(ui.xPlot)

    gridY = Qwt.QwtPlotGrid()
    gridY.enableXMin(True)
    gridY.setMajPen(QPen(Qt.white, 0, Qt.DotLine))
    gridY.setMinPen(QPen(Qt.gray, 0 , Qt.DotLine))
    gridY.attach(ui.yPlot)

    gridZ = Qwt.QwtPlotGrid()
    gridZ.enableXMin(True)
    gridZ.setMajPen(QPen(Qt.white, 0, Qt.DotLine))
    gridZ.setMinPen(QPen(Qt.gray, 0 , Qt.DotLine))
    gridZ.attach(ui.zPlot)

    ui.timer = QTimer() #start a timer (to call replot events)
    ui.timer.start(100.0) #set the interval (in ms)

    window.connect(ui.timer, SIGNAL('timeout()'), plotSomething)

    # show the main window
    window.show()
    sys.exit(app.exec_())
