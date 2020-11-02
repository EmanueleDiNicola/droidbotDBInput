from typing import Any

from DBInput.DBIExceptions import *
from DBInput.webapp.Label import Label


class Field:
    def __init__(self, labels):
        if labels is None or len(labels) > 1 and None in labels:
            raise ArgumentNullException("labels")
        if len(labels) is 0:
            print(len(labels))
            raise ArgumentException("Labels can not be empty")
        if len(labels) > 1:
            for label in labels:
                if not isinstance(label, Label):
                    raise ArgumentException("Not a list of Only Labels")
        self.labels = labels

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def equals(self, obj):
        if not isinstance(obj, Field) or obj is None:
            return False
        other_field = obj
        if len(self.labels) != len(other_field.__getattribute__("labels")):
            return False
        find = False
        for label1 in self.labels:
            for label2 in obj.labels:
                if label1.equals(label2):
                    find = True
                    break
            if not find:
                return False
            else:
                find = False
        return True

    def same(self, field):
        num_labels = len(self.labels)
        num_other_labels = len(field.labels)
        if num_labels != num_other_labels:
            return False
        for i in range(len(self.labels)):
            if self.labels[i].equals(field.labels[i]):
                pass
            else:
                return False
        return True

    def get_hash_code(self):
        hash_code = -1802429414
        for label in self.labels:
            hash_code = hash_code + label.get_hash_code()
        return hash_code

    # Dovrebbe essere toString, speriamo?
    def tostring(self):
        stingers = "Field: [ "
        for label in self.labels:
            stingers = stingers + "(" + label.tostring() + "), "
        return stingers + "]"

# exec(open("DBInput\webapp\Field.py").read())
