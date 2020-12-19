from typing import Any

from DBInput.DBIExceptions import ArgumentNullException, ArgumentException


class Column:
    def __init__(self, name, table_name):
        if table_name is None:
            raise ArgumentNullException("Column.init: tablename can not be null")
        if name is None:
            raise ArgumentNullException("Column.init: name can not be null")
        self.table_name = table_name
        self.name = name
        self.values = list()

    def Count(self):
        return len(self.values)

    def Get(self, key):
        return self.values[key]

    def Add(self, value):
        if value is None:
            #raise ArgumentNullException("Column.Add: value can not be null")
            self.values.append(None)
        else:
            self.values.append(value)

    def Clone(self, tableName):
        clone = Column(self.name, tableName)
        for value in self.values:
            clone.Add(value)
        return clone

    #Not used
    def ValuesNotNull(self):
        if self.values is None:
            return False
        for value in self.values:
            if value is None:
                return False
        return True

    #Not Used
    def ObjectInvariantMethod(self):
        if self.name is None:
            return False
        if self.table_name is None:
            return False
        if not self.ValuesNotNull():
            return False
        return True

    def Equals(self, obj):
        if obj is None:
            return False
        if isinstance(obj, Column):
            if obj.Count() != self.Count():
                return False
            if obj.name == self.name and obj.table_name == self.table_name:
                for i in range(len(self.values)):
                    if self.values[i] != obj.values[i]:
                        return False
            else:
                return False
        return True

    def __hash__(self) -> int:
        hashcode = super().__hash__()
        hashcode = hashcode * -1521134295 + self.name.__hash__()
        hashcode = hashcode * -1521134295 * self.values.__hash__()
        return hashcode

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def ToString(self):
        output = "Table = " + self.table_name + " - " + self.name + " "
        for value in self.values:
            output = output + " - " + str(value)
        return output
