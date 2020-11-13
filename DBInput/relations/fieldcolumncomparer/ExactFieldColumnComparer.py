from DBInput.DBIExceptions import ArgumentNullException, NotImplementedException
from DBInput.relations.fieldcolumncomparer.IFieldColumnComparer import IFieldColumnComparer


class ExactFieldColumnComparer(IFieldColumnComparer):
    def __init__(self):
        pass

    def Compare(self, field, column):
        if field is None:
            raise ArgumentNullException("Field")
        if column is None:
            raise ArgumentNullException("Column")
        for label in field.labels:
            if label.value == column.name:
                return 1
        return 0

    def GetComparer(self):
        raise NotImplementedException()
