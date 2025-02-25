from typing import Any

from DBInput.DBIExceptions import InvalidOperationException
from nltk.stem import WordNetLemmatizer


class CachedLemmatizer:
    def __init__(self):
        self.cached_lemmas = dict()
        self.lemmatizer = WordNetLemmatizer()
        self.is_loaded = False
        self.Load()

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def Load(self):
        self.is_loaded = True

    def Lemmatize(self, word):
        if not self.is_loaded:
            raise InvalidOperationException("Lemmatizer has not been loaded")
        if self.cached_lemmas.__contains__(word):
            return self.cached_lemmas[word]
        lemma = self.lemmatizer.lemmatize(word)
        self.cached_lemmas[word] = lemma
        return lemma
