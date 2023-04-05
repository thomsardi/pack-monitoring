import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg

import json
import os
from ...definition import RESOURCES_DIR

from ..chargerwindow import Ui_ChargerWindow
from ...modules.Command import Command
from ...modules.ChargerRequest import ChargerRequest

class ChargerWindow(qtw.QWidget) :
    command = qtc.pyqtSignal(Command)
    isChargerStart = qtc.pyqtSignal(int)
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.ui = Ui_ChargerWindow()
        self.ui.setupUi(self)
        self.ui.startchargerpushButton.clicked.connect(self.startClicked)
        self.ui.chargervoltageapplypushButton.clicked.connect(self.voltageApplyClicked)
        self.ui.chargercurrentapplypushButton.clicked.connect(self.currentApplyClicked)
        self.isChargerStart = 0
        self.activeWidgetIndex = 0

    def startClicked(self) :
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        arrData = data['ip_list']
        url : str = ""
        ip : str = ""
        for x in arrData :
            if x['number'] == self.activeWidgetIndex+1 :
                url = x['charger_url']['module32_url']
                ip = x['charger_url']['ip']
                break
        
        url = url.replace("%ip", ip)
        value = 0
        if(self.ui.chargercheckBox_1.isChecked()) :
            temp = 1 << 1
            value += temp
        if(self.ui.chargercheckBox_2.isChecked()) :
            temp = 1 << 2
            value += temp
        if(self.ui.chargercheckBox_3.isChecked()) :
            temp = 1 << 3
            value += temp
        command = Command()
        r = ChargerRequest()
        command = r.setModule32(0, value, url)
        self.command.emit(command)
        if (value > 0) :
            self.isChargerStart = 1
        else :
            self.isChargerStart = 0

    def stop(self) :
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        arrData = data['ip_list']
        url : str = ""
        ip : str = ""
        for x in arrData :
            if x['number'] == self.activeWidgetIndex+1 :
                url = x['charger_url']['module32_url']
                ip = x['charger_url']['ip']
                break
        
        url = url.replace("%ip", ip)
        value = 0
        command = Command()
        r = ChargerRequest()
        command = r.setModule32(0, value, url)
        self.command.emit(command)
        self.isChargerStart = 0
    
    def voltageApplyClicked(self) :
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        arrData = data['ip_list']
        url : str = ""
        ip : str = ""
        for x in arrData :
            if x['number'] == self.activeWidgetIndex+1 :
                url = x['charger_url']['voltage_url']
                ip = x['charger_url']['ip']
                break
        
        url = url.replace("%ip", ip)
        group = self.ui.chargervoltagegroupspinBox.value()
        subAddress = self.ui.chargervoltagesubaddressspinBox.value()
        value = self.ui.chargervoltagespinBox.value()
        command = Command()
        r = ChargerRequest()
        command = r.setVoltage(group, subAddress, value, url)
        self.command.emit(command)

    def currentApplyClicked(self) :
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        arrData = data['ip_list']
        url : str = ""
        ip : str = ""
        for x in arrData :
            if x['number'] == self.activeWidgetIndex+1 :
                url = x['charger_url']['current_url']
                ip = x['charger_url']['ip']
                break
        
        url = url.replace("%ip", ip)
        group = self.ui.chargercurrentgroupspinBox.value()
        subAddress = self.ui.chargercurrentsubaddressspinBox.value()
        value = self.ui.chargercurrentspinBox.value()
        command = Command()
        r = ChargerRequest()
        command = r.setCurrent(group, subAddress, value, url)
        self.command.emit(command)

    def updateIpLineEdit(self, ipName : str) :
        self.ui.ipAddressLineEdit.setText(ipName)

    def setActiveWidgetIndex(self, index) :
        self.activeWidgetIndex = index

    def showMessageBox(self, status : int) :
        msg = qtw.QMessageBox()
        msg.setWindowTitle("Send Status")
        if(status >= 0) :
            msg.setText("Command Sent")
            msg.setIcon(qtw.QMessageBox.Information)
        else :
            msg.setText("Command Send Failed")
            msg.setIcon(qtw.QMessageBox.Critical)
        msg.exec()

if __name__ == "__main__":
    import sys
    app = qtw.QApplication(sys.argv)
    widget = ChargerWindow()
    widget.show()
    app.exec_()