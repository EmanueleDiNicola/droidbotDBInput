from typing import Any

from DBInput.DBIExceptions import ArgumentNullException, ArgumentOutOfRangeException


class TablePageRelation:
    def __init__(self, table, page):
        if table is None:
            raise ArgumentNullException("Table")
        if page is None:
            raise ArgumentNullException("Page")
        self.min_quality = 0
        self.table = table
        self.page = page
        self.relations = list()

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def Relations(self):
        return self.GetFilteredRelations()

    def GetFilteredRelations(self):
        filtered_relations = list()
        for field_column_relation in self.relations:
            if field_column_relation.value >= self.min_quality:
                filtered_relations.append(field_column_relation)
        return filtered_relations

    def GetMinQualirty(self):
        return self.min_quality

    def SetMinQuality(self, value):
        if value < 0 or value > 1:
            raise ArgumentOutOfRangeException("Min quality must be in the range [0;1]")
        self.min_quality = value

    def AddRelation(self, field_column_relation):
        self.relations.append(field_column_relation)

    def ToString(self):
        return self.table.ToString() + " -> " + self.page.tostring()

    def Equals(self, obj):
        if obj is None or not isinstance(obj, TablePageRelation):
            return False
        return self.page.equals(obj.page) and self.table.__eq__(obj.table)

    def __hash__(self) -> int:
        return super().__hash__()

