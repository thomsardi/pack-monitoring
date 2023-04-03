import PyQt5.QtCore as qtc
import time
from resources.modules.BatteryData import BatteryData
from resources.modules.DatabaseInfo import DatabaseInfo

class ReadDatabase(qtc.QThread, qtc.QObject) :
    isDone = qtc.pyqtSignal(BatteryData)
    def __init__(self) -> None:
        qtc.QThread.__init__(self)
        qtc.QObject.__init__(self)
        self.connection = None
        self.tableName = None
        self.daemon = True
        self.isRun = False
        self.batteryData = None

    def setDatabaseInfo(self, databaseInfo : DatabaseInfo) :
        self.connection = databaseInfo.connection
        self.tableName = databaseInfo.tableName

    def run(self) :
        dbCursor = self.connection.cursor()
        query = "SELECT * FROM `%s` ORDER BY ID DESC LIMIT 1" % (self.tableName)
        print(query)
        while (self.isRun) :
            dbCursor.execute(query)
            result = dbCursor.fetchall()
            vcell = []
            temp = []
            vpack = []
            for x in range(9, 54) :
                data = [i[x] for i in result]
                vcell.append(data[0])
            for x in range(54, 63) :
                data = [i[x] for i in result]
                temp.append(data[0])
            for x in range(63, 66) :
                data = [i[x] for i in result]
                vpack.append(data[0])
            self.batteryData = BatteryData(vcell, temp, vpack)
            self.isDone.emit(self.batteryData)  
            # print(vcell)
            time.sleep(0.1)        
