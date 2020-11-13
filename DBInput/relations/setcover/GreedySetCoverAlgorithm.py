from DBInput.DBIExceptions import NotImplementedException
from DBInput.relations.setcover.ISetCoverAlgorithm import ISetCoverAlgorithm


class GreedySetCoverAlgorithm(ISetCoverAlgorithm):
    def __init__(self):
        pass

    def EvaluateBestmatch(self, page, all_combinations):
        raise NotImplementedException()

    def GenerateAllMatches(self, page, all_matches):
        raise NotImplementedException()