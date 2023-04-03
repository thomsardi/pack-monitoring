import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg

import json
import os
from ...definition import RESOURCES_DIR

from ..inverterwindow import Ui_InverterWindow
from ...modules.Command import Command
from ...modules.InverterRequest import InverterRequest

class InverterWindow(qtw.QWidget) :
    command = qtc.pyqtSignal(Command)
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.win = Ui_InverterWindow()
        self.win.setupUi(self)
        self.win.startrinverterpushButton.clicked.connect(self.startClicked)
        self.win.stopinverterpushButton.clicked.connect(self.stopClicked)
        # self.win.applyparameterinverterpushButton.clicked.connect(self.parameterApplyClicked)
        self.win.invertermodecomboBox.currentIndexChanged.connect(self.modeIndexChanged)
        self.win.invertercontroltypecomboBox.currentIndexChanged.connect(self.controlTypeIndexChanged)

    def startClicked(self) :
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        mode = self.win.invertermodecomboBox.currentIndex()
        controlType = self.win.invertercontroltypecomboBox.currentIndex()
        chargeVoltage = self.win.inverterchargevoltagespinBox.value()
        voltageCutOff1 = self.win.invertervoltagecutoffspinBox_1.value()
        voltageCutOff2 = self.win.invertervoltagecutoffspinBox_2.value()
        current = self.win.invertercurrentspinBox.value()
        power = round(self.win.inverterpowerdoubleSpinBox.value() * 1000000) #convert to mW (miliWatts)
        data = json.load(f)
        ip = data['app_url']['ip']
        url = str(data['app_url']['parameter_url'])
        url = url.replace("%ip", ip)
        command = Command()
        r = InverterRequest()
        command = r.setParameter(controlType, mode, chargeVoltage, voltageCutOff1, voltageCutOff2, current, power, 1, url)
        self.command.emit(command)
    
    def stopClicked(self) :
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        mode = self.win.invertermodecomboBox.currentIndex()
        controlType = self.win.invertercontroltypecomboBox.currentIndex()
        chargeVoltage = self.win.inverterchargevoltagespinBox.value()
        voltageCutOff1 = self.win.invertervoltagecutoffspinBox_1.value()
        voltageCutOff2 = self.win.invertervoltagecutoffspinBox_2.value()
        current = self.win.invertercurrentspinBox.value()
        power = round(self.win.inverterpowerdoubleSpinBox.value() * 1000000) #convert to mW (miliWatts)
        data = json.load(f)
        ip = data['app_url']['ip']
        url = str(data['app_url']['parameter_url'])
        url = url.replace("%ip", ip)
        command = Command()
        r = InverterRequest()
        command = r.setParameter(controlType, mode, chargeVoltage, voltageCutOff1, voltageCutOff2, current, power, 0, url)
        self.command.emit(command)
    
    def modeIndexChanged(self) :
        index = self.win.invertermodecomboBox.currentIndex()
        if(index == 0) : #charge mode
            self.win.inverterchargevoltagespinBox.setEnabled(True)
            self.win.invertervoltagecutoffspinBox_1.setEnabled(False)
            self.win.invertervoltagecutoffspinBox_2.setEnabled(False)
        elif(index == 1) : #discharge mode
            self.win.inverterchargevoltagespinBox.setEnabled(False)
            self.win.invertervoltagecutoffspinBox_1.setEnabled(True)
            self.win.invertervoltagecutoffspinBox_2.setEnabled(True)
        elif(index == 2) : #cycling mode
            self.win.inverterchargevoltagespinBox.setEnabled(True)
            self.win.invertervoltagecutoffspinBox_1.setEnabled(True)
            self.win.invertervoltagecutoffspinBox_2.setEnabled(True)

    def controlTypeIndexChanged(self) :
        index = self.win.invertercontroltypecomboBox.currentIndex()
        if(index == 0) : #constant current mode
            self.win.invertercurrentspinBox.setEnabled(True)
            self.win.inverterpowerdoubleSpinBox.setEnabled(False)
        elif(index == 1) : #constant power mode
            self.win.invertercurrentspinBox.setEnabled(False)
            self.win.inverterpowerdoubleSpinBox.setEnabled(True)        
    
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
    widget = InverterWindow()
    widget.show()
    app.exec_()