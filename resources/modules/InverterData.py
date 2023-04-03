class InverterData() :
    def __init__(self) -> None:
        self.__systemDcVoltage = 0
        self.__systemDcCurrent = 0
        self.__totalActivePower = 0
        

    def printData(self) :
        print(self.__systemDcVoltage)
        print(self.__systemDcCurrent)
        print(self.__totalActivePower)
    
    # System Dc Voltage
    @property
    def systemDcVoltage(self) :
        return self.__systemDcVoltage
    
    @systemDcVoltage.setter
    def systemDcVoltage(self, systemDcVoltage = int) :
        self.__systemDcVoltage = systemDcVoltage

    # System Dc Current
    @property
    def systemDcCurrent(self) :
        return self.__systemDcCurrent
    
    @systemDcCurrent.setter
    def systemDcCurrent(self, systemDcCurrent = int) :
        self.__systemDcCurrent = systemDcCurrent

    # Total Active Power
    @property
    def totalActivePower(self) :
        return self.__totalActivePower
    
    @totalActivePower.setter
    def totalActivePower(self, totalActivePower = int) :
        self.__totalActivePower = totalActivePower

class InverterDataParser() :
    def __init__(self) -> None:
        self.__inverterData = []

    def parseJson(self, json : dict) -> InverterData:
        data = InverterData()
        data.systemDcVoltage = json['system_dc_side_voltage_mv']
        data.systemDcCurrent = json['system_dc_side_total_current_ma']
        data.totalActivePower = json['total_active_power_mw']
        return data

    @property
    def inverterData(self) :
        return self.__inverterData