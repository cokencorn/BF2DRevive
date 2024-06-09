import mysql.connector
from mysql.connector import errorcode
from Database.DBConfig import DBConfig


class DatabaseDriver(object):
    connection_string = None
    connection = None
    DB_NAME = DBConfig.DATABASE_NAME

    def __init__(self, connection_string):
        self.connect(connection_string)

    def connect(self, connection_string):
        self.connection_string = connection_string
        self.connection = mysql.connector.connect(**connection_string)

        # Create database if not exists
        try:
            self.connection.database = self.DB_NAME
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database()
                self.connection.database = self.DB_NAME

    def query(self, sql, params):
        try:
            cursor = self.connection.cursor(dictionary=True, buffered=True)
            cursor.execute(sql, params)
            self.connection.commit()
        except mysql.connector.Error as err:
            self.connect(self.connection_string)
            cursor = self.connection.cursor(dictionary=True, buffered=True)
            cursor.execute(sql, params)
            self.connection.commit()
        return cursor

    def create_database(self):
        try:
            cursor = self.connection.cursor(buffered=True)
            cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.DB_NAME))
            cursor.close()
        except mysql.connector.Error as err:
            print("DB Error: Failed create database: {}".format(self.DB_NAME))

    def execute(self, sql):
        try:
            cursor = self.connection.cursor()
            return cursor.execute(sql)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("DB Info: " + str(err.msg))
            else:
                print("DB Error: " + str(err.message))
