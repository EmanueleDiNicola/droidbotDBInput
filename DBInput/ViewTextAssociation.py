from DBInput.database.DatabaseStructureFactory import DatabaseStructureFactory
from DBInput.query.CachedMicrosoftSqlQueryEngine import CachedMicrosoftSqlQueryEngine
from DBInput.query.SqlDatabaseInfo import SqlDatabaseInfo
from DBInput.relations.relationsmaker.DefaultRelationsMaker import DefaultRelationsMaker
from DBInput.webapp.Field import Field
from DBInput.webapp.Label import Label
from DBInput.webapp.Page import Page
import numpy as np

from input_event import SetTextEvent


class ViewTextAssociation:
    def __init__(self, events):
        self.sql_database_info = SqlDatabaseInfo()
        self.cached_sql_query_engine = CachedMicrosoftSqlQueryEngine(self.sql_database_info)
        self.database_struct_fact = DatabaseStructureFactory(self.cached_sql_query_engine)
        self.database_struct = self.database_struct_fact.GetDatabaseStructure()
        self.views = dict()
        self.events = list()
        for event in events:
            self.views[event.view['temp_id']] = event.view
        self.page = None

        self.views_resource = list()

        self.views_key_value = dict()

        self.CreatePage()

    def CreatePage(self):
        url = "www.com"
        field_list = list()
        activity = ""
        for key in self.views:
            label_list = list()
            id = self.ExtrapolateId(self.views[key]["resource_id"])
            # Non è un url, modificare
            url = self.views[key]["package"]
            activity = self.views[key]["activity"]
            label_list.append(self.CreateLabel(id))
            if "associate_text_view" in self.views[key]:
                for text_view in self.views[key]["associate_text_view"]:
                    text = text_view["text"]
                    """
                    if text_view["resource_id"] is not None:
                        text_view_resource_id = self.ExtrapolateId(text_view["resource_id"])
                        label_list.append(self.CreateLabel(text_view_resource_id))
                    """
                    if text is not None:
                        label_list.append(self.CreateLabel(text))
            field_list.append(self.CreateField(label_list))
        self.page = self.CreatePageFromFields(field_list, url, activity)
        relations_maker = DefaultRelationsMaker("Test")
        relations_results = relations_maker.FindBestMatch(self.page, self.database_struct)
        self.AssociateViewText(relations_results)

    def CreateLabel(self, view_id):
        return Label(view_id)

    def CreateField(self, labels):
        return Field(labels)

    def CreatePageFromFields(self, fields, url, activity):
        return Page(fields, url, activity)

    def AssociateViewText(self, relations_results):
        max_rows = 1000000000
        for key, element in relations_results.field_column_relations.items():
            actual_count = element.column.Count()
            if actual_count < max_rows:
                max_rows = actual_count
        if max_rows != 1:
            number = np.random.randint(0, max_rows - 1)
        else:
            number = 1
        for relation in relations_results.GetRelations():
            resource_id = relation.field.labels[0].value
            print(relation.field.ToString())
            print(relation.column.ToString())
            text = relations_results.GetData(relation.field, number)
            if text == " ":
                text = "Value Null in the column " + str(number)
            self.views_key_value[resource_id] = text

    def ExtrapolateId(self, string):
        sep = "id/"
        resource_id = string.split(sep, 1)[1]
        return resource_id

    def GetSetTextEvents(self):
        for view in self.views:
            view_resource_id = self.ExtrapolateId(self.views[view]["resource_id"])
            view_temp_id = view
            text = self.views_key_value[view_resource_id]
            self.events.append(SetTextEvent(view=self.views[view_temp_id], text=text))
        return self.events
