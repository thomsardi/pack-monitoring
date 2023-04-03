import PyQt5.QtCore as qtc
import mysql.connector
from mysql.connector import Error
from resources.modules.BatteryData import BatteryData
from resources.modules.DatabaseInfo import DatabaseInfo

class UpdateDatabaseName(qtc.QThread, qtc.QObject) :
    dataList = qtc.pyqtSignal(list)
    def __init__(self) -> None:
        qtc.QThread.__init__(self)
        qtc.QObject.__init__(self)
        self.connection = None
        self.tableName = None
        self.daemon = True
        self.isRun = False
        self.batteryData = None
        self.query = None

    def setDatabaseConnection(self, connection : mysql.connector.connection_cext.CMySQLConnection) :
        self.connection = connection

    def setQuery(self, query : str) :
        self.query = query

    def run(self) :
        dbCursor = self.connection.cursor()
        query = self.query
        try :
            print(query)
            dbCursor.execute(query)
            result = dbCursor.fetchall()
            dataList = [i[0] for i in result]
            self.dataList.emit(dataList)
        except : 
            print("Query Failed")
        
        
             
