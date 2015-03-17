all: ui_plot.py
	pyuic4 ui_plot.ui | perl -wlpE 's/from qwt_plot import QwtPlot/from Qwt import */' > ui_plot.py
