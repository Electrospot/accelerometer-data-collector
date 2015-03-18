all: ui_plot.py

ui_plot.py: ui_plot.ui
	pyuic4 ui_plot.ui | perl -wlpE 's/from qwt_plot import QwtPlot/from PyQt4.Qwt5 import */' > ui_plot.py
