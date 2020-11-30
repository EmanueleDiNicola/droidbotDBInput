from DBInput.webapp.Field import *
from DBInput.webapp.Label import *
from typing import Any


class FieldColumnRelation:
    def __init__(self, field, column, value):
        if field is None:
            raise ArgumentNullException("Field")
        if column is None:
            raise ArgumentNullException("Column")
        if value is None or value < 0 or value > 1:
            raise ArgumentOutOfRangeException("Quality must be in the range [0;1]")
        self.field = field
        self.column = column
        self.value = value

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def Equals(self, obj):
        return isinstance(obj, FieldColumnRelation) and self.field.Equals(obj.field) and self.column.Equals(obj.column)

    def __hash__(self) -> int:
        return super().__hash__()

    def ToString(self):
        return "Q: " + str(self.value) + " " + self.field.ToString() + " " + self.column.ToString()
