import requests
import json
import threading
import time
import os
import PyQt5.QtCore as qtc

from .BatteryData import BatteryData
from .BatteryData import BatteryDataParser
from .Command import Command
from ..definition import RESOURCES_DIR

class RmsRequest(qtc.QThread, qtc.QObject):
    requestResponse = qtc.pyqtSignal(str)
    batteryData = qtc.pyqtSignal(list, int, str)
    status = qtc.pyqtSignal(int)
    failedToGetData = qtc.pyqtSignal(int, int)
    def __init__(self):
        threading.Thread.__init__(self)
        qtc.QObject.__init__(self)
        self.rmsGetDataUrl = "http://localhost/rmssim/getdata.php"
        self.commandList = []
        self.isRun = False
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
                    print("RMS Request Success")
                except :
                    print("RMS Request Failed")
                isRequest = True
            else :
                f = open(os.path.join(RESOURCES_DIR,'resources', 'config_test.json'))
                data = json.load(f)
                totalSize = len(data["ip_list"])
                if (self.lastIndex >= totalSize) :
                    self.lastIndex = 0
                arrData = data["ip_list"][self.lastIndex]
                currIndex = arrData["number"]
                # print(arrData)

                ip = arrData['rms_url']['ip']
                url = str(arrData['rms_url']['data_url'])
                url = url.replace("%ip", ip)
                # print("Send Get Request to Url : ", url)
                try :
                    r = requests.get(url, timeout = 1)
                    response = r.json()
                    jsonInput = response
                    parser = BatteryDataParser()
                    parser.parseJson(jsonInput)
                    response = json.dumps(response)
                    response += '\n'
                    # print("RMS Request Success")
                    data = parser.batteryData.copy()
                    # self.batteryData.emit(parser.batteryData)
                    self.batteryData.emit(data, currIndex, ip)
                    # print("Current Index %i \n" %(currIndex))
                except :
                    self.failedToGetData.emit(1, currIndex)
                    # print("RMS Request Failed")
            self.requestResponse.emit(response)
            if(isRequest) :
                time.sleep(0.1)
            else :
                time.sleep(0.5)
                self.lastIndex += 1
            

    def setAddress(self, value : int, url : str) -> Command:
        data =  { 'addr' : value
                }
        # self.activeData = data
        # self.activeUrl = self.rmsAddressUrl
        command = Command()
        command.data = data
        command.url = url
        self.insertToQueue(command)
        return command

    def setDataCollection(self, value : int, url : str) -> Command:
        data =  { 'data_collection' : value
                }
        # self.activeData = data
        # self.activeUrl = self.dataCollectionUrl
        command = Command()
        command.data = data
        command.url = url
        self.insertToQueue(command)
        return command
    
    def setFrame(self, bid : int, value : int, frameName : str, url : str) -> Command:
        data =  { 'bid' : bid,
                  'frame_write' : value,
                  'frame_name' : frameName
                }
        # self.activeData = data
        # self.activeUrl = self.frameUrl
        command = Command()
        command.data = data
        command.url = url
        self.insertToQueue(command)
        return command

    def setCmsCode(self, bid : int, value : int, cmsCode : str, url : str) -> Command:
        data =  { 'bid' : bid,
                  'cms_write' : value,
                  'cms_code' : cmsCode
                }
        # self.activeData = data
        # self.activeUrl = self.frameUrl
        command = Command()
        command.data = data
        command.url = url
        self.insertToQueue(command)
        return command

    def setBaseCode(self, bid : int, value : int, baseCode : str, url : str) -> Command:
        data =  { 'bid' : bid,
                  'base_write' : value,
                  'base_code' : baseCode
                }
        # self.activeData = data
        # self.activeUrl = self.frameUrl
        command = Command()
        command.data = data
        command.url = url
        self.insertToQueue(command)
        return command

    def setMcuCode(self, bid : int, value : int, mcuCode : str, url : str) -> Command:
        data =  { 'bid' : bid,
                  'mcu_write' : value,
                  'mcu_code' : mcuCode
                }
        # self.activeData = data
        # self.activeUrl = self.frameUrl
        command = Command()
        command.data = data
        command.url = url
        self.insertToQueue(command)
        return command

    def setSiteLocation(self, bid : int, value : int, siteLocation : str, url : str) -> Command:
        data =  { 'bid' : bid,
                  'site_write' : value,
                  'site_location' : siteLocation
                }
        # self.activeData = data
        # self.activeUrl = self.frameUrl
        command = Command()
        command.data = data
        command.url = url
        self.insertToQueue(command)
        return command

    def restartCms(self, bid : int, value : int, url : str) -> Command:
        data =  { 'bid' : bid,
                  'restart' : value
                }
        # self.activeData = data
        # self.activeUrl = self.restartCmsUrl
        command = Command()
        command.data = data
        command.url = url
        self.insertToQueue(command)
        return command

    def restartRms(self, value : int, url : str) -> Command:
        data =  { 'restart' : value
                }
        # self.activeData = data
        # self.activeUrl = self.restartRmsUrl
        command = Command()
        command.data = data
        command.url = url
        self.insertToQueue(command)
        return command

    def insertToQueue(self, command : Command) :
        self.commandList.append(command)
        