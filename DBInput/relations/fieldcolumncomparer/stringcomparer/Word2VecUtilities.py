import difflib
from DBInput.DBIExceptions import InvalidOperationException, KeyNotFoundException
from nltk.corpus import wordnet as wn
import math
import re
from collections import Counter


class Word2VecUtilities:
    def __init__(self):
        self.cached_closest_words = dict()
        self.cached_words_similarity = dict()
        self.max_similar_words = 1
        self.vocabulary = None
        self.is_loaded = False

    def IsLoaded(self):
        return self.is_loaded

    def Load(self):
        self.vocabulary = list(wn.all_lemma_names())
        self.is_loaded = True

    def GetClosestWords(self, old_word):
        self.Load()
        word = str(old_word)
        if not self.is_loaded:
            raise InvalidOperationException("Word2vec model has not been loaded")
        if self.cached_closest_words.__contains__(word):
            return self.cached_closest_words[word]
        close_matches = difflib.get_close_matches(word, self.vocabulary, 10)
        self.cached_closest_words[word] = close_matches
        return self.cached_closest_words[word]

    def GetWord2VecSimilarity(self, word1, word2):
        self.Load()
        if not self.is_loaded:
            raise InvalidOperationException("Word2vec model has not been loaded")
        if not self.cached_words_similarity.__contains__(word1 + word2) or not self.cached_words_similarity.__contains__(word2 + word1):
            if word1 in self.vocabulary and word2 in self.vocabulary:
                similarity = self.cosdis(self.word2vec(word1), self.word2vec(word2))
                if similarity < 0:
                    similarity = 0
                if similarity > 1:
                    similarity = 1
                self.cached_words_similarity[word1 + word2] = similarity
                self.cached_words_similarity[word2 + word1] = similarity
            else:
                self.cached_words_similarity[word1 + word2] = 0
                self.cached_words_similarity[word2 + word1] = 0
                raise KeyNotFoundException()
        return self.cached_words_similarity[word1 + word2]

    # Codice preso in giro
    def word2vec(self, word):

        cw = Counter(word)
        sw = set(cw)
        lw = math.sqrt(sum(c * c for c in cw.values()))

        return cw, sw, lw

    def cosdis(self, v1, v2):
        common = v1[1].intersection(v2[1])
        return sum(v1[0][ch] * v2[0][ch] for ch in common) / v1[2] / v2[2]