import PyQt5.QtCore as qtc
import esptool
import threading

class EspReadMac(threading.Thread, qtc.QObject) :
    isDone = qtc.pyqtSignal(str, int)
    def __init__(self) -> None:
        threading.Thread.__init__(self)
        qtc.QObject.__init__(self)
        self.daemon = True
        self.__port = ""

    def run(self) :
        command = []
        command.extend(["--chip", "esp32", "--port", self.__port, "read_mac"])

        try :
            # print(''.join(command))
            esptool.main(command)
            self.isDone.emit(self.__port, 1)
        except :
            self.isDone.emit(self.__port, 0)

    def setPort(self, portName) :
        self.__port = portName