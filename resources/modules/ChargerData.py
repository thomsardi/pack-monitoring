class ChargerData() :
    def __init__(self) -> None:
        self.__msgCount = 0
        self.__group = 0
        self.__subAddress = 0
        self.__voltage = 0
        self.__current = 0
        self.__moduleOff = 0
        self.__dcOperatingStatus = 0
        self.__acOperatingStatus = 0
        self.__dcStatus1 = 0
        self.__dcStatus2 = 0
        self.__acStatus1 = 0
        self.__acStatus2 = 0
        self.__acVersion = 0
        self.__dcVersion = 0


    def printData(self) :
        print(self.__msgCount)
        print(self.__group)
        print(self.__subAddress)
        print(self.__voltage)
        print(self.__current)
        print(self.__moduleOff)
        print(self.__dcOperatingStatus)
        print(self.__acOperatingStatus)
        print(self.__dcStatus1)
        print(self.__dcStatus2)
        print(self.__acStatus1)
        print(self.__acStatus2)

    # msgCount
    @property
    def msgCount(self) :
        return self.__msgCount
    
    @msgCount.setter
    def msgCount(self, msgCount = int) :
        self.__msgCount = msgCount

    # group
    @property
    def group(self) :
        return self.__group
    
    @group.setter
    def group(self, group = int) :
        self.__group = group

    # subAddress
    @property
    def subAddress(self) :
        return self.__subAddress
    
    @subAddress.setter
    def subAddress(self, subAddress = int) :
        self.__subAddress = subAddress

    # voltage
    @property
    def voltage(self) :
        return self.__voltage
    
    @voltage.setter
    def voltage(self, voltage = int) :
        self.__voltage = voltage

    # current
    @property
    def current(self) :
        return self.__current
    
    @current.setter
    def current(self, current = int) :
        self.__current = current

    # moduleOff
    @property
    def moduleOff(self) :
        return self.__moduleOff
    
    @moduleOff.setter
    def moduleOff(self, moduleOff = int) :
        self.__moduleOff = moduleOff

    # dcOperatingStatus
    @property
    def dcOperatingStatus(self) :
        return self.__dcOperatingStatus
    
    @dcOperatingStatus.setter
    def dcOperatingStatus(self, dcOperatingStatus = int) :
        self.__dcOperatingStatus = dcOperatingStatus

    # acOperatingStatus
    @property
    def acOperatingStatus(self) :
        return self.__acOperatingStatus
    
    @acOperatingStatus.setter
    def acOperatingStatus(self, acOperatingStatus : int) :
        self.__acOperatingStatus = acOperatingStatus
    
    # dcStatus1
    @property
    def dcStatus1(self) :
        return self.__dcStatus1
    
    @dcStatus1.setter
    def dcStatus1(self, dcStatus1 : int) :
        self.__dcStatus1 = dcStatus1

    # dcStatus2
    @property
    def dcStatus2(self) :
        return self.__dcStatus2
    
    @dcStatus2.setter
    def dcStatus2(self, dcStatus2 : int) :
        self.__dcStatus2 = dcStatus2

    # acStatus1
    @property
    def acStatus1(self) :
        return self.__acStatus1
    
    @acStatus1.setter
    def acStatus1(self, acStatus1 = int) :
        self.__acStatus1 = acStatus1

    # acStatus2
    @property
    def acStatus2(self) :
        return self.__acStatus2
    
    @acStatus2.setter
    def acStatus2(self, acStatus2 = int) :
        self.__acStatus2 = acStatus2

    # acVersion
    @property
    def acVersion(self) :
        return self.__acVersion
    
    @acVersion.setter
    def acVersion(self, acVersion = int) :
        self.__acVersion = acVersion
    
    # dcVersion
    @property
    def dcVersion(self) :
        return self.__dcVersion
    
    @dcVersion.setter
    def dcVersion(self, dcVersion = int) :
        self.__dcVersion = dcVersion

class ChargerDataParser() :
    def __init__(self) -> None:
        self.__rectifierData = []

    def parseJson(self, json : dict) -> ChargerData:
        dat = json
        bat = ChargerData()
        bat.msgCount = dat['msg_count']
        bat.group = dat['group']
        bat.subAddress = dat['subaddress']
        bat.voltage = dat['voltage']
        bat.current = dat['current']
        bat.moduleOff = dat['module_off']
        bat.dcOperatingStatus = dat['dc_operating_status']
        bat.acOperatingStatus = dat['ac_operating_status']
        bat.dcStatus1 = dat['dc_status_1']
        bat.dcStatus2 = dat['dc_status_2']
        bat.acStatus1 = dat['ac_status_1']
        bat.acStatus2 = dat['ac_status_2']
        bat.acVersion = dat['ac_version']
        bat.dcVersion = dat['dc_version']
        # bat.printData()
        # self.__rectifierData.append(bat)
        return bat

    @property
    def rectifierData(self) :
        return self.__rectifierData