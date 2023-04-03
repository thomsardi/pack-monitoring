from resources.modules.SerialManager import SerialHandler
import PyQt5.QtCore as qtc

class SerialThread(qtc.QThread):
    isDataReady = qtc.pyqtSignal(bytes)
    stringData = qtc.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.__serialHandler : SerialHandler = None
        self.exiting = False
        self.isLoop = True
        self.data = None
    def run(self):
        # Note: This is never called directly. It is called by Qt once the
        # thread environment has been set up.
        while (self.isLoop) :
            if (self.__serialHandler is not None) :
                self.__serialHandler.run()
                if (self.__serialHandler.isDataReady()) :
                    data = self.__serialHandler.readData()
                    self.isDataReady.emit(data)
                    self.stringData.emit(data.decode())

    def setSerialObject(self, serialHandler : SerialHandler()) :
        self.__serialHandler = serialHandler
    
        