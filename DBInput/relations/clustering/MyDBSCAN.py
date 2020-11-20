import numpy as np
from py_linq import Enumerable

from DBInput.relations.setcover.MinimumSetCoverAlgorithm import MinimumSetCoverAlgorithm


class MyDBSCAN:
    def __init__(self):
        pass

    def EstimateDensity(self, values):
        return np.log(len(values))

    def EstimateRadius(self, values, density):
        k = density
        if k == 0:
            return 0
        k_distances = Enumerable()
        for i in range(len(values)):
            if i < k:
                preceding_ks = values[0:i]
            else:
                preceding_ks = values[i - k:k]
            if (i + k) > (len(values) - 1):
                succeeding_ks = values[i + 1: len(values) - 1 - i]
            else:
                succeeding_ks = values[i + 1: k]
            all_k_neighbors = preceding_ks.concat(succeeding_ks).to_list()
            closest_k_neighbors = all_k_neighbors.select(lambda n: np.abs(values[i] - n)).order_by(
                lambda d: d).to_list()
            k_distances.append(sum(closest_k_neighbors) / len(closest_k_neighbors))
        k_distances = k_distances.order_by(lambda d: d).to_list()
        elbow_index = self.FindElbow(k_distances)
        return k_distances[elbow_index]

    def FindElbow(self, k_distances):
        max_d = -1000
        elbow_index = -1
        for i in range(len(k_distances)):
            diff = np.abs(k_distances[i + 1] - k_distances[i])
            if diff > max_d:
                max_d = diff
                elbow_index = 1
        return elbow_index

    def DBSCANForSims(self, similarities):
        values = similarities.order_by(lambda s: s.value).select(lambda s: s.value).to_list()
        DENSITY = self.EstimateDensity(values)
        R = self.EstimateRadius(values, DENSITY)
        cluster = self.DBSCAN(values, R, DENSITY)
        similarities = similarities.where(lambda s: s.value in cluster).to_list()
        return similarities

    def DBSCAN(self, values, R, DENSITY):
        cluster = Enumerable()
        old_size = 0
        new_size = None
        neighbors = values.where(lambda vv: (values.last(lambda x: x) - vv) <= R)
        if len(neighbors) < DENSITY:
            highest_value = vlues.last(lambda x: x)
            cluster = values.where(lambda v: v == highest_value)
            return cluster.to_list()
        cluster = cluster.concat(neighbors)
        while old_size != new_size:
            old_size = len(cluster)
            for i in range(len(neighbors)):
                values.pop()
            furthest_neighbor = cluster.order_by(lambda v: v).first()
            neighbors = values.where(lambda vv: (furthest_neighbor - vv) <= R).to_list()
            if len(neighbors) < DENSITY:
                return cluster.to_list()
            cluster = cluster.concat(neighbors)
            new_size = len(cluster)
        return cluster.to_list()

    def DBSCANForMatches(self, matches):
        values = Enumerable()
        for match in matches:
            values.append(MinimumSetCoverAlgorithm.ComputeMatchValue(match))
        values = values.order_by(lambda v: v).to_list()
        DENSITY = self.EstimateDensity(values)
        R = self.EstimateRadius(values, DENSITY)
        cluster = self.DBSCAN(values, R, DENSITY)
        matches = matches.where(lambda m: MinimumSetCoverAlgorithm.ComputeMatchValue(m) in cluster).to_list()
        return matches

    def DBSCANGeneral(self, similarities):
        values = similarities.order_by(lambda s: s.Similarity).select(lambda s: s.Similarity).to_list()
        DENSITY = self.EstimateDensity(values)
        R = self.EstimateRadius(values, DENSITY)
        cluster = self.DBSCAN(values, R, DENSITY)
        similarities = similarities.where(lambda s: s.Similarity in cluster).to_list()
        return similarities
