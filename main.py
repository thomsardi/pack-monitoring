from multiprocessing import Event
import sys
import os
import json
import webbrowser
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
# import mysql.connector
# from mysql.connector import Error

searchPath = os.getcwd() + "\\resources"
sys.path.append(searchPath)

from resources.window_ui.ui_py.HomeWindow import HomeWindowUi
from resources.window_ui.ui_py.BatteryDetails import BatteryDetailsUi
from resources.window_ui.ui_py.RmsWindow import RmsWindow
from resources.window_ui.ui_py.ChargerWindow import ChargerWindow
from resources.window_ui.ui_py.InverterWindow import InverterWindow
from resources.window_ui.ui_py.MainInfoWindow import MainInfoWindowUi
from resources.window_ui.ui_py.MainWindowTest import MainWindowTest

from resources.modules.BatteryData import BatteryData
from resources.modules.ChargerRequest import ChargerRequest
from resources.modules.RmsRequest import RmsRequest
from resources.modules.InverterData import InverterData
from resources.modules.InverterRequest import InverterRequest
from resources.modules.ParameterData import VoltageParameter
from resources.modules.ParameterData import TemperatureParameter
from resources.modules.ChargerData import ChargerData 

from resources.definition import RESOURCES_DIR

class MainScreen2(qtw.QMainWindow) :
     def __init__(self, *args, **kwargs) :
        super().__init__()
        self.ui = MainWindowTest()
        self.ui.homeWindow.setupUi(self)
        self.tabCustom = qtw.QWidget()
        self.tabCustom.setObjectName("tabCustom")
        self.ui.homeWindow.tabWidget.addTab(self.tabCustom, "asd")
        self.ui.homeWindow.horizontalLayout.addWidget(self.ui.homeWindow.tabWidget)

class MainScreen(qtw.QMainWindow) :
    def __init__(self, *args, **kwargs) :
        super().__init__()
        self.tabNameList = []
        self.isChargeStart = False
        self.lastChargeStart = False
        self.__stopFlag = Event()
        self.maxVoltage = 3600
        self.minVoltage = 3100
        self.minTemperature = 20000
        self.maxTemperature = 80000
        self.chargerVoltage = 0
        self.chargerTotalCurrent = 0
        self.chargerTotalPower = 0
        self.lastSubAddress = 0
        self.lastVoltage = 0
        self.numberOfData = 0
        self.deviceCount = 0
        self.currentBatteryData : list[dict] = []
        self.grafanaUrlList = [
            "http://192.168.2.25:3000/d/DZJsQrAVk/cycling-station-pack-1?orgId=1&refresh=5s",
            "http://192.168.2.25:3000/d/xXQnzCAVk/cycling-station-pack-2?orgId=1&refresh=5s",
            "http://192.168.2.25:3000/d/zPd0nC0Vk/cycling-station-pack-3?orgId=1&refresh=5s",
            "http://192.168.2.25:3000/d/ZBAbnj0Vz/cycling-station-pack-4?orgId=1&refresh=5s",
            "http://192.168.2.25:3000/d/_FCYnj0Vz/cycling-station-pack-5?orgId=1&refresh=5s",
            "http://192.168.2.25:3000/d/iD9_nC04z/cycling-station-pack-6?orgId=1&refresh=5s",
            "http://192.168.2.25:3000/d/F_f37CAVk/cycling-station-pack-7?orgId=1&refresh=5s",
            "http://192.168.2.25:3000/d/4z-G4j0Vz/cycling-station-pack-8?orgId=1&refresh=5s"
        ]
        
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        element = data["ip_list"]
        self.deviceCount = len(element)
        # print(self.deviceCount)
        for i in range(self.deviceCount) :
            self.tabNameList.append(data['ip_list'][i]['rms_url']['ip'])
        # Window UI
        self.mainInfoWindow : list[MainInfoWindowUi] = []
        for i in range(self.deviceCount) :
            window = MainInfoWindowUi()
            self.mainInfoWindow.append(window)
        
        self.ui = HomeWindowUi()        
        self.batteryDetailsUi : list[BatteryDetailsUi] = []
        for i in range(8):
            window = BatteryDetailsUi()
            self.batteryDetailsUi.append(window)
        
        self.rmsUi = RmsWindow()
        self.rmsUi.command.connect(lambda c : self.rmsRequest.insertToQueue(c))
        self.rmsUi.voltageParameter.connect(self.updateVoltageParameter)
        self.rmsUi.temperatureParameter.connect(self.updateTemperatureParameter)
        
        self.chargerUi = ChargerWindow()
        self.chargerUi.command.connect(lambda c : self.chargerRequest.insertToQueue(c))

        self.inverterUi = InverterWindow()
        self.inverterUi.command.connect(lambda c : self.inverterRequest.insertToQueue(c))

        # Thread
        self.chargerRequest = ChargerRequest()
        self.chargerRequest.isRun = True
        self.chargerRequest.chargerData.connect(self.updateChargerDisplay)
        self.chargerRequest.status.connect(self.chargerUi.showMessageBox)
        self.chargerRequest.start()
        
        self.rmsRequest = RmsRequest()
        self.rmsRequest.isRun = True
        self.rmsRequest.batteryData.connect(self.batteryDataReady)
        self.rmsRequest.batteryData.connect(self.checkCharger)
        self.rmsRequest.batteryData.connect(self.updateLcd)
        self.rmsRequest.failedToGetData.connect(self.updateFailed)
        self.rmsRequest.status.connect(self.rmsUi.showMessageBox)
        self.rmsRequest.start()
        
        self.inverterRequest = InverterRequest()
        self.inverterRequest.isRun = True
        self.inverterRequest.inverterData.connect(self.inverterDataReady)
        self.inverterRequest.inverterData.connect(self.updateInverterDisplay)
        self.inverterRequest.status.connect(self.inverterUi.showMessageBox)
        self.inverterRequest.start()

        self.ui.homeWindow.setupUi(self)
        self.addCustomWidget()
        self.activeWidget = self.getCurrentWidget()
        # print(self.getCurrentIndex())
        self.ui.homeWindow.tabWidget.currentChanged.connect(self.tabIndexChanged)

        self.__firstRender()

    def addCustomWidget(self) :
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        tabCustom : list[MainInfoWindowUi] = []
        for x in range(self.deviceCount) :
            window = MainInfoWindowUi()
            label = "window_%i"%(x+1)
            window.setObjectName(label)
            # tabName = "RMS %i"%(x+1)
            tabName = self.tabNameList[x]
            # print(tabName)
            self.ui.homeWindow.tabWidget.addTab(window, tabName)
            tabCustom.append(window)
            for p in window.packList :
                p.installEventFilter(self)
            palette = window.homeWindow.bdiVoltage.palette()
            style = qtw.QLCDNumber.Flat
            palette.setColor(palette.WindowText, qtg.QColor(255, 0, 0))
            palette.setColor(palette.Background, qtg.QColor(0, 0, 0))

            window.homeWindow.packVoltage.setPalette(palette)
            window.homeWindow.packContent.setPalette(palette)
            window.homeWindow.chargerVoltage.setPalette(palette)
            window.homeWindow.chargerCurrent.setPalette(palette)
            window.homeWindow.chargerPower.setPalette(palette)
            window.homeWindow.bdiVoltage.setPalette(palette)
            window.homeWindow.bdiCurrent.setPalette(palette)
            window.homeWindow.bdiPower.setPalette(palette)

            window.homeWindow.packVoltage.setSegmentStyle(style)
            window.homeWindow.chargerVoltage.setSegmentStyle(style)
            window.homeWindow.chargerCurrent.setSegmentStyle(style)
            window.homeWindow.chargerPower.setSegmentStyle(style)
            window.homeWindow.bdiVoltage.setSegmentStyle(style)
            window.homeWindow.bdiCurrent.setSegmentStyle(style)
            window.homeWindow.bdiPower.setSegmentStyle(style)
            window.homeWindow.packContent.setSegmentStyle(style)
            window.homeWindow.rms.clicked.connect(self.rmsClicked)
            window.homeWindow.charger.clicked.connect(self.chargerClicked)
            window.homeWindow.bidirectionalinverter.clicked.connect(self.inverterClicked)

            window.homeWindow.pack1.clicked.connect(self.pack1Clicked)
            window.homeWindow.pack2.clicked.connect(self.pack2Clicked)
            window.homeWindow.pack3.clicked.connect(self.pack3Clicked)
            window.homeWindow.pack4.clicked.connect(self.pack4Clicked)
            window.homeWindow.pack5.clicked.connect(self.pack5Clicked)
            window.homeWindow.pack6.clicked.connect(self.pack6Clicked)
            window.homeWindow.pack7.clicked.connect(self.pack7Clicked)
            window.homeWindow.pack8.clicked.connect(self.pack8Clicked)

        self.ui.homeWindow.horizontalLayout.addWidget(self.ui.homeWindow.tabWidget)

    def getWidget(self, index : int) -> MainInfoWindowUi :
        return self.ui.homeWindow.tabWidget.widget(index)

    def getCurrentWidget(self) -> MainInfoWindowUi :
        return self.ui.homeWindow.tabWidget.currentWidget()
    
    def getCurrentIndex(self) -> int :
        return self.ui.homeWindow.tabWidget.currentIndex()
    
    def tabIndexChanged(self) :
        index = self.ui.homeWindow.tabWidget.currentIndex()
        self.ui.homeWindow.tabWidget.setCurrentIndex(index)
        self.activeWidget = self.getCurrentWidget()
        self.activeWidget.homeWindow.ipAddressLineEdit.setText(self.tabNameList[index])

    def eventFilter(self, object, event : qtc.QEvent) -> bool:
        number = 0
        index = self.getCurrentIndex() + 1
        data : BatteryData = None
        for x in self.currentBatteryData :
            if x['index'] == index :
                data : list[BatteryData] = x['data']
                break
        
        if not data :
            return False

        if not self.currentBatteryData :
            return False
        if (event.type() == qtc.QEvent.Enter) :
            for x in self.activeWidget.packList : 
                if object is x:
                    self.activeWidget.homeWindow.framelineEdit.setText(data[number].frameName)
                    self.activeWidget.homeWindow.cmscodelineEdit.setText(data[number].cmsCode)
                    self.activeWidget.homeWindow.basecodelineEdit.setText(data[number].baseCode)
                    self.activeWidget.homeWindow.mcucodelineEdit.setText(data[number].mcuCode)
                    self.activeWidget.homeWindow.sitelocationlineEdit.setText(data[number].siteLocation)
                    self.activeWidget.homeWindow.bidlineEdit.setText(str(data[number].bid))
                    if(data[number].wakeStatus) :
                        self.activeWidget.homeWindow.statuslineEdit.setText("Wake")
                    else :
                        self.activeWidget.homeWindow.statuslineEdit.setText("Sleep")
                    if(data[number].doorStatus) :
                        self.activeWidget.homeWindow.doorlineEdit.setText("Closed")
                    else :
                        self.activeWidget.homeWindow.doorlineEdit.setText("Opened")
                    totalPack = round(sum(data[number].vpack)/1000,1)
                    content = round(100*(totalPack - 80) / (112-80),1)
                    if (content < 0) :
                        content = 0
                    self.activeWidget.homeWindow.packVoltage.display(totalPack)
                    self.activeWidget.homeWindow.packContent.display(content)
                    return True
                number += 1
        elif event.type() == qtc.QEvent.Leave:
            self.activeWidget.homeWindow.framelineEdit.clear()
            self.activeWidget.homeWindow.cmscodelineEdit.clear()
            self.activeWidget.homeWindow.basecodelineEdit.clear()
            self.activeWidget.homeWindow.mcucodelineEdit.clear()
            self.activeWidget.homeWindow.sitelocationlineEdit.clear()
            self.activeWidget.homeWindow.bidlineEdit.clear()
            self.activeWidget.homeWindow.statuslineEdit.clear()
            self.activeWidget.homeWindow.doorlineEdit.clear()
            self.activeWidget.homeWindow.packVoltage.display(0)
            self.activeWidget.homeWindow.packContent.display(0)
        return False
            
    def inverterClicked(self) :
        self.inverterUi.close()
        self.inverterUi.show()

    def rmsClicked(self) :
        activeWidgetIndex = self.getCurrentIndex()
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        arrData = data["ip_list"][activeWidgetIndex]
        ip = arrData['rms_url']['ip']
        self.rmsUi.close()
        self.rmsUi.updateIpLineEdit(ip)
        self.rmsUi.setActiveWidgetIndex(activeWidgetIndex)
        self.rmsUi.show()

    def chargerClicked(self) :
        self.chargerUi.close()
        activeWidgetIndex = self.getCurrentIndex()
        f = open(os.path.join(RESOURCES_DIR,'resources', 'config.json'))
        data = json.load(f)
        arrData = data["ip_list"][activeWidgetIndex]
        ip = arrData['charger_url']['ip']
        self.chargerUi.updateIpLineEdit(ip)
        self.chargerUi.setActiveWidgetIndex(activeWidgetIndex)
        self.chargerUi.show()

    def startDataClicked(self, value : int) :
        pass

    def pack1Clicked(self) :
        window = self.batteryDetailsUi[0]
        window.close()
        window.show()
        # webbrowser.open(self.grafanaUrlList[0])

    def pack2Clicked(self) :
        window = self.batteryDetailsUi[1]
        window.close()
        window.show()
        # webbrowser.open(self.grafanaUrlList[1])

    def pack3Clicked(self) :
        window = self.batteryDetailsUi[2]
        window.close()
        window.show()
        # webbrowser.open(self.grafanaUrlList[2])

    def pack4Clicked(self) :
        window = self.batteryDetailsUi[3]
        window.close()
        window.show()
        # webbrowser.open(self.grafanaUrlList[3])

    def pack5Clicked(self) :
        window = self.batteryDetailsUi[4]
        window.close()
        window.show()
        # webbrowser.open(self.grafanaUrlList[4])

    def pack6Clicked(self) :
        window = self.batteryDetailsUi[5]
        window.close()
        window.show()
        # webbrowser.open(self.grafanaUrlList[5])

    def pack7Clicked(self) :
        window = self.batteryDetailsUi[6]
        window.close()
        window.show()
        # webbrowser.open(self.grafanaUrlList[6])

    def pack8Clicked(self) :
        window = self.batteryDetailsUi[7]
        window.close()
        window.show()
        # webbrowser.open(self.grafanaUrlList[7])

    def __firstRender(self) :
        self.__stopFlag.clear()

    def updateLed(self, flag : bool) :
        if(flag) :
            pass
            # self.ui.connectstatuspushButton.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(0, 255, 0);\n}")
        else :
            pass
            # self.ui.connectstatuspushButton.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(34, 34, 34);\n}")

    def getChargeStatus(self, isChargeStart : int) :
        self.isChargeStart = isChargeStart

    def updateVoltageParameter(self, voltageParameter : VoltageParameter) :
        self.maxVoltage = voltageParameter.max
        self.minVoltage = voltageParameter.min
        print("Updating Voltage Parameter")
        print("Max Voltage : ", self.maxVoltage)
        print("Min Voltage : ", self.minVoltage)
        
    def updateTemperatureParameter(self, temperatureParameter : TemperatureParameter) :
        self.maxTemperature = temperatureParameter.max
        self.minTemperature = temperatureParameter.min
        print("Updating Temperature Parameter")
        print("Max Temperature : ", self.maxTemperature)
        print("Min Temperature : ", self.minTemperature)


    def updateFailed(self, failedToGetData : int, dataIndex : int) :
        widget = self.getWidget(dataIndex-1)
        if(failedToGetData) :
            for x in widget.statusList :
                x.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(0, 0, 0);\n}")
            # self.activeWidget.homeWindow.packstatus1.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(0, 0, 0);\n}")
            # self.activeWidget.homeWindow.packstatus2.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(0, 0, 0);\n}")
            # self.activeWidget.homeWindow.packstatus3.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(0, 0, 0);\n}")
            # self.activeWidget.homeWindow.packstatus4.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(0, 0, 0);\n}")
            # self.activeWidget.homeWindow.packstatus5.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(0, 0, 0);\n}")
            # self.activeWidget.homeWindow.packstatus6.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(0, 0, 0);\n}")
            # self.activeWidget.homeWindow.packstatus7.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(0, 0, 0);\n}")
            # self.activeWidget.homeWindow.packstatus8.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(0, 0, 0);\n}")

    def batteryDataReady(self, batteryData : list[BatteryData], dataIndex : int, ipName : str) :
        isFound = False
        for x in self.currentBatteryData :
            if x['index'] == dataIndex :
                x['data'] = batteryData.copy()
                isFound = True
                break

        if (not isFound) :
            data = {
                'index' : dataIndex,
                'data' : batteryData.copy()
            }    
            self.currentBatteryData.append(data)

        # print(len(self.currentBatteryData))
        index = dataIndex-1
        widget = self.getWidget(index)
        tabBar = self.ui.homeWindow.tabWidget.tabBar()
        widget.homeWindow.ipAddressLineEdit.setText(ipName)
        # print("Index : %i" % (dataIndex))
        statusLed : qtw.QPushButton
        statusVcell = True
        statusTemperature = True
        tabBar.setTabText(index, ipName)
        for dat in batteryData :            
            # print(dat.vcell)
            # print(dat.vpack)
            # print(dat.temperature)
            isVcellOk = False
            isTemperatureOk = False
            if(dat.bid <= 0) :
                continue
            
            for v in dat.vcell :
                if (v < 100 or (v > self.minVoltage and v < self.maxVoltage and v > 0)) :
                    isVcellOk = True
                else :
                    isVcellOk = False
                    statusVcell = False
                    break

            if not isVcellOk :
                statusLed = widget.statusList[dat.bid-1]
                statusLed.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(255, 0, 0);\n}")
                tabBar.setTabTextColor(index, qtg.QColor(255, 0, 0))
                continue
                # if dat.bid == 1 :
                #     widget.homeWindow.packstatus1.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(255, 0, 0);\n}")
                # elif dat.bid == 2 :
                #     self.activeWidget.homeWindow.packstatus2.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(255, 0, 0);\n}")
                # elif dat.bid == 3 :
                #     self.activeWidget.homeWindow.packstatus3.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(255, 0, 0);\n}")
                # elif dat.bid == 4 :
                #     self.activeWidget.homeWindow.packstatus4.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(255, 0, 0);\n}")
                # elif dat.bid == 5 :
                #     self.activeWidget.homeWindow.packstatus5.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(255, 0, 0);\n}")
                # elif dat.bid == 6 :
                #     self.activeWidget.homeWindow.packstatus6.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(255, 0, 0);\n}")
                # elif dat.bid == 7 :
                #     self.activeWidget.homeWindow.packstatus7.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(255, 0, 0);\n}")
                # elif dat.bid == 8 :
                #     self.activeWidget.homeWindow.packstatus8.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(255, 0, 0);\n}")
                # continue

            for t in dat.temperature :
                if (t > self.minTemperature and t < self.maxTemperature) :
                    isTemperatureOk = True
                else :
                    isTemperatureOk = False
                    statusTemperature = False
                    break

            if not isTemperatureOk :
                statusLed = widget.statusList[dat.bid-1]
                statusLed.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(255, 0, 0);\n}")
                tabBar.setTabTextColor(index, qtg.QColor(255, 0, 0))
                continue
                # if dat.bid == 1 :
                #     self.activeWidget.homeWindow.packstatus1.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(255, 0, 0);\n}")
                # elif dat.bid == 2 :
                #     self.activeWidget.homeWindow.packstatus2.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(255, 0, 0);\n}")
                # elif dat.bid == 3 :
                #     self.activeWidget.homeWindow.packstatus3.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(255, 0, 0);\n}")
                # elif dat.bid == 4 :
                #     self.activeWidget.homeWindow.packstatus4.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(255, 0, 0);\n}")
                # elif dat.bid == 5 :
                #     self.activeWidget.homeWindow.packstatus5.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(255, 0, 0);\n}")
                # elif dat.bid == 6 :
                #     self.activeWidget.homeWindow.packstatus6.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(255, 0, 0);\n}")
                # elif dat.bid == 7 :
                #     self.activeWidget.homeWindow.packstatus7.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(255, 0, 0);\n}")
                # elif dat.bid == 8 :
                #     self.activeWidget.homeWindow.packstatus8.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(255, 0, 0);\n}")
                # continue
            
            statusLed = widget.statusList[dat.bid-1]
            statusLed.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(0, 255, 0);\n}")          

            # if dat.bid == 1 :
            #     self.activeWidget.homeWindow.packstatus1.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(0, 255, 0);\n}")
            # elif dat.bid == 2 :
            #     self.activeWidget.homeWindow.packstatus2.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(0, 255, 0);\n}")
            # elif dat.bid == 3 :
            #     self.activeWidget.homeWindow.packstatus3.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(0, 255, 0);\n}")
            # elif dat.bid == 4 :
            #     self.activeWidget.homeWindow.packstatus4.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(0, 255, 0);\n}")
            # elif dat.bid == 5 :
            #     self.activeWidget.homeWindow.packstatus5.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(0, 255, 0);\n}")
            # elif dat.bid == 6 :
            #     self.activeWidget.homeWindow.packstatus6.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(0, 255, 0);\n}")
            # elif dat.bid == 7 :
            #     self.activeWidget.homeWindow.packstatus7.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(0, 255, 0);\n}")
            # elif dat.bid == 8 :
            #     self.activeWidget.homeWindow.packstatus8.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(0, 255, 0);\n}")
        if(statusVcell and statusTemperature) :
            tabBar.setTabTextColor(index, qtg.QColor(58, 163, 54))
                

    def checkCharger(self, batteryData : list[BatteryData]) :
        for dat in batteryData :
            isVcellOk = False
            isTemperatureOk = False
            
            if(dat.bid <= 0) :
                continue
            
            for v in dat.vcell :
                if (v < 100 or (v < self.maxVoltage and v > 0)) :
                    isVcellOk = True
                else :
                    isVcellOk = False
                    break

            for t in dat.temperature :
                if (t > self.minTemperature and t < self.maxTemperature) :
                    isTemperatureOk = True
                else :
                    isTemperatureOk = False
                    break
            
            if(not isTemperatureOk or not isVcellOk) :
                if (self.chargerUi.isChargerStart) :
                        self.chargerUi.stop()

    def dataReady(self, batteryData : BatteryData) :
        # pass
        # print("Vcell : ", batteryData.getVcell())
        # print("Temp : ", batteryData.getTemp())
        # print("Vpack : ", batteryData.getVpack())
        vcell = batteryData.vcell      
        temp = batteryData.temperature
        vpack = batteryData.vpack

        # for x in vcell :
        #     if (x > 3600) :
        #         if(self.isChargeStart != self.lastChargeStart) :
        #             self.lastChargeStart = self.isChargeStart
        #             print("Stop Charge")
        #         break
 
    
    def inverterDataReady(self, inverterData : list) :
        pass
    
    def updateChargerDisplay(self, chargerData : ChargerData, dataIndex : int) :
        # print("updated")
        index = dataIndex - 1
        indexToUpdate = index - 1
        if(chargerData.subAddress < self.lastSubAddress) :
            if (indexToUpdate < 0) :
                indexToUpdate = self.deviceCount-1
            widget = self.getWidget(indexToUpdate)
            voltage = self.chargerVoltage / 10
            totalCurrent = self.chargerTotalCurrent / 100
            totalPower = self.chargerTotalPower
            
            value = round(voltage)
            digitCount = self.digitCount(value)
            if(digitCount < 3) :
                widget.homeWindow.chargerVoltage.display(round(voltage, 3 - digitCount))
            else :
                widget.homeWindow.chargerVoltage.display(round(voltage))

            value = round(totalCurrent)
            digitCount = self.digitCount(value)
            if(digitCount < 3) :
                widget.homeWindow.chargerCurrent.display(round(totalCurrent, 3 - digitCount))
            else :
                widget.homeWindow.chargerCurrent.display(round(totalCurrent))

            value = round(totalPower)
            digitCount = self.digitCount(value)
            if(digitCount < 3) :
                widget.homeWindow.chargerPower.display(round(totalPower, 3 - digitCount))
            else :
                widget.homeWindow.chargerPower.display(round(totalPower))
            self.lastVoltage = 0
            self.chargerTotalCurrent = 0
            self.chargerTotalPower = 0

        if(not chargerData.moduleOff) :
            voltage = chargerData.voltage
            if (voltage > self.lastVoltage) :
                self.chargerVoltage = voltage
            else :
                self.chargerVoltage = self.lastVoltage
            self.chargerTotalPower += (chargerData.voltage / 10 * chargerData.current / 100) / 1000 #in Kw
            self.chargerTotalCurrent += chargerData.current
            # print("Current : ", chargerData.current)
            # print("Total Current : ", self.chargerTotalCurrent)
        self.lastSubAddress = chargerData.subAddress

    def updateInverterDisplay(self, inverterData : list[InverterData], dataIndex : int) :
        print("update inverter display")
        index = dataIndex-1
        widget = self.getWidget(index)
        data = inverterData.copy()
        lastVoltage = 0
        totalCurrent = 0
        totalPower = 0
        for d in data :
            if(d.systemDcVoltage > lastVoltage) :
                lastVoltage = d.systemDcVoltage
            totalCurrent += d.systemDcCurrent
            totalPower += (d.systemDcVoltage / 1000) * (d.systemDcCurrent / 1000) / 1000

        lastVoltage = lastVoltage / 1000
        totalCurrent = totalCurrent / 1000    
        value = round(lastVoltage)
        digitCount = self.digitCount(value)
        if(digitCount < 3) :
            widget.homeWindow.bdiVoltage.display(round(lastVoltage, 3 - digitCount))
        else :
            widget.homeWindow.bdiVoltage.display(round(lastVoltage))

        value = round(totalCurrent)
        digitCount = self.digitCount(value)
        if(digitCount < 3) :
            widget.homeWindow.bdiCurrent.display(round(totalCurrent, 3 - digitCount))
        else :
            widget.homeWindow.bdiCurrent.display(round(totalCurrent))

        value = round(totalPower)
        digitCount = self.digitCount(value)
        if(digitCount < 3) :
            widget.homeWindow.bdiPower.display(round(totalPower, 3 - digitCount))
        else :
            widget.homeWindow.bdiPower.display(round(totalPower))

    def updateLcd(self, batteryData : list[BatteryData], dataIndex : int) :
        if (self.getCurrentIndex() != (dataIndex - 1)) :
            return
        
        for dat in batteryData :
            vcell = dat.vcell.copy()        
            temp = dat.temperature.copy()
            vpack = dat.vpack.copy()
            index = dat.bid - 1
            if(index >= 0 and index < 8) :
                batUi : BatteryDetailsUi = self.batteryDetailsUi[index]
                number = vcell.pop(0)
                batUi.ui.lcdNumber.display(number)
                batUi.ui.progressBar.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_2.display(number)
                batUi.ui.progressBar_2.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_3.display(number)
                batUi.ui.progressBar_3.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_4.display(number)
                batUi.ui.progressBar_4.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_5.display(number)
                batUi.ui.progressBar_5.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_6.display(number)
                batUi.ui.progressBar_6.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_7.display(number)
                batUi.ui.progressBar_7.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_8.display(number)
                batUi.ui.progressBar_8.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_9.display(number)
                batUi.ui.progressBar_9.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_10.display(number)
                batUi.ui.progressBar_10.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_11.display(number)
                batUi.ui.progressBar_11.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_12.display(number)
                batUi.ui.progressBar_12.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_13.display(number)
                batUi.ui.progressBar_13.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_14.display(number)
                batUi.ui.progressBar_14.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_15.display(number)
                batUi.ui.progressBar_15.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vpack.pop(0)
                batUi.ui.lcdNumberp.display(number)
                batUi.ui.progressBarp.setValue(self.__convertToPercent(number, 30000, 37000))
                number = temp.pop(0)
                batUi.ui.lcdNumber_t1.display(number / 1000)
                number = temp.pop(0)
                batUi.ui.lcdNumber_t2.display(number / 1000)
                number = temp.pop(0)
                batUi.ui.lcdNumber_t3.display(number / 1000)
                number = vcell.pop(0)
                batUi.ui.lcdNumber_16.display(number)
                batUi.ui.progressBar_16.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_17.display(number)
                batUi.ui.progressBar_17.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_18.display(number)
                batUi.ui.progressBar_18.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_19.display(number)
                batUi.ui.progressBar_19.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_20.display(number)
                batUi.ui.progressBar_20.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_21.display(number)
                batUi.ui.progressBar_21.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_22.display(number)
                batUi.ui.progressBar_22.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_23.display(number)
                batUi.ui.progressBar_23.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_24.display(number)
                batUi.ui.progressBar_24.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_25.display(number)
                batUi.ui.progressBar_25.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_26.display(number)
                batUi.ui.progressBar_26.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_27.display(number)
                batUi.ui.progressBar_27.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_28.display(number)
                batUi.ui.progressBar_28.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_29.display(number)
                batUi.ui.progressBar_29.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_30.display(number)
                batUi.ui.progressBar_30.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vpack.pop(0)
                batUi.ui.lcdNumberp_2.display(number)
                batUi.ui.progressBarp_2.setValue(self.__convertToPercent(number, 30000, 37000))
                number = temp.pop(0)
                batUi.ui.lcdNumber_t1_2.display(number / 1000)
                number = temp.pop(0)
                batUi.ui.lcdNumber_t2_2.display(number / 1000)
                number = temp.pop(0)
                batUi.ui.lcdNumber_t3_2.display(number / 1000)
                number = vcell.pop(0)
                batUi.ui.lcdNumber_31.display(number)
                batUi.ui.progressBar_31.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_32.display(number)
                batUi.ui.progressBar_32.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_33.display(number)
                batUi.ui.progressBar_33.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_34.display(number)
                batUi.ui.progressBar_34.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_35.display(number)
                batUi.ui.progressBar_35.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_36.display(number)
                batUi.ui.progressBar_36.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_37.display(number)
                batUi.ui.progressBar_37.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_38.display(number)
                batUi.ui.progressBar_38.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_39.display(number)
                batUi.ui.progressBar_39.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_40.display(number)
                batUi.ui.progressBar_40.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_41.display(number)
                batUi.ui.progressBar_41.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_42.display(number)
                batUi.ui.progressBar_42.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_43.display(number)
                batUi.ui.progressBar_43.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_44.display(number)
                batUi.ui.progressBar_44.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vcell.pop(0)
                batUi.ui.lcdNumber_45.display(number)
                batUi.ui.progressBar_45.setValue(self.__convertToPercent(number, 3000, 3700))
                number = vpack.pop(0)
                batUi.ui.lcdNumberp_3.display(number)
                batUi.ui.progressBarp_3.setValue(self.__convertToPercent(number, 36000, 44400))
                number = temp.pop(0)
                batUi.ui.lcdNumber_t1_3.display(number / 1000)
                number = temp.pop(0)
                batUi.ui.lcdNumber_t2_3.display(number / 1000)
                number = temp.pop(0)
                batUi.ui.lcdNumber_t3_3.display(number / 1000)


    def __convertToPercent(self, input : int, min : int, max : int) -> int :
        if (input < min) :
            input = min
        elif (input > max) :
            input = max
        percent = (input - min) * 100 / (max - min)
        return int(percent) 

    def digitCount(self, number : int) :
        return len(str(number))
      

    def closeEvent(self, event: qtg.QCloseEvent):
        print("Main Window Close")
        print("Stopping Thread..")
        self.rmsUi.close()
        self.chargerUi.close()
        self.inverterUi.close()
        print("Thread Stopped")
        event.accept()
        
            
if __name__ == '__main__' :
    app = qtw.QApplication([])
    widget = MainScreen()
    widget.show()
    # widget = MainScreen2()
    # widget.show()
    app.exec_()