from DBInput.DBIExceptions import NotImplementedException
from DBInput.datafinder.IDataFinder import IDataFinder
import os
import numpy as np

class LinkDataFinder(IDataFinder):
    process_time_out_ms = 60000

    def __init__(self, link_jar_path):
        super().__init__()
        self.label_dictionary = dict()
        self.link_jar_path = link_jar_path
        wd = os.getcwd()
        self.json_file_path = wd + "\\output.json"
        self.n = 0

    def GetRelatedData(self, page):
        data_for_fields = dict()
        for field in page.get_fields():
            if lent(field.labels) == 3:
                label = field.labels[2]
                data_for_fields[field] = self.GetValueForABTLabel(label.value.lower())
            else:
                data_for_fields[field] = self.GetRandomValue()
        return data_for_fields

    def GetValueForABTLabel(self, abt_label):
        abt_plan_label = self.RemoveSpecialCharacters(abt_label)
        if abt_plan_label not in self.label_dictionary:
            self.UpdateLabelsWithLink(abt_plan_label)
        if abt_plan_label in self.label_dictionary and self.label_dictionary[abt_plan_label] is not None:
            values = self.label_dictionary[abt_plan_label]
            i = np.random.randint(0, len(values))
            return values[i]
        return self.GetRandomValue()

    def GetRandomValue(self):
        n = n + 1
        return "string " + str(n)

    def RemoveSpecialCharacters(self, s):
        new_s = ""
        for c in s:
            if c.isalpha() or c.isspace()
                new_s = new_s + c
        return new_s

    def UpdateLabelsWithLink(self, abt_plan_label):
        self.ExecuteLinkQuery(abt_plan_label)
        link_labels = self.LoadNewLabels()
        self.label_dictionary[abt_plan_label] = link_labels

    def ExecuteLinkQuery(self, abt_plan_label):
        #fa roba con processo
        return None

    def LoadNewLabels(self):
        #legge da Json
        return None

    def GetUnrelatedData(self, page):
        raise NotImplementedException()
