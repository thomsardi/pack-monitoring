class BatteryData() :
    def __init__(self) -> None:
        self.__msgCount = 0
        self.__frameName = ""
        self.__cmsCode = ""
        self.__baseCode = ""
        self.__mcuCode = ""
        self.__siteLocation = ""
        self.__bid = 0
        self.__vcell = []
        self.__temperature = []
        self.__vpack = []
        self.__wakeStatus = 0
        self.__doorStatus = 0

    def printData(self) :
        print(self.__msgCount)
        print(self.__frameName)
        print(self.__cmsCode)
        print(self.__baseCode)
        print(self.__mcuCode)
        print(self.__siteLocation)
        print(self.__bid)
        print(self.__vcell)
        print(self.__temperature)
        print(self.__vpack)
        print(self.__wakeStatus)
        print(self.__doorStatus)

    # msgCount
    @property
    def msgCount(self) :
        return self.__msgCount
    
    @msgCount.setter
    def msgCount(self, msgCount = int) :
        self.__msgCount = msgCount

    # frameName
    @property
    def frameName(self) :
        return self.__frameName
    
    @frameName.setter
    def frameName(self, frameName = str) :
        self.__frameName = frameName

    # cmsCode
    @property
    def cmsCode(self) :
        return self.__cmsCode
    
    @cmsCode.setter
    def cmsCode(self, cmsCode = str) :
        self.__cmsCode = cmsCode

    # baseCode
    @property
    def baseCode(self) :
        return self.__baseCode
    
    @baseCode.setter
    def baseCode(self, baseCode = str) :
        self.__baseCode = baseCode

    # mcuCode
    @property
    def mcuCode(self) :
        return self.__mcuCode
    
    @mcuCode.setter
    def mcuCode(self, mcuCode = str) :
        self.__mcuCode = mcuCode

    # siteLocation
    @property
    def siteLocation(self) :
        return self.__siteLocation
    
    @siteLocation.setter
    def siteLocation(self, siteLocation = str) :
        self.__siteLocation = siteLocation

    # bid
    @property
    def bid(self) :
        return self.__bid
    
    @bid.setter
    def bid(self, bid = int) :
        self.__bid = bid

    # vcell
    @property
    def vcell(self) :
        vcell = self.__vcell.copy()
        return vcell
    
    @vcell.setter
    def vcell(self, vcell : list) :
        self.__vcell = vcell.copy()
    
    # temperature
    @property
    def temperature(self) :
        temperature = self.__temperature.copy()
        return temperature
    
    @temperature.setter
    def temperature(self, temperature : list) :
        self.__temperature = temperature.copy()

    # vpack
    @property
    def vpack(self) :
        vpack = self.__vpack.copy()
        return vpack
    
    @vpack.setter
    def vpack(self, vpack : list) :
        self.__vpack = vpack.copy()

    # wakeStatus
    @property
    def wakeStatus(self) :
        return self.__wakeStatus
    
    @wakeStatus.setter
    def wakeStatus(self, wakeStatus = int) :
        self.__wakeStatus = wakeStatus

    # doorStatus
    @property
    def doorStatus(self) :
        return self.__doorStatus
    
    @doorStatus.setter
    def doorStatus(self, doorStatus = int) :
        self.__doorStatus = doorStatus

class BatteryDataParser() :
    def __init__(self) -> None:
        self.__batteryData = []
        self.__rackSn = ""

    def parseJson(self, json : dict) :
        self.__rackSn = json['rack_sn']
        dataList = []
        dataList = json['cms_data']
        for dat in dataList :
            bat = BatteryData()
            bat.msgCount = dat['msg_count']
            bat.frameName = dat['frame_name']
            bat.cmsCode = dat['cms_code']
            bat.baseCode = dat['base_code']
            bat.mcuCode = dat['mcu_code']
            bat.siteLocation = dat['site_location']
            bat.bid = dat['bid']
            bat.vcell = dat['vcell']
            bat.temperature = dat['temp']
            bat.vpack = dat['pack']
            bat.wakeStatus = dat['wake_status']
            bat.doorStatus = dat['door_status']
            # bat.printData()
            self.__batteryData.append(bat)

    @property
    def batteryData(self) :
        return self.__batteryData
    
    @property
    def rackSn(self) :
        return self.__rackSn