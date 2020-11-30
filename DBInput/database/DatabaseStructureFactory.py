from DBInput.database.DatabaseStructure import DatabaseStructure
from DBInput.database.Table import Table


class DatabaseStructureFactory:

    def __init__(self, query_engine):
        self.query_engine = query_engine
        self.MAX_NUMBER_OF_ROWS = 1000

    def GetDatabaseStructure(self):
        database_struct = DatabaseStructure()
        table_names = self.query_engine.GetTableNames()
        for table_name in table_names:
            table = self.CreateTable(table_name)
            database_struct.AddTable(table)
        return database_struct

    def CreateTable(self, table_name):
        column_names = self.query_engine.GetTableColumnNames(table_name)
        table = Table(table_name, column_names)
        rows = self.query_engine.GetRows(table_name, self.MAX_NUMBER_OF_ROWS)
        table.AddRows(rows)
        return table

