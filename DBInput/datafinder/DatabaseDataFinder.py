from DBInput.datafinder.IDataFinder import IDataFinder
import numpy as np


class DatabaseDataFinder(IDataFinder):
    def __init__(self, database, relations_maker):
        super().__init__()
        self.r = np.random.randint(1000000000000)
        self.database = database
        self.relations_maker = relations_maker
        self.known_relations = dict()

    def GetRelatedData(self, page):
        relation = self.GetRelation(page)
        data_for_fields = dict()
        self.r = np.random.randint(1000000000000)
        for field in page.get_fields():
            data = relation.GetData(field, self.r)
            data_for_fields[field] = data
        return data_for_fields

    def GetRelation(self, page):
        print("Finding widgets-DB columns matches...")
        if not page.get_hash_code() in self.known_relations:
            relation = self.relations_maker.FindBestMatch(page, self.database)
            self.known_relations[page.get_hash_code()] = relation
        else:
            relation = self.known_relations[page.get_hash_code()]
        self.PrintBestMatches(relation.GetRelations(), relation.GetTotalQuality())
        return relation

    def PrintBestMatches(self, best_matches, total_quality):
        print("Best matches forund:")
        tables = list()
        column = list()
        for r in best_matches:
            tables.append(r.column.tableName)
            column.append(r.column.tableName + "." + r.column.name)
            print("For field " + r.field.tostring() + " and column " + r.column.tableName + "." + r.column.name
                  + "the match is " + r.value)

    def GetUnrelatedData(self, page):
        relation = GetRelation(page)
        data_for_fields = dict()
        for field in page.get_fields():
            self.r = np.random.randint(1000000000000)
            data = relation.GetData(field, self.r)
            data_for_fields[field] = data
        return data_for_fields
