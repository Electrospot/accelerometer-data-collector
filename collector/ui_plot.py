# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_plot.ui'
#
# Created: Mon May 18 13:41:58 2015
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

class Ui_SamplerWindow(object):
    def setupUi(self, SamplerWindow):
        SamplerWindow.setObjectName(_fromUtf8("SamplerWindow"))
        SamplerWindow.resize(1151, 975)
        self.centralwidget = QtGui.QWidget(SamplerWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.plot = QwtPlot(self.centralwidget)
        self.plot.setObjectName(_fromUtf8("plot"))
        self.horizontalLayout.addWidget(self.plot)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.sampleName = QtGui.QComboBox(self.groupBox)
        self.sampleName.setEditable(True)
        self.sampleName.setObjectName(_fromUtf8("sampleName"))
        self.sampleName.addItem(_fromUtf8(""))
        self.sampleName.addItem(_fromUtf8(""))
        self.sampleName.addItem(_fromUtf8(""))
        self.sampleName.addItem(_fromUtf8(""))
        self.sampleName.addItem(_fromUtf8(""))
        self.sampleName.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.sampleName, 1, 2, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.outputDirectory = QtGui.QLineEdit(self.groupBox)
        self.outputDirectory.setObjectName(_fromUtf8("outputDirectory"))
        self.gridLayout.addWidget(self.outputDirectory, 0, 2, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_2 = QtGui.QLabel(self.groupBox_3)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.numSamples = QtGui.QSpinBox(self.groupBox_3)
        self.numSamples.setMinimum(100)
        self.numSamples.setMaximum(10000)
        self.numSamples.setSingleStep(100)
        self.numSamples.setProperty("value", 1500)
        self.numSamples.setObjectName(_fromUtf8("numSamples"))
        self.gridLayout_2.addWidget(self.numSamples, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox_3)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.delay = QtGui.QSpinBox(self.groupBox_3)
        self.delay.setMaximum(10)
        self.delay.setSingleStep(1)
        self.delay.setProperty("value", 1)
        self.delay.setObjectName(_fromUtf8("delay"))
        self.gridLayout_2.addWidget(self.delay, 1, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox_3)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)
        self.waitProgress = QtGui.QProgressBar(self.groupBox_3)
        self.waitProgress.setProperty("value", 0)
        self.waitProgress.setTextVisible(False)
        self.waitProgress.setObjectName(_fromUtf8("waitProgress"))
        self.gridLayout_2.addWidget(self.waitProgress, 2, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox_3)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 3, 0, 1, 1)
        self.captureProgress = QtGui.QProgressBar(self.groupBox_3)
        self.captureProgress.setProperty("value", 0)
        self.captureProgress.setTextVisible(False)
        self.captureProgress.setObjectName(_fromUtf8("captureProgress"))
        self.gridLayout_2.addWidget(self.captureProgress, 3, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem, 5, 0, 1, 1)
        self.previewPlot = QwtPlot(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previewPlot.sizePolicy().hasHeightForWidth())
        self.previewPlot.setSizePolicy(sizePolicy)
        self.previewPlot.setMinimumSize(QtCore.QSize(0, 0))
        self.previewPlot.setObjectName(_fromUtf8("previewPlot"))
        self.gridLayout_2.addWidget(self.previewPlot, 6, 0, 1, 2)
        self.cancelButton = QtGui.QPushButton(self.groupBox_3)
        self.cancelButton.setEnabled(False)
        self.cancelButton.setCheckable(False)
        self.cancelButton.setChecked(False)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.gridLayout_2.addWidget(self.cancelButton, 7, 0, 1, 2)
        self.startCaptureButton = QtGui.QPushButton(self.groupBox_3)
        self.startCaptureButton.setObjectName(_fromUtf8("startCaptureButton"))
        self.gridLayout_2.addWidget(self.startCaptureButton, 4, 0, 1, 2)
        self.verticalLayout_3.addWidget(self.groupBox_3)
        self.groupBox_4 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_6 = QtGui.QLabel(self.groupBox_4)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_3.addWidget(self.label_6, 0, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_3.addWidget(self.label_8, 1, 0, 1, 1)
        self.label_9 = QtGui.QLabel(self.groupBox_4)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_3.addWidget(self.label_9, 2, 0, 1, 1)
        self.xCalScaling = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.xCalScaling.setMaximum(2.0)
        self.xCalScaling.setSingleStep(0.05)
        self.xCalScaling.setProperty("value", 1.0)
        self.xCalScaling.setObjectName(_fromUtf8("xCalScaling"))
        self.gridLayout_3.addWidget(self.xCalScaling, 0, 1, 1, 1)
        self.yCalScaling = QtGui.QDoubleSpinBox(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yCalScaling.sizePolicy().hasHeightForWidth())
        self.yCalScaling.setSizePolicy(sizePolicy)
        self.yCalScaling.setMaximum(2.0)
        self.yCalScaling.setSingleStep(0.05)
        self.yCalScaling.setProperty("value", 1.0)
        self.yCalScaling.setObjectName(_fromUtf8("yCalScaling"))
        self.gridLayout_3.addWidget(self.yCalScaling, 1, 1, 1, 1)
        self.zCalScaling = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.zCalScaling.setMaximum(2.0)
        self.zCalScaling.setSingleStep(0.05)
        self.zCalScaling.setProperty("value", 1.0)
        self.zCalScaling.setObjectName(_fromUtf8("zCalScaling"))
        self.gridLayout_3.addWidget(self.zCalScaling, 2, 1, 1, 1)
        self.label_10 = QtGui.QLabel(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_3.addWidget(self.label_10, 0, 2, 1, 1)
        self.zCalOffset = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.zCalOffset.setMinimum(-2.0)
        self.zCalOffset.setMaximum(2.0)
        self.zCalOffset.setSingleStep(0.05)
        self.zCalOffset.setObjectName(_fromUtf8("zCalOffset"))
        self.gridLayout_3.addWidget(self.zCalOffset, 2, 3, 1, 1)
        self.xCalOffset = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.xCalOffset.setMinimum(-2.0)
        self.xCalOffset.setMaximum(2.0)
        self.xCalOffset.setSingleStep(0.05)
        self.xCalOffset.setObjectName(_fromUtf8("xCalOffset"))
        self.gridLayout_3.addWidget(self.xCalOffset, 0, 3, 1, 1)
        self.label_11 = QtGui.QLabel(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_3.addWidget(self.label_11, 1, 2, 1, 1)
        self.label_12 = QtGui.QLabel(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_3.addWidget(self.label_12, 2, 2, 1, 1)
        self.yCalOffset = QtGui.QDoubleSpinBox(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yCalOffset.sizePolicy().hasHeightForWidth())
        self.yCalOffset.setSizePolicy(sizePolicy)
        self.yCalOffset.setMinimum(-2.0)
        self.yCalOffset.setMaximum(2.0)
        self.yCalOffset.setSingleStep(0.05)
        self.yCalOffset.setProperty("value", 0.0)
        self.yCalOffset.setObjectName(_fromUtf8("yCalOffset"))
        self.gridLayout_3.addWidget(self.yCalOffset, 1, 3, 1, 1)
        self.label_13 = QtGui.QLabel(self.groupBox_4)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_3.addWidget(self.label_13, 0, 4, 1, 1)
        self.label_14 = QtGui.QLabel(self.groupBox_4)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_3.addWidget(self.label_14, 1, 4, 1, 1)
        self.label_15 = QtGui.QLabel(self.groupBox_4)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout_3.addWidget(self.label_15, 2, 4, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_4)
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.logWindow = QtGui.QPlainTextEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logWindow.sizePolicy().hasHeightForWidth())
        self.logWindow.setSizePolicy(sizePolicy)
        self.logWindow.setObjectName(_fromUtf8("logWindow"))
        self.verticalLayout_2.addWidget(self.logWindow)
        self.rateLabel = QtGui.QLabel(self.groupBox_2)
        self.rateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.rateLabel.setObjectName(_fromUtf8("rateLabel"))
        self.verticalLayout_2.addWidget(self.rateLabel)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout.setStretch(0, 2)
        SamplerWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(SamplerWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1151, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        SamplerWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(SamplerWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        SamplerWindow.setStatusBar(self.statusbar)
        self.actionSave_Profile_As = QtGui.QAction(SamplerWindow)
        self.actionSave_Profile_As.setObjectName(_fromUtf8("actionSave_Profile_As"))
        self.actionOpen_Profile = QtGui.QAction(SamplerWindow)
        self.actionOpen_Profile.setObjectName(_fromUtf8("actionOpen_Profile"))
        self.actionQuit = QtGui.QAction(SamplerWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.menuFile.addAction(self.actionSave_Profile_As)
        self.menuFile.addAction(self.actionOpen_Profile)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(SamplerWindow)
        QtCore.QMetaObject.connectSlotsByName(SamplerWindow)

    def retranslateUi(self, SamplerWindow):
        SamplerWindow.setWindowTitle(_translate("SamplerWindow", "Mame Sampler", None))
        self.groupBox.setTitle(_translate("SamplerWindow", "Output Options", None))
        self.sampleName.setItemText(0, _translate("SamplerWindow", "test", None))
        self.sampleName.setItemText(1, _translate("SamplerWindow", "flat_on_table", None))
        self.sampleName.setItemText(2, _translate("SamplerWindow", "holding_steady", None))
        self.sampleName.setItemText(3, _translate("SamplerWindow", "bang_on_table", None))
        self.sampleName.setItemText(4, _translate("SamplerWindow", "drop_on_table", None))
        self.sampleName.setItemText(5, _translate("SamplerWindow", "pick_up_table", None))
        self.label.setText(_translate("SamplerWindow", "Directory", None))
        self.label_5.setText(_translate("SamplerWindow", "Sample Name", None))
        self.outputDirectory.setText(_translate("SamplerWindow", "~/accel-data/", None))
        self.groupBox_3.setTitle(_translate("SamplerWindow", "Capture", None))
        self.label_2.setText(_translate("SamplerWindow", "Num Samples", None))
        self.numSamples.setSuffix(_translate("SamplerWindow", " samples", None))
        self.label_3.setText(_translate("SamplerWindow", "Delay", None))
        self.delay.setSuffix(_translate("SamplerWindow", " seconds", None))
        self.label_4.setText(_translate("SamplerWindow", "Wait Progress", None))
        self.label_7.setText(_translate("SamplerWindow", "Capture Progress", None))
        self.cancelButton.setText(_translate("SamplerWindow", "Cancel Last Capture", None))
        self.startCaptureButton.setText(_translate("SamplerWindow", "Start", None))
        self.groupBox_4.setTitle(_translate("SamplerWindow", "Calibration", None))
        self.label_6.setText(_translate("SamplerWindow", "X_fixed =", None))
        self.label_8.setText(_translate("SamplerWindow", "Y_fixed =", None))
        self.label_9.setText(_translate("SamplerWindow", "Z_fixed =", None))
        self.label_10.setText(_translate("SamplerWindow", "* ( X +", None))
        self.label_11.setText(_translate("SamplerWindow", "* ( Y +", None))
        self.label_12.setText(_translate("SamplerWindow", "* ( Z +", None))
        self.label_13.setText(_translate("SamplerWindow", ")", None))
        self.label_14.setText(_translate("SamplerWindow", ")", None))
        self.label_15.setText(_translate("SamplerWindow", ")", None))
        self.groupBox_2.setTitle(_translate("SamplerWindow", "Log", None))
        self.rateLabel.setText(_translate("SamplerWindow", "x samples/second", None))
        self.menuFile.setTitle(_translate("SamplerWindow", "File", None))
        self.actionSave_Profile_As.setText(_translate("SamplerWindow", "Save Profile As...", None))
        self.actionSave_Profile_As.setShortcut(_translate("SamplerWindow", "Ctrl+S", None))
        self.actionOpen_Profile.setText(_translate("SamplerWindow", "Open Profile", None))
        self.actionOpen_Profile.setShortcut(_translate("SamplerWindow", "Ctrl+O", None))
        self.actionQuit.setText(_translate("SamplerWindow", "Quit", None))
        self.actionQuit.setShortcut(_translate("SamplerWindow", "Ctrl+Q", None))

from PyQt4.Qwt5 import *
