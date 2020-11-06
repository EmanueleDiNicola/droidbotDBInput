from DBInput.DBIExceptions import InvalidOperationException
from nltk.corpus import wordnet as wn


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
        self.vocabulary = list(wn.all_lemma_names())
        self.is_loaded = True

    def GetClosestWords(self, word):
        if not self.is_loaded:
            raise InvalidOperationException("Word2vec model has not been loaded")
        #[word for word in wordnet_vocab if similar_string in word]
        # op if exact word is not present,  you can get similar word which are present in wordnet vocab
        #["alzheimer's", "alzheimer's_disease", 'alzheimers']

