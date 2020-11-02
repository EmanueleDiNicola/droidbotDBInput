from DBInput.DBIExceptions import ArgumentNullException


class PageDatabaseRelation:
    # Prende page ma non la usa (?)
    def __init__(self, page, field_column_relations, quality):
        if field_column_relations is None:
            raise ArgumentNullException("fieldColumnRelations is Null")
        self.field_column_relations = dict()
        for rel in field_column_relations:
            self.field_column_relations[rel.field] = rel
        self.total_quality = quality

    def GetRelations(self):
        all_relations = list()
        for key in self.field_column_relations.keys():
            value = self.field_column_relations.get(key)
            all_relations.append(value)
        return all_relations

    def GetTotalQuality(self):
        return self.total_quality

    def GetData(self, field, row_number):
        column = self.field_column_relations[field].column
        data = column.Get(row_number % (column.Count()))
        return data

#exec(open("DBInput\\relations\PageDatabaseRelation.py").read())