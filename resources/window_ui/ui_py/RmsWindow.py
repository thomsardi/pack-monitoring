import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg

import json
import os
from ...definition import RESOURCES_DIR

from ..rmswindow import Ui_RmsWindow
from ...modules.Command import Command
from ...modules.RmsRequest import RmsRequest
from ...modules.ParameterData import VoltageParameter
from ...modules.ParameterData import TemperatureParameter

class RmsWindow(qtw.QWidget) :
    command = qtc.pyqtSignal(Command)
    voltageParameter = qtc.pyqtSignal(VoltageParameter)
    temperatureParameter = qtc.pyqtSignal(TemperatureParameter)
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.ui = Ui_RmsWindow()
        self.ui.setupUi(self)
        self.ui.addresspushButton.clicked.connect(self.addressClicked)
        self.ui.startdatapushButton.clicked.connect(self.startDataClicked)
        self.ui.stopdatapushButton.clicked.connect(self.stopDataClicked)
        self.ui.frameapplypushButton.clicked.connect(self.applyFrameClicked)
        self.ui.cmscodeapplypushButton.clicked.connect(self.applyCmsClicked)
        self.ui.basecodeapplypushButton.clicked.connect(self.applyBaseClicked)
        self.ui.mcucodeapplypushButton.clicked.connect(self.applyMcuClicked)
        self.ui.sitelocationapplypushButton.clicked.connect(self.applySiteClicked)
        self.ui.restartcmspushButton.clicked.connect(self.restartCmsClicked)
        self.ui.restartrmspushButton.clicked.connect(self.restartRmsClicked)
        self.ui.cellvoltageapplypushButton.clicked.connect(self.voltageParameterClicked)
        self.ui.temperatureapplypushButton.clicked.connect(self.temperatureParameterClicked)

    def addressClicked(self) :
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        ip = data['rms_url']['ip']
        url = str(data['rms_url']['address_url'])
        url = url.replace("%ip", ip)
        command = Command()
        r = RmsRequest()
        command = r.setAddress(1, url)
        self.command.emit(command)
    
    def startDataClicked(self) :
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        ip = data['rms_url']['ip']
        url = str(data['rms_url']['data_collection_url'])
        url = url.replace("%ip", ip)
        command = Command()
        r = RmsRequest()
        command = r.setDataCollection(1, url)
        self.command.emit(command)

    def stopDataClicked(self) :
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        ip = data['rms_url']['ip']
        url = str(data['rms_url']['data_collection_url'])
        url = url.replace("%ip", ip)
        command = Command()
        r = RmsRequest()
        command = r.setDataCollection(0, url)
        self.command.emit(command)

    def applyFrameClicked(self) :
        bid = self.ui.framebidspinBox.value()
        code = self.ui.framenamelineEdit.text()
        if (code == "") :
            return
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        ip = data['rms_url']['ip']
        url = str(data['rms_url']['frame_url'])
        url = url.replace("%ip", ip)
        command = Command()
        r = RmsRequest()
        command = r.setFrame(bid, 1, code, url)
        self.command.emit(command)

    def applyCmsClicked(self) :
        bid = self.ui.cmscodebidspinBox.value()
        code = self.ui.cmscodelineEdit.text()
        if (code == "") :
            return
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        ip = data['rms_url']['ip']
        url = str(data['rms_url']['cms_url'])
        url = url.replace("%ip", ip)
        command = Command()
        r = RmsRequest()
        command = r.setCmsCode(bid, 1, code, url)
        self.command.emit(command)

    def applyBaseClicked(self) :
        bid = self.ui.basecodebidspinBox.value()
        code = self.ui.basecodelineEdit.text()
        if (code == "") :
            return
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        ip = data['rms_url']['ip']
        url = str(data['rms_url']['base_url'])
        url = url.replace("%ip", ip)
        command = Command()
        r = RmsRequest()
        command = r.setBaseCode(bid, 1, code, url)
        self.command.emit(command)

    def applyMcuClicked(self) :
        bid = self.ui.mcucodebidspinBox.value()
        code = self.ui.mcucodelineEdit.text()
        if (code == "") :
            return
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        ip = data['rms_url']['ip']
        url = str(data['rms_url']['mcu_url'])
        url = url.replace("%ip", ip)
        command = Command()
        r = RmsRequest()
        command = r.setMcuCode(bid, 1, code, url)
        self.command.emit(command)

    def applySiteClicked(self) :
        bid = self.ui.sitelocationbidspinBox.value()
        code = self.ui.sitelocationlineEdit.text()
        if (code == "") :
            return
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        ip = data['rms_url']['ip']
        url = str(data['rms_url']['site_url'])
        url = url.replace("%ip", ip)
        command = Command()
        r = RmsRequest()
        command = r.setSiteLocation(bid, 1, code, url)
        self.command.emit(command)
    
    def restartCmsClicked(self) :
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        ip = data['rms_url']['ip']
        url = str(data['rms_url']['restart_cms_url'])
        url = url.replace("%ip", ip)
        command = Command()
        r = RmsRequest()
        command = r.restartCms(255, 1, url)
        self.command.emit(command)

    def restartRmsClicked(self) :
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        ip = data['rms_url']['ip']
        url = str(data['rms_url']['restart_rms_url'])
        url = url.replace("%ip", ip)
        command = Command()
        r = RmsRequest()
        command = r.restartRms(1, url)
        self.command.emit(command)

    def voltageParameterClicked(self) :
        maxVal = self.ui.cellvoltagemaxspinBox.value()
        minVal = self.ui.cellvoltageminspinBox.value()
        v = VoltageParameter()
        v.max = maxVal
        v.min = minVal
        self.voltageParameter.emit(v)
    
    def temperatureParameterClicked(self) :
        maxVal = self.ui.temperaturemaxspinBox.value()
        minVal = self.ui.temperatureminspinBox.value()
        v = TemperatureParameter()
        v.max = maxVal
        v.min = minVal
        self.temperatureParameter.emit(v)

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
    widget = RmsWindow()
    widget.show()
    app.exec_()