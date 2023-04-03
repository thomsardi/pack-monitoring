import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import serial
from ..serialsetting import Ui_Serial
from ...modules.SerialManager import SerialHandler

class SerialConfigUi(qtw.QWidget) :
    isChosen = qtc.pyqtSignal(SerialHandler)
    def __init__(self):
        super().__init__()
        self.__baudrateList = ["9600", "19200", "38400", "115200"]
        self.__databitsList = ["5", "6", "7", "8"]
        self.__parityList = ["None", "Odd", "Even", "Space", "Mark"]
        self.__stopbitsList = ["1", "1.5", "2"]
        self.uiSerial = Ui_Serial()
        self.__serialHandler = SerialHandler()
        self.__portList = self.__serialHandler.getCom()
        self.uiSerial.setupUi(self)
        self.uiSerial.okpushButton.clicked.connect(self.onClickOk)
        self.uiSerial.cancelpushButton.clicked.connect(self.onClickCancel)
        self.uiSerial.scanportpushButton.clicked.connect(self.onClickScan)
        self.uiSerial.portcomboBox.currentIndexChanged.connect(self.__updateDescription)
        self.uiSerial.baudratecomboBox.addItems(self.__baudrateList)
        self.uiSerial.databitscomboBox.addItems(self.__databitsList)
        self.uiSerial.paritycomboBox.addItems(self.__parityList)
        self.uiSerial.stopbitscomboBox.addItems(self.__stopbitsList)
    
    def updatePort(self) :
        self.uiSerial.portcomboBox.clear()
        self.__portList = self.__serialHandler.getCom()
        for p in self.__portList :
            self.uiSerial.portcomboBox.addItem(p.name)
        self.serialConfigToString()

    def onClickCancel(self) :
        self.close()

    def onClickOk(self) :
        self.setConfiguration()
        self.isChosen.emit(self.__serialHandler)
        self.close()
        
    def onClickScan(self) :
        self.updatePort()
    
    def getConfiguration(self) :
        return self.__serialHandler

    def serialConfigToString(self) :
        index = self.uiSerial.portcomboBox.findText(self.__serialHandler.port)
        if (index >= 0) :
            self.uiSerial.portcomboBox.setCurrentIndex(index)
        else :
            self.uiSerial.portcomboBox.setCurrentIndex(0)

        self.uiSerial.baudratecomboBox.setCurrentIndex(self.uiSerial.baudratecomboBox.findText(str(self.__serialHandler.baudrate)))
        
        if self.__serialHandler.bytesize == serial.FIVEBITS :
            self.uiSerial.databitscomboBox.setCurrentIndex(self.uiSerial.databitscomboBox.findText("5"))
        elif self.__serialHandler.bytesize == serial.SIXBITS :
            self.uiSerial.databitscomboBox.setCurrentIndex(self.uiSerial.databitscomboBox.findText("6"))
        elif self.__serialHandler.bytesize == serial.SEVENBITS :
            self.uiSerial.databitscomboBox.setCurrentIndex(self.uiSerial.databitscomboBox.findText("7"))
        else :
            self.uiSerial.databitscomboBox.setCurrentIndex(self.uiSerial.databitscomboBox.findText("8"))

        if self.__serialHandler.parity == serial.PARITY_NONE :
            self.uiSerial.paritycomboBox.setCurrentIndex(self.uiSerial.paritycomboBox.findText("None"))
        elif self.__serialHandler.parity == serial.PARITY_ODD :
            self.uiSerial.paritycomboBox.setCurrentIndex(self.uiSerial.paritycomboBox.findText("Odd"))
        elif self.__serialHandler.parity == serial.PARITY_EVEN :
            self.uiSerial.paritycomboBox.setCurrentIndex(self.uiSerial.paritycomboBox.findText("Even"))
        elif self.__serialHandler.parity == serial.PARITY_SPACE:
            self.uiSerial.paritycomboBox.setCurrentIndex(self.uiSerial.paritycomboBox.findText("Space"))            
        else :
            self.uiSerial.paritycomboBox.setCurrentIndex(self.uiSerial.paritycomboBox.findText("Mark"))
        
        if self.__serialHandler.stopbits == serial.STOPBITS_ONE :
            self.uiSerial.stopbitscomboBox.setCurrentIndex(self.uiSerial.stopbitscomboBox.findText("1"))
        elif self.__serialHandler.stopbits == serial.STOPBITS_ONE_POINT_FIVE  :
            self.uiSerial.stopbitscomboBox.setCurrentIndex(self.uiSerial.stopbitscomboBox.findText("1.5"))        
        else :
            self.uiSerial.stopbitscomboBox.setCurrentIndex(self.uiSerial.stopbitscomboBox.findText("2")) 


    def setConfiguration(self) :
        self.__serialHandler.setPort(self.uiSerial.portcomboBox.currentText())
        self.__serialHandler.baudrate = int(self.uiSerial.baudratecomboBox.currentText())
        dataBits = self.uiSerial.databitscomboBox.currentText()
        parity = self.uiSerial.paritycomboBox.currentText()
        stopBits = self.uiSerial.stopbitscomboBox.currentText()
        if dataBits == "5" :
            self.__serialHandler.bytesize = serial.FIVEBITS
        elif dataBits == "6" :
            self.__serialHandler.bytesize = serial.SIXBITS
        elif dataBits == "7" :
            self.__serialHandler.bytesize = serial.SEVENBITS
        else :
            self.__serialHandler.bytesize = serial.EIGHTBITS

        if parity == "None" :
            self.__serialHandler.parity = serial.PARITY_NONE
        elif dataBits == "Odd" :
            self.__serialHandler.parity = serial.PARITY_ODD
        elif dataBits == "Even" :
            self.__serialHandler.parity = serial.PARITY_EVEN
        elif dataBits == "Space" :
            self.__serialHandler.parity = serial.PARITY_SPACE            
        else :
            self.__serialHandler.parity = serial.PARITY_MARK

        if stopBits == "1" :
            self.__serialHandler.stopbits = serial.STOPBITS_ONE
        elif stopBits == "1.5" :
            self.__serialHandler.stopbits = serial.STOPBITS_ONE_POINT_FIVE          
        else :
            self.__serialHandler.stopbits = serial.STOPBITS_TWO

    def __updateDescription(self) :
        index = self.uiSerial.portcomboBox.currentIndex()
        if (index >= 0) :
            self.uiSerial.descriptionplainTextEdit.setPlainText(self.__portList[index].description)
        else :
            self.uiSerial.descriptionplainTextEdit.setPlainText("")

