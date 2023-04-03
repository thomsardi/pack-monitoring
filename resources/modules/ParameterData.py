class VoltageParameter() :
    def __init__(self) -> None:
        self.__max = 0
        self.__min = 0

    @property
    def max(self) :
        return self.__max

    @max.setter
    def max(self, max : int) :
        self.__max = max
    
    @property
    def min(self) :
        return self.__min

    @min.setter
    def min(self, min : int) :
        self.__min = min

class TemperatureParameter() :
    def __init__(self) -> None:
        self.__max = 0
        self.__min = 0

    @property
    def max(self) :
        return self.__max

    @max.setter
    def max(self, max : int) :
        self.__max = max
    
    @property
    def min(self) :
        return self.__min

    @min.setter
    def min(self, min : int) :
        self.__min = min