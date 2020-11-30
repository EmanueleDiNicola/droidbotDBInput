from DBInput.relations.fieldcolumncomparer.stringcomparer.IStringComparer import IStringComparer


class MeanComposedStringComparer(IStringComparer):
    def __init__(self):
        self.string_comparers = list()

    def GetStringComparers(self):
        new_list = self.string_comparers
        return new_list

    def AddComparer(self, comparer):
        self.string_comparers.append(comparer)

    def StringSimilarity(self, s1, s2):
        mean = 0
        for comparer in self.string_comparers:
            similarity = comparer.StringSimilarity(s1, s2)
            mean = mean + similarity
        return mean / len(self.string_comparers)

    def GetComparers(self):
        return self.string_comparers