import requests
import json
import threading
import time
import os
import PyQt5.QtCore as qtc

from .InverterData import InverterData
from .InverterData import InverterDataParser
from .Command import Command
from ..definition import RESOURCES_DIR


class InverterRequest(qtc.QThread, qtc.QObject):
    requestResponse = qtc.pyqtSignal(str)
    inverterData = qtc.pyqtSignal(list, int)
    status = qtc.pyqtSignal(int)
    def __init__(self):
        threading.Thread.__init__(self)
        qtc.QObject.__init__(self)
        self.inverterGetDataUrl = "http://localhost/invertersim/get-data-inverter.php"
        self.commandList = []
        self.isRun = False
        self.data = []
        self.lastIndex = 0

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
                    print("Inverter Request Success")
                except :
                    print("Inverter Request Failed")
                isRequest = True
            else :
                f = open(os.path.join(RESOURCES_DIR,'resources', 'config_test.json'))
                data = json.load(f)
                totalSize = len(data["ip_list"])
                if (self.lastIndex >= totalSize) :
                    self.lastIndex = 0
                arrData = data["ip_list"][self.lastIndex]
                currIndex = arrData["number"]
                
                url_list = []
                url_list = arrData['inverter_url']
                for list in url_list :
                    ip = str(list['ip'])
                    url = str(list['data_url'])
                    url = url.replace("%ip", ip)
                    # print("Send Get Request to Url : ", url)
                    try :
                        r = requests.get(url, timeout = 1)
                        response = r.json()
                        jsonInput = response
                        parser = InverterDataParser()
                        data = parser.parseJson(jsonInput)
                        response = json.dumps(response)
                        response += '\n'
                        # print("Inverter Request Success")
                        self.data.append(data)
                    except :
                        pass
                        # print("Inverter Request Failed")
            if(self.data) :
                self.inverterData.emit(self.data, currIndex)
                self.data.clear()
            # self.requestResponse.emit(response)
            if(isRequest) :
                time.sleep(0.1)
            else :
                time.sleep(1)
                self.lastIndex += 1

    def startInverter(self, value : int, url : str) -> Command:
        data =  { 'start' : value
                }
        # self.activeData = data
        # self.activeUrl = self.rmsAddressUrl
        command = Command()
        command.data = data
        command.url = url
        self.insertToQueue(command)
        return command

    def setParameter(self, controlType, mode, chargeVoltage : int, voltageCutOff1 : int, voltageCutOff2 : int, current : int, power : int, start : int, url : str) -> Command:
        data =  { 'mode' : mode,
                  'control_type' : controlType,
                  'voltage' : chargeVoltage,
                  'voltage_cut_off_1' : voltageCutOff1,
                  'voltage_cut_off_2' : voltageCutOff2,
                  'current' : current,
                  'power' : power,
                  'start' : start
                }
        # self.activeData = data
        # self.activeUrl = self.dataCollectionUrl
        command = Command()
        command.data = data
        command.url = url
        self.insertToQueue(command)
        return command

    def insertToQueue(self, command : Command) :
        self.commandList.append(command)
        