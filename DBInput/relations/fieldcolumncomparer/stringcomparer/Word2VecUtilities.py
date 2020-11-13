import difflib
from DBInput.DBIExceptions import InvalidOperationException, KeyNotFoundException
from nltk.corpus import wordnet as wn
import math
import re
from collections import Counter


class Word2VecUtilities:
    def __init__(self):
        self.model_path = None
        self.cached_closest_words = dict()
        self.cached_words_similarity = dict()
        self.max_similar_words = 1
        self.vocabulary = None
        self.reader = None
        self.is_loaded = False

    def IsLoaded(self):
        return self.is_loaded

    def Load(self, resources_path):
        self.model_path = resources_path
        # Da vedere cosa farci con model_path e simili
        self.vocabulary = list(wn.all_lemma_names())
        self.is_loaded = True

    def GetClosestWords(self, old_word):
        word = str(old_word)
        if not self.is_loaded:
            raise InvalidOperationException("Word2vec model has not been loaded")
        if self.cached_closest_words.__contains__(word):
            return self.cached_closest_words[word]
        close_matches = difflib.get_close_matches(word, self.vocabulary, 10)
        self.cached_closest_words[word] = close_matches
        return self.cached_closest_words[word]

    def GetWord2VecSimilarity(self, word1, word2):
        if not self.is_loaded:
            raise InvalidOperationException("Word2vec model has not been loaded")
        if not self.cached_words_similarity.__contains__(word1 + word2) or not self.cached_words_similarity.__contains__(word2 + word1):
            if word1 in self.vocabulary and word2 in self.vocabulary:
                similarity = self.get_cosine(word1, word2)
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
    def get_cosine(self, text1, text2):
        vec1 = self.text_to_vector(text1)
        vec2 = self.text_to_vector(text2)
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])
        sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
        sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    def text_to_vector(self, text):
        word = re.compile(r"\w+")
        words = word.findall(text)
        return Counter(words)
