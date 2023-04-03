import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import json
import os
from resources.window_ui.serialmonitor import Ui_SerialMonitor
from ...modules.ChargerRequest import ChargerRequest
from ...modules.RmsRequest import RmsRequest
from ...definition import RESOURCES_DIR

class SerialMonitorUi(qtw.QWidget) :
    dataToSend = qtc.pyqtSignal(bytes)
    isChargeStart = qtc.pyqtSignal(int)
    isStartDataClicked = qtc.pyqtSignal(int)
    def __init__(self) -> None:
        super().__init__()
        self.serialMonitorUi = Ui_SerialMonitor()
        self.serialMonitorUi.setupUi(self)
        self.__serialLineEnding = ["No Line Ending", "Newline(\\n)", "Carriage Return(\\r)", "NL + CR (\\r\\n)"]
        self.serialMonitorUi.seriallinendingcomboBox.addItems(self.__serialLineEnding)
        self.serialMonitorUi.seriallinendingcomboBox.setCurrentIndex(1)
        self.serialMonitorUi.clearpushButton.clicked.connect(self.__clearTerminal)
        self.serialMonitorUi.sendcommandpushButton.clicked.connect(self.__send)
        self.serialMonitorUi.addresspushButton.clicked.connect(self.addressClicked)
        self.serialMonitorUi.startdatapushButton.clicked.connect(self.startDataClicked)
        self.serialMonitorUi.stopdatapushButton.clicked.connect(self.stopDataClicked)
        self.serialMonitorUi.restartcmspushButton.clicked.connect(self.restartCmsClicked)
        self.serialMonitorUi.restartrmspushButton.clicked.connect(self.restartRmsClicked)
        self.serialMonitorUi.startchargepushButton.clicked.connect(self.startChargeClicked)
        self.serialMonitorUi.stopchargepushButton.clicked.connect(self.stopChargeClicked)
        self.serialMonitorUi.voltageapplypushButton.clicked.connect(self.voltageApplyClicked)
        self.serialMonitorUi.currentapplypushButton.clicked.connect(self.currentApplyClicked)
        self.serialMonitorUi.frameapplypushButton.clicked.connect(self.applyFrameClicked)
        
        # print(data)
        
    def update(self, s : str) :
        if (self.serialMonitorUi.autoScrollCheckBox.isChecked()) :
            self.updateCursorPos()
        self.serialMonitorUi.terminalplainTextEdit.insertPlainText(s)
    
    def __clearTerminal(self) :
        self.serialMonitorUi.terminalplainTextEdit.clear()

    def __send(self) :
        data = self.__makeCommand(self.serialMonitorUi.commandlineEdit.text())
        self.serialMonitorUi.commandlineEdit.clear()
        bytesToSend = bytes(data, 'utf-8')
        self.dataToSend.emit(bytesToSend)
    
    # def addressClicked(self) :
    #     data = "startaddress\n"
    #     bytesData = bytes(data, 'utf-8')
    #     self.dataToSend.emit(bytesData)
    
    def addressClicked(self) :
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        url = data['rms_url']['address_url']
        self.rmsRequest.setAddress(1, url)
        
    
    # def startDataClicked(self) :
    #     data = "startdata\n"
    #     bytesData = bytes(data, 'utf-8')
    #     self.dataToSend.emit(bytesData)

    def startDataClicked(self) :
        self.isStartDataClicked.emit(1)
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        url = data['rms_url']['data_collection_url']
        self.rmsRequest.setDataCollection(1, url)
        
    
    # def stopDataClicked(self) :
    #     data = "stopdata\n"
    #     bytesData = bytes(data, 'utf-8')
    #     self.dataToSend.emit(bytesData)
    
    def stopDataClicked(self) :
        self.isStartDataClicked.emit(0)
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        url = data['rms_url']['data_collection_url']
        self.rmsRequest.setDataCollection(0, url)
    
    # def restartCmsClicked(self) :
    #     data = "restartcms\n"
    #     bytesData = bytes(data, 'utf-8')
    #     self.dataToSend.emit(bytesData)
 
    def applyFrameClicked(self) :
        print("applied")
        bid = self.serialMonitorUi.bidspinBox.value()
        frameName = self.serialMonitorUi.framenamelineEdit.text()
        if (frameName == "") :
            return
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        url = data['rms_url']['frame_url']
        self.rmsRequest.setFrame(bid, 1, frameName, url)

    def restartCmsClicked(self) :
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        url = data['rms_url']['restart_cms_url']
        self.rmsRequest.restartCms(255, 1, url)

    # def restartRmsClicked(self) :
    #     data = "restartrms\n"
    #     bytesData = bytes(data, 'utf-8')
    #     self.dataToSend.emit(bytesData)
    
    def restartRmsClicked(self) :
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        url = data['rms_url']['restart_rms_url']
        self.rmsRequest.restartRms(1, url)
    
    def startChargeClicked(self) :
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        url = data['rectifier_url']['module32_url']
        rectifier = ChargerRequest()
        rectifier.setModuleOnOff32Url(url)
        rectifier.setModule32(0, 14)
        rectifier.requestResponse.connect(self.printResponse)
        rectifier.requestResponse.connect(self.update)
        rectifier.start()
        self.isChargeStart.emit(1)
        
    def stopChargeClicked(self) :
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        url = data['rectifier_url']['module32_url']
        rectifier = ChargerRequest()
        rectifier.setModuleOnOff32Url(url)
        rectifier.setModule32(0, 0)
        rectifier.requestResponse.connect(self.printResponse)
        rectifier.requestResponse.connect(self.update)
        rectifier.start()
        self.isChargeStart.emit(0)

    def voltageApplyClicked(self) :
        group = self.serialMonitorUi.voltagegroupspinBox.value()
        subaddress = self.serialMonitorUi.voltagesubaddressspinBox.value()
        voltage = self.serialMonitorUi.voltagespinBox.value()

        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        url = data['rectifier_url']['voltage_url']
        rectifier = ChargerRequest()
        rectifier.setVoltageUrl(url)
        rectifier.setVoltage(group, subaddress, voltage)
        rectifier.requestResponse.connect(self.printResponse)
        rectifier.requestResponse.connect(self.update)
        rectifier.start()
    
    def currentApplyClicked(self) :
        group = self.serialMonitorUi.currentgroupspinBox.value()
        subaddress = self.serialMonitorUi.currentsubaddressspinBox.value()
        current = self.serialMonitorUi.currentspinBox.value()

        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        url = data['rectifier_url']['current_url']
        rectifier = ChargerRequest()
        rectifier.setCurrentUrl(url)
        rectifier.setCurrent(group, subaddress, current)
        rectifier.requestResponse.connect(self.printResponse)
        rectifier.requestResponse.connect(self.update)
        rectifier.start()

    def __makeCommand(self, cmd) :
        if self.serialMonitorUi.seriallinendingcomboBox.currentIndex() == 1 :
            cmd += "\n"
        elif self.serialMonitorUi.seriallinendingcomboBox.currentIndex() == 2 :
            cmd += "\r"
        elif self.serialMonitorUi.seriallinendingcomboBox.currentIndex() == 3 :
            cmd += "\r\n"
        return cmd

    def printResponse(self, data : str) :
        # print(data)
        pass

    def updateCursorPos(self) :
        self.__plainTextCursor = self.serialMonitorUi.terminalplainTextEdit.textCursor()
        self.serialMonitorUi.terminalplainTextEdit.moveCursor(self.__plainTextCursor.MoveOperation.End, self.__plainTextCursor.MoveMode.MoveAnchor)