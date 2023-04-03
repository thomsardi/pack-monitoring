import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import sys
from pathlib import Path
from resources.window_ui.uploader import Ui_Uploader
from resources.modules.SerialManager import SerialHandler
from resources.modules.OutputWindow import OutputWindow
from resources.modules.EspUploader import EspUploader
from resources.modules.EspReadMac import EspReadMac

class UploaderUi(qtw.QWidget) :
    def __init__(self):
        super().__init__()
        self.uploaderUi = Ui_Uploader()
        self.uploaderUi.setupUi(self)
        self.uploaderUi.firmwarebrowsepushButton.clicked.connect(self.openFirmwareBrowse)
        self.uploaderUi.systembrowsepushButton.clicked.connect(self.openSystemBrowse)
        self.uploaderUi.bootLoaderBrowsepushButton.clicked.connect(self.openBootloaderBrowse)
        self.uploaderUi.uploadpushButton.clicked.connect(self.uploadButtonOnClick)
        self.uploaderUi.clearpushButton.clicked.connect(self.__clearTerminal)
        self.uploaderUi.detectPushButton.clicked.connect(self.detectButtonClicked)
        self.__realout = sys.stdout
        self.__serial = SerialHandler()
        self.__numOfUsb = 0
        
        self.__text = ""
        self.__totalUpload = 0
        self.__successUpload = 0
        self.__failedUpload = 0

    def openFirmwareBrowse(self) :
        dirPath = Path().absolute()
        dirPath = str(dirPath) + "/bin"
        fname = qtw.QFileDialog.getOpenFileName(self, 'Browse Firmware File', dirPath, 'bin file (*.bin)')
        self.uploaderUi.firmwaredirlineEdit.setText(fname[0])

    def openSystemBrowse(self) :
        dirPath = Path().absolute()
        dirPath = str(dirPath) + "/bin"
        fname = qtw.QFileDialog.getOpenFileName(self, 'Browse System File', dirPath, 'bin file (*.bin)')
        self.uploaderUi.systemdirlineEdit.setText(fname[0])

    def openBootloaderBrowse(self) :
        dirPath = Path().absolute()
        dirPath = str(dirPath) + "/bin"
        fname = qtw.QFileDialog.getOpenFileName(self, 'Browse Bootloader File', dirPath, 'bin file (*.bin)')
        self.uploaderUi.bootLoaderlineEdit.setText(fname[0])

    def uploadButtonOnClick(self) :
        self.__serial.reScanPort()
        espUploader = []
        sys.stdout = OutputWindow()
        sys.stdout.isDataAvailable.connect(self.updateTerminalPlainText)
        self.__currentCount = 0
        usbList = self.__serial.getUsbDevice()
        self.__numOfUsb = len(usbList)
        print("Detected Devices : ", self.__numOfUsb)
        firmwarePath = self.uploaderUi.firmwaredirlineEdit.text()
        systemPath = self.uploaderUi.systemdirlineEdit.text()
        partition = self.uploaderUi.partitioncomboBox.currentText()
        bootLoaderPath = self.uploaderUi.bootLoaderlineEdit.text()
        
        for usb in usbList :
            eUploader = EspUploader()
            eUploader.isDone.connect(self.uploadDone)
            eUploader.port = usb.name
            eUploader.firmwarePath = firmwarePath
            eUploader.systemPath = systemPath
            eUploader.partition = partition
            eUploader.bootloaderPath = bootLoaderPath
            espUploader.append(eUploader)
        for e in espUploader :
            e.start()

    def uploadDone(self, portName, status) :
        self.__totalUpload += 1
        if (status) :
            self.__successUpload += 1
            statusText = "Success"
        else :
            self.__failedUpload += 1
            statusText = "Error"
        print("Port : ", portName)
        print("Upload Status : ", statusText)
        if(self.__totalUpload >= self.__numOfUsb) :
            sys.stdout = sys.__stdout__
            self.showMessageBox(self.__totalUpload, self.__successUpload, self.__failedUpload)
            self.__totalUpload = 0
            self.__successUpload = 0
            self.__failedUpload = 0
            self.__numOfUsb = 0
        
    def showMessageBox(self, totalUpload : int, successUpload : int, failedUpload : int) :
        totalUploadinfo = "Finish Upload into : %d device(s)\n" %(totalUpload)
        successUploadInfo = "Success Upload : %d device(s)\n" %(successUpload)
        failedUploadInfo = "Failed Upload : %d device(s)\n" %(failedUpload)
        msg = qtw.QMessageBox()
        msg.setWindowTitle("Upload Status")
        msg.setText(totalUploadinfo + successUploadInfo + failedUploadInfo)
        msg.setIcon(qtw.QMessageBox.Information)
        msg.exec()

    def updateTerminalPlainText(self, data) :
        self.updateCursorPos()
        text = data
        self.uploaderUi.terminalplainTextEdit.insertPlainText(text)

    def clearWindow(self) :
        self.__clearLineEdit()
        self.__clearTerminal()

    def __clearLineEdit(self) :
        self.uploaderUi.firmwaredirlineEdit.clear()
        self.uploaderUi.systemdirlineEdit.clear()
        self.uploaderUi.bootLoaderlineEdit.clear()
    
    def __clearTerminal(self) :
        self.uploaderUi.terminalplainTextEdit.clear()
        self.updateCursorPos()

    def setSerial(self, serial : SerialHandler()) :
        self.__serial = serial

    def detectButtonClicked(self) :
        self.__serial.reScanPort()
        espReadMac = []
        sys.stdout = OutputWindow()
        sys.stdout.isDataAvailable.connect(self.updateTerminalPlainText)

        usbList = self.__serial.getUsbDevice()
        self.__numOfUsb = len(usbList)
        self.__currentCount = 0
        for usb in usbList :
            e = EspReadMac()
            e.setPort(usb.name)
            espReadMac.append(e)
            e.isDone.connect(self.__readMacEvent)
        
        for e in espReadMac :
            e.start()
        
    def __readMacEvent(self, portName, status) :
        self.__currentCount += 1
        statusText = ""
        print("Port : ", portName)
        if (status) :
            statusText = "Success"
        else :
            statusText = "Error"
        print("Read Mac : ", statusText)
        if(self.__currentCount >= self.__numOfUsb) :
            self.__currentCount += 0
            sys.stdout = sys.__stdout__

    def updateCursorPos(self) :
        plainTextCursor = qtg.QTextCursor()
        plainTextCursor = self.uploaderUi.terminalplainTextEdit.textCursor()
        self.uploaderUi.terminalplainTextEdit.moveCursor(plainTextCursor.MoveOperation.End, plainTextCursor.MoveMode.MoveAnchor)

