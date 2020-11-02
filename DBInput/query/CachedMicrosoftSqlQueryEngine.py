from DBInput.DBIExceptions import SqlException
from DBInput.query.IQueryEngine import IQueryEngine
import numpy as np
import logging
import pyodbc


class CachedMicrosoftSqlQueryEngine(IQueryEngine):
    GET_TABLES_NAMES_QUERY = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"
    MAX_NUMBER_OF_ROWS = 10000

    def __init__(self, sql_database_info):
        self.table_names = list()
        self.table_column_names = dict()
        self.table_rows = dict()
        self.logger = logging.getLoggerClass()
        self.load(sql_database_info)

    def CreateSqlConnection(self, sql_database_info):
        connection = pyodbc.connect(
            "Driver=" + sql_database_info.__getattribute__("driver") + ";"
            "Server=" + sql_database_info.__getattribute__("server") + ";"
            "Database=" + sql_database_info.__getattribute__("database") + ";"
            "UID=" + sql_database_info.__getattribute__("uid") + ";"
            "PWD=" + sql_database_info.__getattribute__("pwd") + ";"
            "Mars_connection=yes;"
            "Trusted_Connection=yes"
        )
        return connection

    def load(self, sql_database_info):
        self.logger = logging.getLogger("Sql Database")
        self.logger.setLevel("DEBUG")
        try:
            self.logger.info("Connecting to SQL Microsoft database")
            connection = self.CreateSqlConnection(sql_database_info)
            self.logger.info("Loading data from database")
            self.LoadTableNames(connection)
            for table_name in self.table_names:
                self.LoadTableColumnNames(connection, table_name)
                self.LoadTableRows(connection, table_name)
            self.RemoveEmptyTables()
            self.logger.info("Data has been loaded")
        except:
            raise SqlException("Error in connecting to database.")

    def LoadTableNames(self, connection):
        cursor = connection.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables")
        fetch_output = cursor.fetchall()
        if fetch_output is None:
            raise SqlException("Table names are Null")
        for table in fetch_output:
            self.table_names.append(table[0])

    def LoadTableColumnNames(self, connection, table_name):
        cursor = connection.cursor()
        query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS  WHERE TABLE_NAME = '" + table_name + "'"
        cursor.execute(query)
        column_output = cursor.fetchall()
        if column_output is None:
            raise SqlException("Column names of table" + table_name + "are Null")
        column_output_2 = list()
        for column in column_output:
            column_output_2.append(column[0])
        self.table_column_names[table_name] = column_output_2

    def LoadTableRows(self, connection, table_name):
        try:
            cursor = connection.cursor()
            for column_name in self.table_column_names[table_name]:
                query = "SELECT * FROM " + table_name
                cursor.execute(query)
                rows_output = cursor.fetchall()
                row_output2 = list()
                for row in rows_output:
                    row_output2.append(row)
                self.table_rows[table_name] = row_output2
        except:
            raise SqlException("Error in reading atabase rows")

    def RemoveEmptyTables(self):
        not_empty_tables = list()
        for table_name in self.table_names:
            if len(self.table_column_names[table_name])>0 and len(self.table_rows[table_name])>0:
                not_empty_tables.append(table_name)
            else:
                self.table_column_names.pop(table_name)
                self.table_rows.pop(table_name)
        self.table_names = not_empty_tables

    def GetRow(self, columns):
        #Non ho capito cosa deve fare sto metodo.
        pass

    def GetRows(self, table_name, max_number_of_rows):
        number_of_rows = min(max_number_of_rows, len(self.table_rows[table_name]))
        i = 0
        output = list()
        for row in self.table_rows[table_name]:
            output.append(self.table_rows[table_name][i])
            i = i + 1
            if i == number_of_rows:
                break
        print(output)

    def GetTableColumnNames(self, table_name):
        return self.table_column_names[table_name]

    def GetTableNames(self):
        return self.table_names


