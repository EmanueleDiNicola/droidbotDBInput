from DBInput.relations.fieldcolumncomparer.stringcomparer.IStringComparer import IStringComparer


class Word2VecComparer(IStringComparer):
    def __init__(self, use_closest_words):
        self.use_closest_words = use_closest_words
        self.cached_words_similarity = dict()
        