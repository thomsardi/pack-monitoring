# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chargerwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ChargerWindow(object):
    def setupUi(self, ChargerWindow):
        ChargerWindow.setObjectName("ChargerWindow")
        ChargerWindow.resize(450, 390)
        ChargerWindow.setMaximumSize(QtCore.QSize(450, 390))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/resources/icons/charger.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ChargerWindow.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(ChargerWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(ChargerWindow)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 1)
        self.line_8 = QtWidgets.QFrame(self.frame)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.gridLayout.addWidget(self.line_8, 7, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 9, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.frame)
        self.label_20.setObjectName("label_20")
        self.gridLayout_3.addWidget(self.label_20, 0, 0, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.frame)
        self.label_22.setObjectName("label_22")
        self.gridLayout_3.addWidget(self.label_22, 2, 0, 1, 1)
        self.chargervoltageapplypushButton = QtWidgets.QPushButton(self.frame)
        self.chargervoltageapplypushButton.setObjectName("chargervoltageapplypushButton")
        self.gridLayout_3.addWidget(self.chargervoltageapplypushButton, 4, 0, 1, 1)
        self.chargervoltagesubaddressspinBox = QtWidgets.QSpinBox(self.frame)
        self.chargervoltagesubaddressspinBox.setObjectName("chargervoltagesubaddressspinBox")
        self.gridLayout_3.addWidget(self.chargervoltagesubaddressspinBox, 2, 1, 1, 1)
        self.chargervoltagegroupspinBox = QtWidgets.QSpinBox(self.frame)
        self.chargervoltagegroupspinBox.setObjectName("chargervoltagegroupspinBox")
        self.gridLayout_3.addWidget(self.chargervoltagegroupspinBox, 1, 1, 1, 1)
        self.chargervoltagespinBox = QtWidgets.QSpinBox(self.frame)
        self.chargervoltagespinBox.setMaximum(1000000)
        self.chargervoltagespinBox.setObjectName("chargervoltagespinBox")
        self.gridLayout_3.addWidget(self.chargervoltagespinBox, 3, 1, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.frame)
        self.label_23.setObjectName("label_23")
        self.gridLayout_3.addWidget(self.label_23, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 3, 2, 1, 1)
        self.gridLayout_3.setColumnStretch(0, 6)
        self.gridLayout_3.setColumnStretch(1, 6)
        self.gridLayout_3.setColumnStretch(2, 1)
        self.horizontalLayout.addLayout(self.gridLayout_3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.line_9 = QtWidgets.QFrame(self.frame)
        self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.horizontalLayout.addWidget(self.line_9)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_27 = QtWidgets.QLabel(self.frame)
        self.label_27.setObjectName("label_27")
        self.gridLayout_4.addWidget(self.label_27, 1, 0, 1, 1)
        self.chargercurrentgroupspinBox = QtWidgets.QSpinBox(self.frame)
        self.chargercurrentgroupspinBox.setObjectName("chargercurrentgroupspinBox")
        self.gridLayout_4.addWidget(self.chargercurrentgroupspinBox, 1, 1, 1, 1)
        self.chargercurrentspinBox = QtWidgets.QSpinBox(self.frame)
        self.chargercurrentspinBox.setMaximum(150000)
        self.chargercurrentspinBox.setObjectName("chargercurrentspinBox")
        self.gridLayout_4.addWidget(self.chargercurrentspinBox, 3, 1, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.frame)
        self.label_26.setObjectName("label_26")
        self.gridLayout_4.addWidget(self.label_26, 2, 0, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.frame)
        self.label_25.setObjectName("label_25")
        self.gridLayout_4.addWidget(self.label_25, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 3, 0, 1, 1)
        self.chargercurrentsubaddressspinBox = QtWidgets.QSpinBox(self.frame)
        self.chargercurrentsubaddressspinBox.setObjectName("chargercurrentsubaddressspinBox")
        self.gridLayout_4.addWidget(self.chargercurrentsubaddressspinBox, 2, 1, 1, 1)
        self.chargercurrentapplypushButton = QtWidgets.QPushButton(self.frame)
        self.chargercurrentapplypushButton.setObjectName("chargercurrentapplypushButton")
        self.gridLayout_4.addWidget(self.chargercurrentapplypushButton, 4, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 3, 2, 1, 1)
        self.gridLayout_4.setColumnStretch(0, 6)
        self.gridLayout_4.setColumnStretch(1, 6)
        self.gridLayout_4.setColumnStretch(2, 1)
        self.horizontalLayout.addLayout(self.gridLayout_4)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.gridLayout.addLayout(self.horizontalLayout, 8, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.frame)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 4, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.chargercheckBox_1 = QtWidgets.QCheckBox(self.frame)
        self.chargercheckBox_1.setChecked(True)
        self.chargercheckBox_1.setObjectName("chargercheckBox_1")
        self.verticalLayout_3.addWidget(self.chargercheckBox_1)
        self.chargercheckBox_2 = QtWidgets.QCheckBox(self.frame)
        self.chargercheckBox_2.setChecked(True)
        self.chargercheckBox_2.setObjectName("chargercheckBox_2")
        self.verticalLayout_3.addWidget(self.chargercheckBox_2)
        self.chargercheckBox_3 = QtWidgets.QCheckBox(self.frame)
        self.chargercheckBox_3.setChecked(True)
        self.chargercheckBox_3.setObjectName("chargercheckBox_3")
        self.verticalLayout_3.addWidget(self.chargercheckBox_3)
        self.startchargerpushButton = QtWidgets.QPushButton(self.frame)
        self.startchargerpushButton.setObjectName("startchargerpushButton")
        self.verticalLayout_3.addWidget(self.startchargerpushButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.gridLayout.addLayout(self.horizontalLayout_2, 5, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(ChargerWindow)
        QtCore.QMetaObject.connectSlotsByName(ChargerWindow)

    def retranslateUi(self, ChargerWindow):
        _translate = QtCore.QCoreApplication.translate
        ChargerWindow.setWindowTitle(_translate("ChargerWindow", "Charger System"))
        self.label_2.setText(_translate("ChargerWindow", "Parameter Setting"))
        self.label_7.setText(_translate("ChargerWindow", "Start / Stop Charger"))
        self.label_3.setText(_translate("ChargerWindow", "Voltage"))
        self.label_20.setText(_translate("ChargerWindow", "Voltage"))
        self.label_22.setText(_translate("ChargerWindow", "SubAddress"))
        self.chargervoltageapplypushButton.setText(_translate("ChargerWindow", "Apply"))
        self.label_23.setText(_translate("ChargerWindow", "Group"))
        self.label_4.setText(_translate("ChargerWindow", "mV"))
        self.label_27.setText(_translate("ChargerWindow", "Group"))
        self.label_26.setText(_translate("ChargerWindow", "SubAddress"))
        self.label_25.setText(_translate("ChargerWindow", "Current"))
        self.label_5.setText(_translate("ChargerWindow", "Current"))
        self.chargercurrentapplypushButton.setText(_translate("ChargerWindow", "Apply"))
        self.label_6.setText(_translate("ChargerWindow", "mA"))
        self.label.setText(_translate("ChargerWindow", "Charger System"))
        self.chargercheckBox_1.setText(_translate("ChargerWindow", "Charger 1"))
        self.chargercheckBox_2.setText(_translate("ChargerWindow", "Charger 2"))
        self.chargercheckBox_3.setText(_translate("ChargerWindow", "Charger 3"))
        self.startchargerpushButton.setText(_translate("ChargerWindow", "Apply"))
import res_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ChargerWindow = QtWidgets.QWidget()
    ui = Ui_ChargerWindow()
    ui.setupUi(ChargerWindow)
    ChargerWindow.show()
    sys.exit(app.exec_())
