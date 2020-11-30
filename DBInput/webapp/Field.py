from typing import Any

from DBInput.DBIExceptions import *
from DBInput.webapp.Label import Label


class Field:
    def __init__(self, labels):
        if labels is None or len(labels) > 1 and None in labels:
            raise ArgumentNullException("Field: labels is None or One of labels is None")
        if len(labels) is 0:
            raise ArgumentException("Field: Labels can not be empty")
        if len(labels) > 1:
            for label in labels:
                if not isinstance(label, Label):
                    raise ArgumentException("Field: Not a list of Only Labels")
        self.labels = labels

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def Equals(self, obj):
        if not isinstance(obj, Field) or obj is None:
            return False
        other_field = obj
        if len(self.labels) != len(other_field.__getattribute__("labels")):
            return False
        find = False
        for label1 in self.labels:
            for label2 in obj.labels:
                if label1.Equals(label2):
                    find = True
                    break
            if not find:
                return False
            else:
                find = False
        return True

    def Same(self, field):
        num_labels = len(self.labels)
        num_other_labels = len(field.labels)
        if num_labels != num_other_labels:
            return False
        for i in range(len(self.labels)):
            if self.labels[i].Equals(field.labels[i]):
                pass
            else:
                return False
        return True

    def GetHashCode(self):
        hash_code = -1802429414
        for label in self.labels:
            hash_code = hash_code + label.GetHashCode()
        return hash_code

    def ToString(self):
        string = "Field: [ "
        for label in self.labels:
            string = string + "(" + label.ToString() + "), "
        return string + "]"
