from typing import Any

from DBInput.DBIExceptions import ArgumentNullException, ArgumentException


def ValuesAreValid(values):
    if values is None:
        raise ArgumentNullException("Row.ValuesAreValid, values: Values can not be null")
    for value in values:
        if value is None:
            raise ArgumentException("Row.ValuesAreValid: No element inside the array can be null: values")
    return True


class Row:
    def __init__(self, values):
        if ValuesAreValid(values):
            self.values = values

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def __hash__(self) -> int:
        return super().__hash__()

    def Length(self):
        return len(self.values)

    def Equals(self, obj):
        if obj is None:
            return False
        if isinstance(obj, Row):
            if obj.Length() != self.Length():
                return False
            for i in range(len(self.values)):
                if self.values[i] != obj.values[i]:
                    return False
            return True
        return False

    def ToString(self):
        output = "Row:"
        for v in self.values:
            output = output + " - " + str(v)
        return output
