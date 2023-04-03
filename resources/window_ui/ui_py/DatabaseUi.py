import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

import mysql.connector
from mysql.connector import Error
from ..databaseconnection import Ui_databaseForm
from ...modules.BatteryData import BatteryData
from ...modules.ReadDatabase import ReadDatabase
from ...modules.UpdateDatabaseName import UpdateDatabaseName
from ...modules.DatabaseInfo import DatabaseInfo


class DatabaseUi(qtw.QWidget) :
    dataReady = qtc.pyqtSignal(BatteryData)
    isDatabaseConnected = qtc.pyqtSignal(bool)
    def __init__(self) -> None:
        super().__init__()
        self.databaseUi = Ui_databaseForm()
        self.databaseUi.setupUi(self)
        self.databaseUi.testConnectionpushButton.clicked.connect(self.testConnection)
        self.databaseUi.connectpushButton.clicked.connect(self.connect)
        self.databaseUi.databaseNamecomboBox.currentIndexChanged.connect(self.databaseNameCurrentIndexChanged)
        self.databaseUi.tableNamecomboBox.currentIndexChanged.connect(self.tableNameCurrentIndexChanged)
        self.databaseUi.databaseNamecomboBox.setCurrentIndex(0)
        self.databaseUi.tableNamecomboBox.setCurrentIndex(0)
        self.databaseUi.hostNamelineEdit.setText("localhost")
        self.databaseUi.usernameLineEdit.setText("rndpc")
        self.databaseConnection = None
        self.readThread = None
        self.isConnected = False
        self.updateDatabaseName = UpdateDatabaseName()
        self.updateTableName = UpdateDatabaseName()

    def testConnection(self) :
        hostname = self.databaseUi.hostNamelineEdit.text()
        username = self.databaseUi.usernameLineEdit.text()
        password = self.databaseUi.passwordLineEdit.text()
        connection = self.createConnection(hostname, username, password)
        if(connection is None) :
            self.databaseUi.databaseNamecomboBox.clear()
            self.databaseUi.databaseNamecomboBox.setCurrentIndex(0)
            self.databaseUi.tableNamecomboBox.clear()
            self.databaseUi.tableNamecomboBox.setCurrentIndex(0)
            print("Connection is None")
            return
        self.getDatabaseNameList(connection)
        # self.__updateDatabaseNameComboBox(connection)
        # databaseName = self.databaseUi.databaseNamecomboBox.currentText()
        # connection = self.createConnection(hostname, username, password, databaseName)
        # if(connection is None) :
        #     self.databaseConnection = None
        #     return
        # self.getTableNameList(connection)
        # self.__updateTableNameComboBox(connection)
        # self.databaseConnection = connection

    def connect(self) : 
        if(self.isConnected) :
            if(self.readThread is not None) :
                self.readThread.isRun = False
                self.readThread.exit()
                while(not self.readThread.isFinished()) :
                    pass
            # print("Disconnect")
            self.isConnected = False
        else :
            tableName = self.databaseUi.tableNamecomboBox.currentText()
            databaseInfo = DatabaseInfo(self.databaseConnection, tableName)
            readThread = ReadDatabase()
            readThread.setDatabaseInfo(databaseInfo)
            readThread.isRun = True
            readThread.isDone.connect(self.update)
            readThread.start()
            self.readThread = readThread
            self.isConnected = True
            # print("Connect")
        if(self.isConnected) :
            self.databaseUi.connectpushButton.setText("Disconnect")
        else :
            self.databaseUi.connectpushButton.setText("Connect")
        self.sendSignal()

    def databaseNameCurrentIndexChanged(self) :
        if(self.readThread is not None) :
            self.readThread.isRun = False
            self.readThread.exit()
            while(not self.readThread.isFinished()) :
                pass  
            self.databaseUi.connectpushButton.setText("Connect")
            self.isConnected = False
        else :
            self.isConnected = False
            self.databaseUi.connectpushButton.setText("Connect")
        
        hostname = self.databaseUi.hostNamelineEdit.text()
        username = self.databaseUi.usernameLineEdit.text()
        password = self.databaseUi.passwordLineEdit.text()
        databaseName = self.databaseUi.databaseNamecomboBox.currentText()
        if (databaseName == "" or databaseName is None) :
            return
        connection = self.createConnection(hostname, username, password, databaseName)
        if(connection is None) :
            self.databaseConnection = None
            return
        self.getTableNameList(connection)
        # self.__updateTableNameComboBox(connection)
        self.databaseConnection = connection
        self.sendSignal()

    def tableNameCurrentIndexChanged(self) :
        if(self.readThread is not None) :
            self.readThread.isRun = False    
            self.readThread.exit()
            while(not self.readThread.isFinished()) :
                pass
            self.databaseUi.connectpushButton.setText("Connect")
            self.isConnected = False
        else :
            self.isConnected = False
            self.databaseUi.connectpushButton.setText("Connect")
        self.sendSignal()
            
    def createConnection(self, hostname, username, password, databaseName = None) :
        connection = None
        try:
            # connection = mysql.connector.connect(
            # host = hostname,
            # user = username,
            # passwd = password,
            # database = databaseName
            # )
            connection = mysql.connector.connect(
            host = hostname,
            user = username,
            passwd = password,
            database = databaseName
            )
            print("MySQL Database connection successful")
            self.databaseUi.connectionLed.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(0, 255, 0);\n}")
        except Error as err:
            print(f"Error: '{err}'")
            self.databaseUi.connectionLed.setStyleSheet("QPushButton{\n	border-radius : 8px;\n	background-color: rgb(255, 0, 0);\n}")
        return connection

    def update(self, batteryData : BatteryData) :
        self.dataReady.emit(batteryData)

    def sendSignal(self) : 
        self.isDatabaseConnected.emit(self.isConnected)

    # def __updateTableNameComboBox(self, connection : mysql.connector.connection_cext.CMySQLConnection) :
    #     if(connection is None) :
    #         return
    #     self.databaseUi.tableNamecomboBox.setCurrentIndex(0)
    #     self.databaseUi.tableNamecomboBox.clear()
    #     dbCursor = connection.cursor()
    #     dbCursor.execute("SHOW TABLES")
    #     result = list(dbCursor.fetchall())
    #     tableNameList = [i[0] for i in result]
    #     self.databaseUi.tableNamecomboBox.addItems(tableNameList)

    def __updateDatabaseNameComboBox(self, databaseName : list) :
        self.databaseUi.tableNamecomboBox.setCurrentIndex(0)
        self.databaseUi.tableNamecomboBox.clear()
        self.databaseUi.databaseNamecomboBox.clear()
        self.databaseUi.databaseNamecomboBox.setCurrentIndex(0)      
        self.databaseUi.databaseNamecomboBox.addItems(databaseName)

    def __updateTableNameComboBox(self, tableName : list) :
        self.databaseUi.tableNamecomboBox.setCurrentIndex(0)
        self.databaseUi.tableNamecomboBox.clear()
        self.databaseUi.tableNamecomboBox.addItems(tableName)
    
    def getDatabaseNameList(self, connection : mysql.connector.connection_cext.CMySQLConnection) :
        # updateDatabaseName = UpdateDatabaseName()
        self.updateDatabaseName.setDatabaseConnection(connection)
        self.updateDatabaseName.setQuery("SHOW DATABASES")
        self.updateDatabaseName.dataList.connect(self.__updateDatabaseNameComboBox)
        self.updateDatabaseName.start()
    
    def getTableNameList(self, connection : mysql.connector.connection_cext.CMySQLConnection) :
        # updateTableName = UpdateDatabaseName()
        self.updateTableName.setDatabaseConnection(connection)
        self.updateTableName.setQuery("SHOW TABLES")
        self.updateTableName.dataList.connect(self.__updateTableNameComboBox)
        self.updateTableName.start()

    # def __updateDatabaseNameComboBox(self, connection : mysql.connector.connection_cext.CMySQLConnection) :
    #     if(connection is None) :
    #         return
    #     self.databaseUi.tableNamecomboBox.setCurrentIndex(0)
    #     self.databaseUi.tableNamecomboBox.clear()
        
    #     dbCursor = connection.cursor()
    #     dbCursor.execute("SHOW DATABASES")
    #     result = list(dbCursor.fetchall())
    #     databaseNameList = [i[0] for i in result]  
    #     self.databaseUi.databaseNamecomboBox.clear()
    #     self.databaseUi.databaseNamecomboBox.setCurrentIndex(0)      
    #     self.databaseUi.databaseNamecomboBox.addItems(databaseNameList)