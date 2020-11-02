from DBInput.DBIExceptions import ArgumentException


class DatabaseStructure:
    def __init__(self):
        self.tables = dict()

    def AddTable(self, table):
        self.tables[table.name] = table

    def GetTable(self, table_name):
        if table_name not in self.tables:
            raise ArgumentException("Table not present")
        return self.tables[table_name]

    def Equals(self, obj):
        if obj is None:
            return False
        if obj.tables is None:
            return False
        if isinstance(obj, DatabaseStructure):
            return obj.tables == self.tables

    def GetHashCode(self):
        return 1212389988 + self.tables.__hash__()

    def Count(self):
        return len(self.tables)

#exec(open("DBInput\database\DatabaseStructure.py").read())
