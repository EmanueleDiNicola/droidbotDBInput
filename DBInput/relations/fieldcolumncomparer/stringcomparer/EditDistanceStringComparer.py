from DBInput.DBIExceptions import NotImplementedException
from DBInput.relations.fieldcolumncomparer import StringTransformation
from DBInput.relations.fieldcolumncomparer.stringcomparer import Tokenizer
from DBInput.relations.fieldcolumncomparer.stringcomparer.CachedLemmatizer import CachedLemmatizer
from DBInput.relations.fieldcolumncomparer.stringcomparer.IStringComparer import IStringComparer
import nltk.metrics.distance


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
        if len(s1_tokens) >= len(s2_tokens):
            longest = s1_tokens
            shortest = s2_tokens
        else:
            longest = s2_tokens
            shortest = s1_tokens
        sum = 0.0
        for t1 in longest:
            max_similarity = 0.0
            for t2 in shortest:
                similarity = self.GetEditDistance(t1, t2)
                #print("Similarity = " + t1 + " " + t2 + " = " + str(similarity))
                if similarity > max_similarity:
                    #print("Similarity = " + str(similarity))
                    max_similarity = similarity
                    #print("Max Similarity = " + str(max_similarity))
            sum = sum + max_similarity
            #print("Sum = " + str(sum))
        #print("Shortest = " + str(shortest) + " " + str(len(shortest)))
        #print("Longest = " + str(longest) + " " + str(len(longest)))
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
            if token is not '':
                lemmatized_tokens.add(CachedLemmatizer.Lemmatize(CachedLemmatizer(), token))
        return lemmatized_tokens

    def GetEditDistance(self, s1, s2):
        if not (self.cached_word_similarity.__contains__(s1 + s2) or self.cached_word_similarity.__contains__(s1 + s2)):
            edit_distance = nltk.edit_distance(s1, s2)
            len_s1 = len(s1)
            len_s2 = len(s2)
            len_tot = len_s1 + len_s2
            similarity = 1 - (edit_distance/len_tot)
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
