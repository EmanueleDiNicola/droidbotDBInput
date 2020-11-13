from py_linq import Enumerable
import numpy as np
from DBInput.DBIExceptions import ArgumentNullException


class CombinationsGenerator:
    def __init__(self, elements):
        if elements is None:
            raise ArgumentNullException("Elements")
        self.elements = elements
        self.indexes = np.array([False] * len(elements))
        self.combination_number = 0

    def GetEnumerator(self):
        while self.HasNext():
            yield self.GetNext()

    def Getnext(self):
        self.IncrementIndexes()
        return self.GetCombination()

    def IncrementIndexes(self):
        x = self.combination_number
        i = 0
        while i < len(self.indexes) and x > 0:
            self.indexes[i] = x % 2 == 1
            x = x / 2
            i = i + 1
        self.combination_number = self.combination_number + 1

    def GetCombination(self):
        combination = list()
        for i in range(len(self.indexes)):
            if self.indexes[i]:
                combination.append(self.elements[i])
        return combination

    def Hasnext(self):
        for i in range(len(self.indexes)):
            if not self.indexes[i]:
                return true
        return false

