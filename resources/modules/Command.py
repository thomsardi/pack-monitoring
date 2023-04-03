class Command() :
    def __init__(self) -> None:
        self.__url = None
        self.__data = None

    @property
    def url(self) :
        return self.__url

    @url.setter
    def url(self, url : str) :
        self.__url = url
    
    @property
    def data(self) :
        return self.__data

    @data.setter
    def data(self, data : dict) :
        self.__data = data