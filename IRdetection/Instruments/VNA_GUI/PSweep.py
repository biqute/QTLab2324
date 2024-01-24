# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PSweep.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import HP8753E as hp
from par_dialog import Ui_Dialog as uid
import time
from pathlib import Path
import numpy as np


class Ui_PSWeep(object):

    _I = None
    _Q = None
    _F = None
    
    num = 0 

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(198, 175, 175))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 215, 215))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 87, 87))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(132, 117, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(198, 175, 175))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 215, 215))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(198, 175, 175))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 215, 215))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 87, 87))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(132, 117, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(198, 175, 175))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 215, 215))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 87, 87))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(198, 175, 175))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 215, 215))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 87, 87))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(132, 117, 117))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 87, 87))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 87, 87))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(198, 175, 175))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(198, 175, 175))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(198, 175, 175))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        MainWindow.setPalette(palette)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.page_title = QtWidgets.QLabel(self.centralwidget)
        self.page_title.setGeometry(QtCore.QRect(330, 20, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.page_title.setFont(font)
        self.page_title.setFrameShape(QtWidgets.QFrame.Box)
        self.page_title.setLineWidth(3)
        self.page_title.setAlignment(QtCore.Qt.AlignCenter)
        self.page_title.setObjectName("page_title")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 90, 401, 441))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.Set_power_start_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Set_power_start_pushButton.sizePolicy().hasHeightForWidth())
        self.Set_power_start_pushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Set_power_start_pushButton.setFont(font)
        self.Set_power_start_pushButton.setObjectName("Set Power Start")
        self.gridLayout.addWidget(self.Set_power_start_pushButton, 0, 1, 1, 1)
        self.Set_IFBW_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Set_IFBW_pushButton.sizePolicy().hasHeightForWidth())
        self.Set_IFBW_pushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Set_IFBW_pushButton.setFont(font)
        self.Set_IFBW_pushButton.setObjectName("Set_IFBW_pushButton")
        self.gridLayout.addWidget(self.Set_IFBW_pushButton, 3, 1, 1, 1)
        self.Set_points_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Set_points_pushButton.sizePolicy().hasHeightForWidth())
        self.Set_points_pushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Set_points_pushButton.setFont(font)
        self.Set_points_pushButton.setObjectName("Set_points_pushButton")
        self.gridLayout.addWidget(self.Set_points_pushButton, 2, 1, 1, 1)
        self.Set_power_stop_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Set_power_stop_pushButton.sizePolicy().hasHeightForWidth())
        self.Set_power_stop_pushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Set_power_stop_pushButton.setFont(font)
        self.Set_power_stop_pushButton.setObjectName("Set_power_stop_pushButton")
        self.gridLayout.addWidget(self.Set_power_stop_pushButton, 1, 1, 1, 1)
        self.power_start_lcd = QtWidgets.QLCDNumber(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.power_start_lcd.sizePolicy().hasHeightForWidth())
        self.power_start_lcd.setSizePolicy(sizePolicy)
        self.power_start_lcd.setFrameShadow(QtWidgets.QFrame.Plain)
        self.power_start_lcd.setLineWidth(3)
        self.power_start_lcd.setObjectName("power_start_lcd")
        self.gridLayout.addWidget(self.power_start_lcd, 0, 0, 1, 1)
        self.IFBW_lcd = QtWidgets.QLCDNumber(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IFBW_lcd.sizePolicy().hasHeightForWidth())
        self.IFBW_lcd.setSizePolicy(sizePolicy)
        self.IFBW_lcd.setFrameShadow(QtWidgets.QFrame.Plain)
        self.IFBW_lcd.setLineWidth(3)
        self.IFBW_lcd.setObjectName("IFBW_lcd")
        self.gridLayout.addWidget(self.IFBW_lcd, 3, 0, 1, 1)
        self.power_stop_lcd = QtWidgets.QLCDNumber(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.power_stop_lcd.sizePolicy().hasHeightForWidth())
        self.power_stop_lcd.setSizePolicy(sizePolicy)
        self.power_stop_lcd.setFrameShadow(QtWidgets.QFrame.Plain)
        self.power_stop_lcd.setLineWidth(3)
        self.power_stop_lcd.setObjectName("power_stop_lcd")
        self.gridLayout.addWidget(self.power_stop_lcd, 1, 0, 1, 1)
        self.points_num_lcd = QtWidgets.QLCDNumber(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.points_num_lcd.sizePolicy().hasHeightForWidth())
        self.points_num_lcd.setSizePolicy(sizePolicy)
        self.points_num_lcd.setFrameShadow(QtWidgets.QFrame.Plain)
        self.points_num_lcd.setLineWidth(3)
        self.points_num_lcd.setObjectName("points_num_lcd")
        self.gridLayout.addWidget(self.points_num_lcd, 2, 0, 1, 1)
        self.cp_label = QtWidgets.QLabel(self.centralwidget)
        self.cp_label.setGeometry(QtCore.QRect(530, 90, 210, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.cp_label.setFont(font)
        self.cp_label.setFrameShape(QtWidgets.QFrame.Box)
        self.cp_label.setLineWidth(3)
        self.cp_label.setAlignment(QtCore.Qt.AlignCenter)
        self.cp_label.setObjectName("cp_label")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(530, 150, 211, 381))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.current_power_lcd = QtWidgets.QLCDNumber(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.current_power_lcd.sizePolicy().hasHeightForWidth())
        self.current_power_lcd.setSizePolicy(sizePolicy)
        self.current_power_lcd.setFrameShadow(QtWidgets.QFrame.Plain)
        self.current_power_lcd.setLineWidth(3)
        self.current_power_lcd.setObjectName("current_power_lcd")
        self.verticalLayout.addWidget(self.current_power_lcd)
        self.progressBar = QtWidgets.QProgressBar(self.verticalLayoutWidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.GET_IQF_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GET_IQF_pushButton.sizePolicy().hasHeightForWidth())
        self.GET_IQF_pushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.GET_IQF_pushButton.setFont(font)
        self.GET_IQF_pushButton.setObjectName("GET_IQF_pushButton")
        self.verticalLayout.addWidget(self.GET_IQF_pushButton)
        self.crf_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.crf_pushButton.sizePolicy().hasHeightForWidth())
        self.crf_pushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.crf_pushButton.setFont(font)
        self.crf_pushButton.setObjectName("crf_pushButton")
        self.verticalLayout.addWidget(self.crf_pushButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_Set_IQF_Parameters = QtWidgets.QAction(MainWindow)
        self.action_Set_IQF_Parameters.setObjectName("action_Set_IQF_Parameters")
        self.action_Set_Main_Parameters = QtWidgets.QAction(MainWindow)
        self.action_Set_Main_Parameters.setObjectName("action_Set_Main_Parameters")
        self.menuMenu.addAction(self.action_Set_Main_Parameters)
        self.menuMenu.addAction(self.action_Set_IQF_Parameters)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.Set_IFBW_pushButton.clicked.connect(self.set_IFBW)
        self.Set_points_pushButton.clicked.connect(self.set_points)
        self.Set_power_start_pushButton.clicked.connect(self.set_power_start)
        self.Set_power_stop_pushButton.clicked.connect(self.set_power_stop)
        self.GET_IQF_pushButton.clicked.connect(self.Power_sweep)
        self.crf_pushButton.clicked.connect(self.crf)

        #self.action_Set_Main_Parameters.triggered.connect(self.MainParamsWidget)
        #self.action_Set_IQF_Parameters.triggered.connect(self.ParamsWidget)s

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.page_title.setText(_translate("MainWindow", "POWER SWEEP"))
        self.Set_power_start_pushButton.setText(_translate("MainWindow", "SET POWER START"))
        self.Set_IFBW_pushButton.setText(_translate("MainWindow", "SET IFBW"))
        self.Set_points_pushButton.setText(_translate("MainWindow", "SET POINTS NUMBER"))
        self.Set_power_stop_pushButton.setText(_translate("MainWindow", "SET POWER STOP"))
        self.cp_label.setText(_translate("MainWindow", "CURRENT POWER"))
        self.GET_IQF_pushButton.setText(_translate("MainWindow", "POWER SWEEP"))
        self.crf_pushButton.setText(_translate("MainWindow", "CREATE HDF5"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.action_Set_Main_Parameters.setText(_translate("MainWindow", "Set Main Parameters"))
        self.action_Set_IQF_Parameters.setText(_translate("MainWindow", "Set IQF Parameters"))
        self.show_params()

    def Power_sweep(self):
        vna = hp.HP8753E()
        powers = np.arange(vna._params['power_start'],vna._params['power_stop'], 5)
        for pow in powers:
            vna.set_params(pow, bw=vna._params['IFBW'], pt = vna._params['points'], start=vna._params['start'], span = vna._params['span'])
            time.sleep(1)
            self._I, self._Q, self._F = vna.get_IQF_single_meas()
            self.crf()
        return

    def show_params(self):
        vna = hp.HP8753E()
        self.power_start_lcd.display(vna._params['power_start'])
        self.power_stop_lcd.display(vna._params['power_stop'])
        self.IFBW_lcd.display(vna._params['IFBW'])
        self.points_num_lcd.display(vna._params['points'])
        self.current_power_lcd.display(vna._params['power'])

    def set_IFBW(self):
        vna = hp.HP8753E()
        Dialog = QtWidgets.QDialog()
        ui = uid()
        ui.setupUi(Dialog)
        if Dialog.exec_():
            self.IFBW_lcd.display(ui.test_value)
            vna.set_IFBW(float(ui.test_value))
            print('IFBW: ', vna.get_IFBW())
        return 

    def set_points(self):
        vna = hp.HP8753E()
        Dialog = QtWidgets.QDialog()
        ui = uid()
        ui.setupUi(Dialog)
        if Dialog.exec_():
            self.points_lcd.display(ui.test_value)
            vna.set_points(float(ui.test_value))
            print('Points: ', vna.get_points())
        return 

    def set_power_start(self):
        vna = hp.HP8753E()
        Dialog = QtWidgets.QDialog()
        ui = uid()
        ui.setupUi(Dialog)
        if Dialog.exec_():
            self.power_start_lcd.display('-'+str(ui.test_value))
            vna.set_power_start(0 - float(ui.test_value))
        return 

    def set_power_stop(self):
        vna = hp.HP8753E()
        Dialog = QtWidgets.QDialog()
        ui = uid()
        ui.setupUi(Dialog)
        if Dialog.exec_():
            self.power_stop_lcd.display('-'+str(ui.test_value))
            vna.set_power_stop(0 - float(ui.test_value))
        return 


    def Get_IQF(self):
        vna = hp.HP8753E()
        self._I, self._Q, self._F = vna.get_IQF_single_meas()
        sleep = vna.get_span()/vna.get_IFBW()
        for i in range(0,int(sleep)):
            self.progressBar.setValue(i) 
        time.sleep(2)
        return

    def crf(self):
        vna = hp.HP8753E()
        vna.set_save_path("C:\\Users\\kid\\SynologyDrive\\Lab2023\\KIDs\\QTLab2324\\IRdetection\\Instruments\\PSweep_test\\")
        myfile = Path(str(vna._path)+"PowerSweep_"+str(self.num)+".h5")
        if (myfile.is_file()==True):
            print('File exists already!')
            self.num = self.num + 1
            vna.create_run_file(num=self.num, i=self._I,q=self._Q,f=self._F)
        else:
            vna.create_run_file(num=self.num, i=self._I,q=self._Q,f=self._F)
            print('File does not exist') 
        self.progressBar.reset()
        return


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wg = QtWidgets.QMainWindow()
    ui = Ui_PSWeep()
    ui.setupUi(wg)
    wg.show()
    sys.exit(app.exec_())