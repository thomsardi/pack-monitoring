# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inverterwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InverterWindow(object):
    def setupUi(self, InverterWindow):
        InverterWindow.setObjectName("InverterWindow")
        InverterWindow.resize(288, 352)
        InverterWindow.setMaximumSize(QtCore.QSize(2000, 2000))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/resources/icons/solar-inverter-crop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        InverterWindow.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(InverterWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(InverterWindow)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_13 = QtWidgets.QLabel(self.frame)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_4.addWidget(self.label_13)
        self.line_2 = QtWidgets.QFrame(self.frame)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_4.addWidget(self.line_2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 6, 2, 1, 1)
        self.invertervoltagecutoffspinBox_2 = QtWidgets.QSpinBox(self.frame)
        self.invertervoltagecutoffspinBox_2.setEnabled(False)
        self.invertervoltagecutoffspinBox_2.setMaximum(1500000)
        self.invertervoltagecutoffspinBox_2.setProperty("value", 768000)
        self.invertervoltagecutoffspinBox_2.setObjectName("invertervoltagecutoffspinBox_2")
        self.gridLayout_2.addWidget(self.invertervoltagecutoffspinBox_2, 4, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 3, 2, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.frame)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 4, 2, 1, 1)
        self.invertermodecomboBox = QtWidgets.QComboBox(self.frame)
        self.invertermodecomboBox.setObjectName("invertermodecomboBox")
        self.invertermodecomboBox.addItem("")
        self.invertermodecomboBox.addItem("")
        self.invertermodecomboBox.addItem("")
        self.gridLayout_2.addWidget(self.invertermodecomboBox, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 4, 0, 1, 1)
        self.invertervoltagecutoffspinBox_1 = QtWidgets.QSpinBox(self.frame)
        self.invertervoltagecutoffspinBox_1.setEnabled(False)
        self.invertervoltagecutoffspinBox_1.setMaximum(1000000)
        self.invertervoltagecutoffspinBox_1.setProperty("value", 793600)
        self.invertervoltagecutoffspinBox_1.setObjectName("invertervoltagecutoffspinBox_1")
        self.gridLayout_2.addWidget(self.invertervoltagecutoffspinBox_1, 3, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 5, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 5, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 6, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.frame)
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.label_14, 0, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.frame)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 2, 2, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.frame)
        self.label_15.setObjectName("label_15")
        self.gridLayout_2.addWidget(self.label_15, 2, 0, 1, 1)
        self.invertercurrentspinBox = QtWidgets.QSpinBox(self.frame)
        self.invertercurrentspinBox.setMaximum(120000)
        self.invertercurrentspinBox.setProperty("value", 5000)
        self.invertercurrentspinBox.setObjectName("invertercurrentspinBox")
        self.gridLayout_2.addWidget(self.invertercurrentspinBox, 5, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)
        self.inverterchargevoltagespinBox = QtWidgets.QSpinBox(self.frame)
        self.inverterchargevoltagespinBox.setEnabled(True)
        self.inverterchargevoltagespinBox.setMaximum(1000000)
        self.inverterchargevoltagespinBox.setProperty("value", 921600)
        self.inverterchargevoltagespinBox.setObjectName("inverterchargevoltagespinBox")
        self.gridLayout_2.addWidget(self.inverterchargevoltagespinBox, 2, 1, 1, 1)
        self.invertercontroltypecomboBox = QtWidgets.QComboBox(self.frame)
        self.invertercontroltypecomboBox.setObjectName("invertercontroltypecomboBox")
        self.invertercontroltypecomboBox.addItem("")
        self.invertercontroltypecomboBox.addItem("")
        self.gridLayout_2.addWidget(self.invertercontroltypecomboBox, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.inverterpowerdoubleSpinBox = QtWidgets.QDoubleSpinBox(self.frame)
        self.inverterpowerdoubleSpinBox.setEnabled(False)
        self.inverterpowerdoubleSpinBox.setMaximum(1000000.0)
        self.inverterpowerdoubleSpinBox.setObjectName("inverterpowerdoubleSpinBox")
        self.gridLayout_2.addWidget(self.inverterpowerdoubleSpinBox, 6, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 3, 3, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 6)
        self.gridLayout_2.setColumnStretch(1, 12)
        self.gridLayout_2.setColumnStretch(2, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.startrinverterpushButton = QtWidgets.QPushButton(self.frame)
        self.startrinverterpushButton.setObjectName("startrinverterpushButton")
        self.horizontalLayout_4.addWidget(self.startrinverterpushButton)
        self.stopinverterpushButton = QtWidgets.QPushButton(self.frame)
        self.stopinverterpushButton.setObjectName("stopinverterpushButton")
        self.horizontalLayout_4.addWidget(self.stopinverterpushButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 2, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(InverterWindow)
        QtCore.QMetaObject.connectSlotsByName(InverterWindow)

    def retranslateUi(self, InverterWindow):
        _translate = QtCore.QCoreApplication.translate
        InverterWindow.setWindowTitle(_translate("InverterWindow", "Bidirectional Inverter System"))
        self.label_13.setText(_translate("InverterWindow", "Parameter"))
        self.label_8.setText(_translate("InverterWindow", "kW"))
        self.label_5.setText(_translate("InverterWindow", "mV"))
        self.label_11.setText(_translate("InverterWindow", "mV"))
        self.invertermodecomboBox.setItemText(0, _translate("InverterWindow", "Charge"))
        self.invertermodecomboBox.setItemText(1, _translate("InverterWindow", "Discharge"))
        self.invertermodecomboBox.setItemText(2, _translate("InverterWindow", "Cycling"))
        self.label_7.setText(_translate("InverterWindow", "Voltage LL Cut Off"))
        self.label_9.setText(_translate("InverterWindow", "Current"))
        self.label_6.setText(_translate("InverterWindow", "mA"))
        self.label_4.setText(_translate("InverterWindow", "Power"))
        self.label_14.setText(_translate("InverterWindow", "Mode"))
        self.label_12.setText(_translate("InverterWindow", "mV"))
        self.label_15.setText(_translate("InverterWindow", "Voltage"))
        self.label_3.setText(_translate("InverterWindow", "Voltage L Cut Off"))
        self.invertercontroltypecomboBox.setItemText(0, _translate("InverterWindow", "Constant Current"))
        self.invertercontroltypecomboBox.setItemText(1, _translate("InverterWindow", "Constant Power"))
        self.label_2.setText(_translate("InverterWindow", "Control Mode"))
        self.startrinverterpushButton.setText(_translate("InverterWindow", "Start"))
        self.stopinverterpushButton.setText(_translate("InverterWindow", "Stop"))
        self.label.setText(_translate("InverterWindow", "Bidirectional Inverter System"))
import res_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    InverterWindow = QtWidgets.QWidget()
    ui = Ui_InverterWindow()
    ui.setupUi(InverterWindow)
    InverterWindow.show()
    sys.exit(app.exec_())
