from DBInput.database.DatabaseStructureFactory import DatabaseStructureFactory
from DBInput.query.CachedMicrosoftSqlQueryEngine import CachedMicrosoftSqlQueryEngine
from DBInput.query.SqlDatabaseInfo import SqlDatabaseInfo
from DBInput.relations.relationsmaker.DefaultRelationsMaker import DefaultRelationsMaker
from DBInput.webapp.Field import Field
from DBInput.webapp.Label import Label
from DBInput.webapp.Page import Page
import numpy as np


class ViewTextAssociation:
    def __init__(self, views, activity):
        self.sql_database_info = SqlDatabaseInfo()
        self.cached_sql_query_engine = CachedMicrosoftSqlQueryEngine(self.sql_database_info)
        self.database_struct_fact = DatabaseStructureFactory(self.cached_sql_query_engine)
        self.database_struct = self.database_struct_fact.GetDatabaseStructure()
        self.views = views
        self.page = None
        self.number_tried = list()
        self.views_id_key = dict()
        self.views_key_value = dict()
        self.CreatePage(activity)

    def CreatePage(self, activity):
        label_list = list()
        url = "www.com"
        for key in self.views:
            id = self.ExtrapolateId(self.views[key])
            # Non è un url, modificare
            url = self.views[key]["package"]
            label_list.append(self.CreateLabel(id))
            self.views_id_key[id] = key
        field_list = list()
        for label in label_list:
            field_list.append(self.CreateField([label]))
        self.page = self.CreatePageFromFields(field_list, url, activity)
        relations_maker = DefaultRelationsMaker("MAXSIMILARITY_MAXLABELS_OLD")
        relations_results = relations_maker.FindBestMatch(self.page, self.database_struct)
        self.AssociateViewText(relations_results)

    def CreateLabel(self, view_id):
        return Label(view_id)

    def CreateField(self, labels):
        return Field(labels)

    def CreatePageFromFields(self, fields, url, activity):
        return Page(fields, url, activity)

    def AssociateViewText(self, relations_results):
        number_already_chosen = True
        number = 0
        max_rows = 1000000000
        for key, element in relations_results.field_column_relations.items():
            actual_count = element.column.Count()
            if actual_count < max_rows:
                max_rows = actual_count
        for relation in relations_results.GetRelations():
            while number_already_chosen:
                number = np.random.randint(0, max_rows)
                if number not in self.number_tried or len(self.number_tried) == max_rows:
                    number_already_chosen = False
                    if len(self.number_tried) == max_rows:
                        self.number_tried = self.number_tried.clear()
                        number = np.random.randint(0, max_rows)
            self.number_tried.append(number)
            id = relation.field.labels[0].value
            key = self.views_id_key[id]
            self.views_key_value[key] = relations_results.GetData(relation.field, number)

    def ExtrapolateId(self, view):
        string = view["resource_id"]
        sep = "id/"
        id = string.split(sep, 1)[1]
        return id

    def GetViewIdKey(self):
        return self.views_id_key

    def GetViewKeyValue(self):
        return self.views_key_value
