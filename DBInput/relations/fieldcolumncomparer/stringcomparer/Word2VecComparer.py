from numpy.core.defchararray import lower

from DBInput.DBIExceptions import NotImplementedException
from DBInput.relations.fieldcolumncomparer import StringTransformation
from DBInput.relations.fieldcolumncomparer.stringcomparer import Tokenizer
from DBInput.relations.fieldcolumncomparer.stringcomparer.CachedLemmatizer import CachedLemmatizer
from DBInput.relations.fieldcolumncomparer.stringcomparer.IStringComparer import IStringComparer
from DBInput.relations.fieldcolumncomparer.stringcomparer.Word2VecUtilities import Word2VecUtilities


class Word2VecComparer(IStringComparer):
    def __init__(self, use_closest_words):
        self.use_closest_words = use_closest_words
        self.cached_words_similarity = dict()
        self.w_2_vec_util = Word2VecUtilities()
        if not self.w_2_vec_util.IsLoaded():
            # Inserire path coerente
            self.w_2_vec_util.Load("Path")

    def StringSimilarity(self, s1, s2):
        if len(s1) == 0 or len(s2) == 0:
            return 0
        if self.cached_words_similarity.__contains__(s1 + s2):
            return self.cached_words_similarity[s1 + s2]
        if self.cached_words_similarity.__contains__(s2 + s1):
            return self.cached_words_similarity[s2 + s1]
        s1_tokens = self.GetLemmatizedTokens(s1)
        s2_tokens = self.GetLemmatizedTokens(s2)
        if len(s1_tokens) >= len(s2_tokens):
            longest = s1_tokens
            shortest = s2_tokens
        else:
            longest = s2_tokens
            shortest = s1_tokens
        sum = 0.0
        for t1 in longest:
            max = 0.0
            for t2 in shortest:
                if self.use_closest_words:
                    similarity = self.ComputeClosestWordsSimilarity(t1, t2)
                else:
                    print(str(t1) + " " + str(type(t1)))
                    print(str(t2) + " " + str(type(t2)))
                    similarity = self.w_2_vec_util.GetWord2VecSimilarity(t1, t2)
                if similarity > max:
                    max = similarity
            sum = sum + max
        mean = sum / len(longest)
        self.cached_words_similarity[s1 + s2] = self.cached_words_similarity[s2 + s1] = mean
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
            if token is not '':
                lemmatized_tokens.add(CachedLemmatizer.Lemmatize(CachedLemmatizer(), token))
        return lemmatized_tokens

    def ComputeClosestWordsSimilarity(self, s1, s2):
        max = 0
        s1_closest_words = self.GetClosesWords(s1)
        s2_closest_wprds = self.GetClosesWords(s2)
        for ss1 in s1_closest_words:
            for ss2 in s2_closest_wprds:
                syn_similarity = self.w_2_vec_util.GetWord2VecSimilarity(str(lower(ss1)), str(lower(ss2)))
                if syn_similarity > max:
                    max = syn_similarity
        return max

    def GetClosesWords(self, s1):
        closest_words = self.w_2_vec_util.GetClosestWords(lower(s1))
        return closest_words

    def GetComparers(self):
        raise NotImplementedException()

