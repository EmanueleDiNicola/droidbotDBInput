from DBInput.DBIExceptions import NotImplementedException
from DBInput.relations.fieldcolumncomparer import StringTransformation
from DBInput.relations.fieldcolumncomparer.stringcomparer import Tokenizer
from DBInput.relations.fieldcolumncomparer.stringcomparer.CachedLemmatizer import CachedLemmatizer
from DBInput.relations.fieldcolumncomparer.stringcomparer.IStringComparer import IStringComparer
import


class EditDistanceStringComparer(IStringComparer):
    def __init__(self):
        self.cached_word_similarity = dict()

    def StringSimilarity(self, s1, s2):
        if len(s1) == 0 or len(s2) == 0:
            return 0
        if self.cached_word_similarity.__contains__(s1 + s2):
            return self.cached_word_similarity[s1 + s2]
        if self.cached_word_similarity.__contains__(s2 + s1):
            return self.cached_word_similarity[s2 + s1]
        s1_tokens = self.GetLemmatizedTokens(s1)
        s2_tokens = self.GetLemmatizedTokens(s2)
        if s1_tokens >= s2_tokens:
            longest = s1_tokens
            shortest = s2_tokens
        else:
            longest = s2_tokens
            shortest = s1_tokens
        sum = 0.0
        for t1 in longest:
            max = 0.0
            for t2 in shortest:
                similarity = self.GetEditDistance(t1, t2)
                if similarity > max:
                    max = similarity
            sum = sum + max
        mean = sum / len(longest)
        self.cached_word_similarity[s1 + s2] = self.cached_word_similarity[s2 + s1] = mean
        return mean

    def GetLemmatizedTokens(self, s):
        tokens = Tokenizer.SplitSeparators(Tokenizer.SplitCamelCase(s))
        clean_tokens = set()
        for token in tokens:
            clean_token = StringTransformation.CleanString(token)
            if clean_tokens != "":
                clean_tokens.add(clean_token.lower())
        lemmatized_tokens = set()
        for token in clean_tokens:
            lemmatized_tokens.add(CachedLemmatizer.Lemmatize(CachedLemmatizer(), token))
        return lemmatized_tokens

    def GetEditDistance(self, s1, s2):
        diff = self.Diff(s1, s2)
        print(diff)
        lcs = self.Longest_Common_Subsequence(s1, s2)
        if not (self.cached_word_similarity.__contains__(s1 + s2) or self.cached_word_similarity.__contains__(s1 + s2)):
            similarity = self.GetSimilarity(diff, lcs)
            if similarity < 0:
                similarity = 0
            else:
                if similarity > 1:
                    similarity = 1
            self.cached_word_similarity[s1 + s2] = similarity
            self.cached_word_similarity[s2 + s1] = similarity
        return self.cached_word_similarity[s1 + s2]

    def GetComparers(self):
        raise NotImplementedException()

    def Longest_Common_Subsequence(self, xs, ys):
        totallen = len(xs) + len(ys)
        frontier = [0] * (2 * totallen + 1)
        candidates = [None] * (2 * totallen + 1)
        for d in range(totallen + 1):
            for k in range(-d, d + 1, 2):
                if k == -d or (k != d and frontier[totallen + k - 1] < frontier[totallen + k + 1]):
                    index = totallen + k + 1
                    x = frontier[index]
                else:
                    index = totallen + k - 1
                    x = frontier[index] + 1
                y = x - k
                chain = candidates[index]
                while x < len(xs) and y < len(ys) and xs[x] == ys[y]:
                    chain = ((x, y), chain)
                    x = x + 1
                    y = y + 1
                if x >= len(xs) and y >= len(ys):
                    result = []
                    while chain:
                        result.append(chain[0])
                        chain = chain[1]
                    result.reverse()
                    return result
                frontier[totallen + k] = x
                candidates[totallen + k] = chain

    def Diff(self, xs, ys):
        i = -1
        j = -1
        matches = self.Longest_Common_Subsequence(xs, ys)
        matches.append((len(xs), len(ys)))
        result = []
        for (mi, mj) in matches:
            if mi - i > 1 or mj - j > 1:
                result.append((i + 1, mi - i - 1, j + 1, mj - j - 1))
            i = mi
            j = mj
        return result

    def GetSimilarity(self, diff, lcs):
        length_a = len(diff[0])
        length_b = len(diff[1])
        length_lcs = max(max(lcs))
        result = (2.0 * length_lcs) / (length_a + length_b)
        return result

    def Functtest(self, s1, s2):
        length_a = len(s1)
        length_b = len(s2)
        length_lcs = max(max(self.Longest_Common_Subsequence(s1, s2)))
        result = (2.0 * length_lcs) / (length_a + length_b)
        return result
