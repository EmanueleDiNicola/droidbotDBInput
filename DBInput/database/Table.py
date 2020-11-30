from DBInput.DBIExceptions import ArgumentNullException, ArgumentException
from DBInput.database.Column import *
from past.types import basestring


class Table:
    def __init__(self, name, columns):
        if name is None:
            raise ArgumentNullException("Table name can not be null")
        self.name = name
        if columns is None:
            raise ArgumentNullException("columns can not be null")
        column_c = False
        column_names = False
        for column in columns:
            if isinstance(column, Column):
                column_c = True
            if isinstance(column, basestring):
                column_names = True
        if column_names and column_c:
            raise ArgumentException("Table columns parameter is invalid")
        if column_names:
            self.columns = self.CreateColumns(columns)
        if column_c:
            if not self.ColumnsAreValid(columns):
                raise ArgumentException("Columns can not be null or have different sizes")
            self.columns = self.Clone(columns)

    def CreateColumns(self, columns_names):
        new_columns = list()
        for name in columns_names:
            new_column = Column(name, self.name)
            new_columns.append(new_column)
        return new_columns

    def Clone(self, columns):
        cloned = list()
        for column in columns:
            cloned.append(column.Clone(self.name))
        return cloned

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def AddRow(self, row):
        self.RowIsValid(row)
        self.AddRowValuesToColumn(row)

    def RowIsValid(self, row):
        if row is None:
            raise ArgumentNullException("Row can not be null")
        if len(row) != len(self.columns):
            raise ArgumentException("Row length doesn't match table length")

    def AddRowValuesToColumn(self, row):
        for i in range(len(self.columns)):
            self.columns[i].Add(row[i])

    def AddRows(self, rows):
        if rows is None:
            raise ArgumentNullException("Rows can not be NULL")
        for row in rows:
            self.RowIsValid(row)
        for row in rows:
            self.AddRowValuesToColumn(row)

    def ObjectInvariantMethod(self):
        if self.columns is None:
            return False
        if not self.ColumnsAreValid(self.columns):
            return False
        return True

    def ColumnsAreValid(self, columns):
        size = -1
        if len(columns) == 0:
            return False
        for column in columns:
            if column is None:
                return False
            if size == -1:
                size = column.Count()
            else:
                if size != column.Count():
                    return False
        return True

    def Equals(self, obj):
        if isinstance(obj, Table):
            if self.name == obj.name:
                return self.SameColumns(self.columns, obj.columns)
        return False

    def SameColumns(self, columns1, columns2):
        if len(columns1) != len(columns2):
            return False
        for i in range(len(columns1)):
            if not columns1[i].Equals(columns2[i]):
                return False
        return True

    def GetHashCode(self):
        hash_code = -1604460014
        hash_code += 17 * hash_code + self.name.__hash__()
        hash_code += 17 * hash_code + len(self.columns)
        return hash_code

    def ToString(self):
        output = self.name + " has " + str(len(self.columns)) + " columns:"
        for column in self.columns:
            output = output + "\n" + column.ToString()
        return output
