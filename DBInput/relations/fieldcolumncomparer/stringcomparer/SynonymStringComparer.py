from nltk.corpus import wordnet
from DBInput.DBIExceptions import NotImplementedException
from DBInput.relations.fieldcolumncomparer.StringTransformation import CleanString
from DBInput.relations.fieldcolumncomparer.stringcomparer.CachedLemmatizer import CachedLemmatizer
from DBInput.relations.fieldcolumncomparer.stringcomparer.IStringComparer import IStringComparer
from DBInput.relations.fieldcolumncomparer.stringcomparer.Tokenizer import SplitCamelCase, SplitSeparators
from DBInput.relations.fieldcolumncomparer.stringcomparer.WordNetUtilities import WordNetUtilities


class SynonymStringComparer(IStringComparer):
    def __init__(self):
        self.SYNONYM_SIMILARITY = 0.9
        self.word_net_utilities = WordNetUtilities()
        self.cached_lemmatizer = CachedLemmatizer()
        if not self.word_net_utilities.is_loaded:
            self.word_net_utilities.Load()
        if not self.cached_lemmatizer.is_loaded:
            self.cached_lemmatizer.Load()
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
            lemmatized_tokens.add(self.cached_lemmatizer.Lemmatize(token))
        return lemmatized_tokens

    def Tokenize(self, str):
        return SplitSeparators(SplitCamelCase(str))

    def GetComparers(self):
        raise NotImplementedException()

    def GetSynonyms(self, lemma):
        if lemma in self.cached_synonyms:
            return self.cached_synonyms[lemma]
        syn_set_list = self.word_net_utilities.GetSynSets(lemma)
        synonyms = set()
        for syn_set in syn_set_list:
            synonyms.add(syn_set.lemmas()[0].name())
        if lemma in synonyms:
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

    def StringSimilarity2(self, word_1, word_2):
        s1_lemmas = self.GetLemmas(word_1)
        s2_lemmas = self.GetLemmas(word_2)
        tot = 0
        for s1_lemma in s1_lemmas:
            set_1 = wordnet.synsets(s1_lemma)
            max_value = 0
            #best_word_1 = None
            #best_word_2 = None
            for s2_lemma in s2_lemmas:
                set_2 = wordnet.synsets(s2_lemma)
                for word_set_1 in set_1:
                    for word_set_2 in set_2:
                        value = word_set_1.wup_similarity(word_set_2)
                        #print(word_set_1.name() + " " + word_set_2.name() + " = " + str(value))
                        if value is not None and value > max_value:
                            max_value = value
                            #best_word_1 = word_set_1.name()
                            #best_word_2 = word_set_2.name()
            #print(best_word_1 + " - " + best_word_2 + " = " + str(max_value))
            tot = tot + max_value
        return tot / (max(len(s1_lemmas), len(s2_lemmas)))
