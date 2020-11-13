from DBInput.DBIExceptions import ArgumentNullException
from DBInput.relations.fieldcolumncomparer.IFieldColumnComparer import IFieldColumnComparer


class MaxQualityComparer(IFieldColumnComparer):
    def __init__(self, string_comparer):
        self.string_comparer = string_comparer

    def Compare(self, field, column):
        if field is None:
            raise ArgumentNullException("Field")
        if column is None:
            raise ArgumentNullException("Column")
        max = 0
        for label in field.labels:
            quality = self.string_comparer.StringSimilarity(label.value, column.name)
            if quality > max:
                max = quality
        return max

    def GetComparer(self):
        return self.string_comparer
