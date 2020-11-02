from DBInput.DBIExceptions import NotImplementedException
from DBInput.relations.fieldcolumncomparer.StringTransformation import CleanString
from DBInput.relations.fieldcolumncomparer.stringcomparer.IStringComparer import IStringComparer
import numpy as np


class DamerauLevenshteinStringComparer(IStringComparer):

    def __init__(self):
        pass

    def StringSimilarity(self, s1, s2):
        cleans1 = CleanString(s1)
        cleans2 = CleanString(s2)
        max_distance = max(len(cleans1), len(cleans2))
        if max_distance == 0:
            return 0
        distance = self.GetDamerauLevenshteinDistance(cleans1, cleans2)
        return (max_distance - distance) / max_distance

    def GetDamerauLevenshteinDistance(self, s, t):
        height = len(s) + 1
        width = len(t) + 1
        matrix = np.zeros((height, width))
        for i in range(height):
            matrix[i, 0] = i
        for i in range(width):
            matrix[0, i] = i
        i = 0
        for i in range(i + 1, height):
            j = 0
            for j in range(j + 1, width):
                if s[i - 1] == t[j - 1]:
                    cost = 0
                else:
                    cost = 1
                insertion = matrix[i, j - 1] + 1
                deletion = matrix[i - 1, j] + 1
                substitution = matrix[i - 1, j - 1] + cost
                distance = min(insertion, deletion, substitution)
                if i > 1 and j > 1 and s[i - 1] == t[j - 2] and s[i - 2] == t[j - 1]:
                    distance = min(distance, matrix[i - 2, j - 2] + cost)
                matrix[i, j] = distance
        return matrix[height - 1, width - 1]

    def GetComparers(self):
        raise NotImplementedException()



