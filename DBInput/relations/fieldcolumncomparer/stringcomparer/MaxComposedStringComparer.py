from DBInput.relations.fieldcolumncomparer.stringcomparer.IStringComparer import IStringComparer


class MaxComposedStringComparer(IStringComparer):
    def __init__(self):
        self.string_comparers = list()

    def GetStringComparers(self):
        list2 = self.string_comparers
        return list2

    def AddComparer(self, comparer):
        self.string_comparers.append(comparer)

    def StringSimilarity(self, s1, s2):
        max = 0
        for comparer in self.string_comparers:
            similarity = comparer.StringSimiliarity(s1, s2)
            if similarity > max:
                max = similarity
        return max

    def GetComparers(self):
        return self.string_comparers