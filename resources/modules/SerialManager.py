import serial
import serial.tools.list_ports as port_list

class SerialHandler(serial.Serial):
    def __init__(self) :
        super().__init__()
        self.__ports = port_list.comports()
        self.__dataBuffer = []
        self.__newData = False
        self.__txData : bytearray
        self.__isTransmit = False
    
    def getCom(self):
        self.__ports = port_list.comports()
        return self.__ports
            
    def reScanPort(self):
        self.__ports = port_list.comports() 
    
    def printComInfo(self):
        for p in self.__ports :
            print(p.device, p.description)
        print(len(self.__ports), 'ports found')

    def begin(self) :
        self.open()
        return self.isOpen()

    def end(self) :
        self.close()
        return self.isOpen()

    def run(self) :
        # print("Serial Handler is running")
        while (self.inWaiting() > 0) :
            data = self.readline()
            self.__dataBuffer.append(data)
            self.__newData = True
        while (self.__isTransmit) :
            self.write(self.__txData)
            self.__isTransmit = False

    def readData(self) :
        numOfList = len(self.__dataBuffer)
        print(numOfList)
        if (numOfList > 0) :
            data = bytes(self.__dataBuffer.pop(0))
            print(data)
            return data
        self.__newData = False
        return bytes(0)

    def writeData(self, data : bytes) :
        self.__isTransmit = True
        self.__txData = data
        print(self.__txData)

    def isDataReady(self) :
        return self.__newData

    def getUsbDevice(self) :
        usbList = []
        for p in self.__ports :
            desc = p.description.lower()
            if "usb" in desc :
                usbList.append(p)
        return usbList
    
        