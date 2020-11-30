from DBInput.datafinder.IDataFinder import IDataFinder


class RandomValuesDtaFinder(IDataFinder):
    def __init__(self):
        super().__init__()
        self.n = 0

    def GetRelatedData(self, page):
        data_for_fields = dict()
        for field in page.GetFields():
            data_for_fields[field] = self.GetRndomValue()
        return data_for_fields

    def GetRandomValue(self):
        n = n + 1
        return "string " + str(n)

    def GetUnrelatedData(self, page):
        return self.GetRelatedData(page)
