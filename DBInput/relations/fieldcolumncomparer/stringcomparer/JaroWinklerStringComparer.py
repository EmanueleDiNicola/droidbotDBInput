from DBInput.DBIExceptions import NotImplementedException
from DBInput.relations.fieldcolumncomparer import StringTransformation
from DBInput.relations.fieldcolumncomparer.stringcomparer.IStringComparer import IStringComparer
import numpy as np
from numpy.core.defchararray import lower


class JaroWinklerStringComparer(IStringComparer):

    def __init__(self):
        pass

    def StringSimilarity(self, s1, s2):
        cleans1 = StringTransformation.CleanString(s1)
        cleans2 = StringTransformation.CleanString(s2)
        if s1 == "" or s2 == "":
            return 0
        return JaroWinkler().Proximity(cleans1, cleans2)

    def GetComparers(self):
        raise NotImplementedException()


class JaroWinkler:
    default_mismatch_score = 0.0
    default_match_score = 1.0

    def __init__(self):
        self.mWeightThreshold = 0.7
        self.mNumChars = 4

    def Distance(self, a_string1, a_string2):
        return 1.0 - self.Proximity(a_string1, a_string2)

    def Proximity(self, a_string1, a_string2):
        len1 = len(a_string1)
        len2 = len(a_string2)
        if len1 == 0:
            if len2 == 0:
                return 1.0
            else:
                return 0.0
        search_range = max(0, (max(len1, len2) / 2) - 1)
        matched1 = np.zeros(len1, dtype=bool)
        matched2 = np.zeros(len2, dtype=bool)
        num_common = 0
        for i in range(len1):
            start = int(max(0, i - search_range))
            end = min(i + search_range + 1, len2)
            j = start
            while j < end:
                if matched2[j]:
                    j = j + 1
                    continue
                if a_string1[i] != a_string2[j]:
                    j = j + 1
                    continue
                matched1[i] = True
                matched2[j] = True
                num_common = num_common + 1
                j = j + 1
        if num_common == 0:
            return 0.0
        num_half_transposed = 0
        k = 0
        for i in range(len(a_string1)):
            if not matched1[i]:
                continue
            while not matched2[k]:
                k = k + 1
            if a_string1[i] != a_string2[k]:
                num_half_transposed = num_half_transposed + 1
            k = k + 1
        num_transposed = num_half_transposed / 2
        num_common_d = num_common
        i_weight = (num_common_d / len1 + num_common_d / len2
                    + (num_common - num_transposed) / num_common_d) / 3.0
        if i_weight <= self.mWeightThreshold:
            return i_weight
        i_max = min(self.mNumChars, min(len(a_string1), len(a_string2)))
        i_pos = 0
        while i_pos < i_max and a_string1[i_pos] == a_string2[i_pos]:
            i_pos = i_pos + 1
        if i_pos == 0:
            return i_weight
        return i_weight + 0.1 * i_pos * (1.0 - i_weight)

    def RateSimilarity(self, first_word, second_word):
        first_word = lower(first_word)
        second_word = lower(second_word)
        if first_word is not None and second_word is not None:
            if first_word == second_word:
                return self.default_match_score
            else:
                half_length = min(len(first_word), len(second_word)) / 2 + 1
                common1 = self.GetCommonCharacters(first_word, second_word, half_length)
                common_matches = len(common1)
                if common_matches == 0:
                    return self.default_match_score
                common2 = self.GetCommonCharacters(second_word, first_word, half_length)
                if common_matches != len(common2):
                    return self.default_match_score
                transpositions = 0
                for i in common_matches:
                    if common1[i] != common2[i]:
                        transpositions = transpositions + 1
                transpositions = transpositions / 2
                jaro_metric = common_matches / (3.0 * len(first_word)) + common_matches / (3.0 * len(second_word)
                                                                                           ) + (
                                      common_matches - transpositions) / (3.0 * common_matches)
                return jaro_metric
        return self.default_match_score

    def GetCommonCharacters(self, first_word, second_word, separation_distance):
        if first_word is not None and second_word is not None:
            return_commons = ""
            copy = second_word
            len1 = len(first_word)
            len2 = len(second_word)
            for i in range(len(first_word)):
                character = first_word[i]
                found = False
                j = max(0, i - separation_distance)
                while not found and j < min(i + separation_distance, len2):
                    if copy[j] == character:
                        found = True
                        return_commons = return_commons + character
                        copy[j] = '#'
                    j = j + 1
            return return_commons
        return None
