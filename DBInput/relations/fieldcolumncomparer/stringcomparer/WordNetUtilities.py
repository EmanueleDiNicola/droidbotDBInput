from typing import Any

import nltk
from DBInput.DBIExceptions import InvalidOperationException
from nltk.corpus import wordnet


class WordNetUtilities:
    def __init__(self):
        self.is_loaded = False
        self.cached_syn_sets = dict()

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def Load(self, resources_path):
        nltk.data.path = resources_path
        self.is_loaded = True

    def GetSynSets(self, word):
        if not self.is_loaded:
            raise InvalidOperationException("Wordnet has not been implemented")
        if self.cached_syn_sets.__contains__(word):
            return self.cached_syn_sets[word]
        syn_sets = wordnet.synsets(word)
        self.cached_syn_sets[word] = syn_sets
        return syn_sets
