from sklearn.cluster import DBSCAN
import numpy as np
from py_linq import Enumerable
from DBInput.relations.setcover.MinimumSetCoverAlgorithm import MinimumSetCoverAlgorithm

#INCOMPLETA, INTERROTTA
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    class WebDBSCAN:
        class DBSCANPoint:
            def __init__(self, x, y):
                self.point_point = None
                self.point = Point(x, y)

            def Point(self):
                return self.point

        def DBSCANForSims(self, similarities, R, DENSITY):
            enum_similarities = Enumerable(similarities)
            values = enum_similarities.order_by(lambda m: m.value).select(lambda m: m.value).to_list()
            return self.DBSCAN(values, R, DENSITY)

        def DBSCANForMatches(self, matches, R, DENSITY):
            values = Enumerable(list())
            for match in matches:
                values.append(MinimumSetCoverAlgorithm.ComputeMatchValue(match))
            values = values.order_by(lambda v: v).to_list()
            return self.DBSCAN(values, R, DENSITY)

        def DBSCAN(self, values, R, DENSITY):
            points = list()
            for v in values:
                p = Point(v, 0)
                points.append(p)
            return None
            #calculate clusters