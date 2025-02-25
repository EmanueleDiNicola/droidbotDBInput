from typing import Any

from DBInput.DBIExceptions import ArgumentNullException


class Label:
    def __init__(self, value):
        if value is None:
            raise ArgumentNullException("Label: Value is None")
        self.value = value

    def Equals(self, obj):
        if isinstance(obj, Label) and obj.__getattribute__("value") == self.value:
            return True
        return False

    def __hash__(self) -> int:
        return super().__hash__()

    def GetHashCode(self):
        return -1937169414 + hash(self.value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def ToString(self):
        return "Label - value: " + str(self.__getattribute__("value"))

