from typing import Any

from DBInput.DBIExceptions import ArgumentNullException


class Label:
    def __init__(self, value):
        if value is None:
            raise ArgumentNullException("Value")
        self.value = value

    def equals(self, obj):
        if isinstance(obj, Label) and obj.__getattribute__("value") == self.value:
            return True
        return False

    def __hash__(self) -> int:
        return super().__hash__()

    def get_hash_code(self):
        return -1937169414 + hash(self.value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def tostring(self):
        return "Label - value: " + str(self.__getattribute__("value"))

#exec(open("DBInput\webapp\Label.py").read())