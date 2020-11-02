import nltk
from DBInput.DBIExceptions import NotImplementedException
from DBInput.relations.fieldcolumncomparer.StringTransformation import CleanString
from DBInput.relations.fieldcolumncomparer.stringcomparer.CachedLemmatizer import CachedLemmatizer
from DBInput.relations.fieldcolumncomparer.stringcomparer.IStringComparer import IStringComparer
from DBInput.relations.fieldcolumncomparer.stringcomparer.Tokenizer import SplitCamelCase, SplitSeparators
from DBInput.relations.fieldcolumncomparer.stringcomparer.WordNetUtilities import WordNetUtilities


class SynonymStringComparer(IStringComparer):
    def __init__(self):
        self.SYNONYM_SIMILARITY = 0.9
        if not WordNetUtilities.is_loaded:
            # TODO Controlla la funzione Load
            WordNetUtilities.Load("DBInput.ABTSettinfs.settings")
        if not CachedLemmatizer.is_loaded:
            CachedLemmatizer.Load("DBInput.ABTSettinfs.settings")
        self.cached_synonyms = dict()

    def StringSimilarity(self, s1, s2):
        s1_lemmas = self.GetLemmas(s1)
        s2_lemmas = self.GetLemmas(s2)
        intersection = 0
        for lemma in s1_lemmas:
            if lemma in s2_lemmas:
                intersection = intersection + 1
            else:
                synonyms = self.GetSynonyms(lemma)
                intersection = intersection + self.IntersectionValue(s2_lemmas, synonyms)
        similarity = self.ComputeSimilarity(s1_lemmas, s2_lemmas, intersection)
        if similarity is None:
            return 0
        else:
            return similarity

    def GetLemmas(self, str):
        tokens = set(self.Tokenize(str))
        clean_tokens = set()
        for token in tokens:
            clean_token = CleanString(token)
            if clean_token is not "":
                clean_tokens.add(clean_token)
        return self.Lemmatize(clean_tokens)

    def Lemmatize(self, tokens):
        lemmatized_tokens = set()
        for token in tokens:
            lemmatized_tokens.add(CachedLemmatizer.Lemmatize(token))
        return lemmatized_tokens

    def Tokenize(self, str):
        return SplitSeparators(SplitCamelCase(str))

    def GetComparers(self):
        raise NotImplementedException()

    def GetSynonyms(self, lemma):
        if lemma in self.cached_synonyms:
            return self.cached_synonyms[lemma]
        syn_set_list = WordNetUtilities.GetSynSets(lemma)
        synonyms = set()
        for syn_set in syn_set_list:
            synonyms.union(syn_set.Words)
            # VEDI COS'E' in debug
        synonyms.remove(lemma)
        self.cached_synonyms[lemma] = synonyms
        return synonyms

    def IntersectionValue(self, s2_lemmas, synonyms):
        for synonym in synonyms:
            if synonym in s2_lemmas:
                return self.SYNONYM_SIMILARITY
        return 0

    def ComputeSimilarity(self, s1_lemmas, s2_lemmas, intersection):
        return intersection / (len(s1_lemmas) + len(s2_lemmas) - intersection)
