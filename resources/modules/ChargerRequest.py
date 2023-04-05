import requests
import json
import threading
import PyQt5.QtCore as qtc
import time
import os
from .Command import Command
from .ChargerData import ChargerData
from .ChargerData import ChargerDataParser
from ..definition import RESOURCES_DIR

class ChargerRequest(qtc.QThread, qtc.QObject):
    requestResponse = qtc.pyqtSignal(str)
    chargerData = qtc.pyqtSignal(ChargerData, int)
    status = qtc.pyqtSignal(int)
    def __init__(self):
        threading.Thread.__init__(self)
        qtc.QObject.__init__(self)
        self.__rectifierGetDataUrl = "http://localhost/chargersim/getdata.php"
        self.commandList = []
        self.isRun = False
        self.currentGroup = 0
        self.currentAddress = 1
        self.lastIndex = 0
        self.chargerTotal = 3

    @property
    def rectifierGetDataUrl(self) :
        return self.__rectifierGetDataUrl
    @rectifierGetDataUrl.setter
    def rectifierGetDataUrl(self, url : str) :
        self.__rectifierGetDataUrl = url

    def run(self) :
        while self.isRun :
            isRequest = False
            response = "Failed\n"
            if self.commandList :
                command = Command()
                command = self.commandList.pop(0)
                data = command.data
                url = command.url
                print("Send POST Request to Url : ", url)
                print(data)
                try :
                    r = requests.post(url = url, json = data, timeout= 1)
                    response = r.json()
                    status = response['status']
                    self.status.emit(status)
                    response = json.dumps(response)
                    response += '\n'
                    print("Charger Request Success")
                except :
                    print("Charger Request Failed")
                isRequest = True
            else :
                f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
                data = json.load(f)
                totalSize = len(data["ip_list"])
                
                if(self.currentAddress > self.chargerTotal) :
                    self.currentAddress = 1
                    self.lastIndex += 1

                if (self.lastIndex >= totalSize) :
                    self.lastIndex = 0

                arrData = data["ip_list"][self.lastIndex]
                currIndex = arrData["number"]
                ip = arrData['charger_url']['ip']
                url : str = arrData['charger_url']['data_url']
                url = url.replace("%ip", ip)
                data = {'group' : self.currentGroup,
                        'subaddress' : self.currentAddress
                }
                print("Send Post Request to Url : ", url)
                print(data)
                try :
                    r = requests.post(url = url, json = data, timeout = 1)
                    response = r.json()
                    jsonInput = response
                    parser = ChargerDataParser()
                    data = ChargerData()
                    data = parser.parseJson(jsonInput)
                    response = json.dumps(response)
                    response += '\n'
                    # print(response)
                    print("Charger Request Success")
                    self.chargerData.emit(data, currIndex)
                except :
                    print("Charger Request Failed")
                    # pass
                self.currentAddress += 1

            # self.requestResponse.emit(response)
            if(isRequest) :
                time.sleep(0.1)
            else :
                time.sleep(0.5)

    def setVoltage(self, group : int, subAddress : int, voltage : int, url : str) -> Command:
        data =  { 'group' : group,
                  'subaddress' : subAddress,
                  'voltage' : voltage
                }
        command = Command()
        command.data = data
        command.url = url
        self.insertToQueue(command)
        return command


    def setCurrent(self, group : int, subAddress : int, current : int, url : str) -> Command:
        data =  { 'group' : group,
                  'subaddress' : subAddress,
                  'current' : current
                }
        command = Command()
        command.data = data
        command.url = url
        self.insertToQueue(command)
        return command
    
    def setModule32(self, group : int, value : int, url : str) -> Command:
        data =  { 'group' : group,
                  'value' : value
                }
        command = Command()
        command.data = data
        command.url = url
        self.insertToQueue(command)
        return command

    def setModule64(self, group : int, value : int, url : str) -> Command:
        data =  { 'group' : group,
                  'value' : value
                }
        command = Command()
        command.data = data
        command.url = url
        self.insertToQueue(command)
        return command

    def insertToQueue(self, command : Command) :
        self.commandList.append(command)
        