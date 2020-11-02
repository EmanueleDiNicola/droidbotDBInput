from typing import Any

from DBInput.DBIExceptions import ArgumentNullException, ArgumentException


class Column:
    def __init__(self, name, tableName):
        if tableName is None:
            raise ArgumentNullException("tablename can not be null")
        if name is None:
            raise ArgumentNullException("name can not be null")
        self.tableName = tableName
        self.name = name
        self.values = list()

    def Count(self):
        return len(self.values)

    def Get(self, key):
        return self.values[key]

    def Add(self, value):
        if value is None:
            raise ArgumentNullException("value", "value can not be null")
        else:
            self.values.append(value)

    def Clone(self, tableName):
        clone = Column(self.name, tableName)
        for value in self.values:
            clone.Add(value)
        return clone

    def ValuesNotNull(self):
        if self.values is None:
            return False
        for value in self.values:
            if value is None:
                return False
        return True

    def ObjectInvariantMethod(self):
        if self.name is None:
            return False
        if self.tableName is None:
            return False
        if not self.ValuesNotNull():
            return False
        return True

    def equals(self, obj):
        if obj is None:
            return False
        if isinstance(obj, Column):
            if obj.Count() != self.Count():
                return False
            if obj.name == self.name and obj.tableName == self.tableName:
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

    def toString(self):
        return self.name + " " + self.tableName

#exec(open("DBInput\database\Column.py").read())
