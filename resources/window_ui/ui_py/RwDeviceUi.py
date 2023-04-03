import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import sys
from pathlib import Path
from resources.window_ui.uploader import Ui_Uploader
from resources.modules.SerialManager import SerialHandler
from resources.modules.OutputWindow import OutputWindow
from resources.modules.EspUploader import EspUploader
from resources.modules.EspReadMac import EspReadMac
from ..rwdevice import Ui_RwDevice
from ...modules.SerialThread import SerialThread

class RwDeviceUi(qtw.QWidget) :
    def __init__(self):
        super().__init__()
        self.rwDeviceUi = Ui_RwDevice()
        self.rwDeviceUi.setupUi(self)
        self.rwDeviceUi.addresspushButton.clicked.connect(self.addressClicked)
        self.rwDeviceUi.startdatapushButton.clicked.connect(self.startDataClicked)
        self.rwDeviceUi.stopdatapushButton.clicked.connect(self.stopDataClicked)
        self.rwDeviceUi.restartcmspushButton.clicked.connect(self.restartCmsClicked)
        self.rwDeviceUi.restartrmspushButton.clicked.connect(self.restartRmsClicked)
        self.__activeSerial = SerialHandler()
        self.__realout = sys.stdout
        self.__numOfUsb = 0
        self.__currentCount = 0
        self.__text = ""

    def addressClicked(self) :
        self.__activeSerial.writeData("setaddress\n")

    def startDataClicked(self) :
        self.__activeSerial.writeData("startdata\n")

    def stopDataClicked(self) :
        self.__activeSerial.writeData("stopdata\n")
    
    def restartCmsClicked(self) :
        self.__activeSerial.writeData("restartcms\n")
    
    def restartRmsClicked(self) :
        self.__activeSerial.writeData("restartrms\n")

    def updateTerminalPlainText(self, data) :
        self.updateCursorPos()
        text = data
        self.rwDeviceUi.terminalplainTextEdit.insertPlainText(text)

    def clearWindow(self) :
        self.__clearLineEdit()
        self.__clearTerminal()

    def __clearLineEdit(self) :
        pass
    
    def __clearTerminal(self) :
        self.rwDeviceUi.terminalplainTextEdit.clear()
        self.updateCursorPos()

    def setSerial(self, serial : SerialHandler()) :
        self.__serial = serial

    def updateCursorPos(self) :
        plainTextCursor = qtg.QTextCursor()
        plainTextCursor = self.rwDeviceUi.terminalplainTextEdit.textCursor()
        self.rwDeviceUi.terminalplainTextEdit.moveCursor(plainTextCursor.MoveOperation.End, plainTextCursor.MoveMode.MoveAnchor)

