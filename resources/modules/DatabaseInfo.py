import mysql.connector

class DatabaseInfo() :
    def __init__(self, connection : mysql.connector.connection_cext.CMySQLConnection = None, tableName : str = None) -> None:
        self.connection = connection
        self.tableName = tableName