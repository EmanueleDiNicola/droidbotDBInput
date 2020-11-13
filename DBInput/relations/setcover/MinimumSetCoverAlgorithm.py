from DBInput.relations.setcover.ISetCoverAlgorithm import ISetCoverAlgorithm
from py_linq import Enumerable
import itertools
import numpy as np


class MinimumSetCoverAlgorithm(ISetCoverAlgorithm):
    def __init__(self):
        self.current_best_value = None
        self.WEIGHT = 0.5
        self.MATCHES_UPPER_BOUND = 10000000
        self.R = 0.02
        self.DENSITY = 10
        self.NUM_BREAKS = 13

    def GenerateAllMatches(self, page, filtered_sims):
        group_sims = Enumerable(list())
        for field in page.get_fields():
            w_sims = list(filtered_sims.where(lambda fcr: fcr.field.same(field)))
            group_sims.append(w_sims)
        all_matches = Enumerable(list())
        for element in itertools.product(*group_sims):
            all_matches.add(element)
        if len(all_matches) < self.MATCHES_UPPER_BOUND:
            return all_matches
        else:
            return all_matches.take(self.MATCHES_UPPER_BOUND)

    def EvaluateBestmatch(self, page, all_matches):
        fields = page.get_fields()
        best_match = Enumerable(None)
        best_matches_by_value = DBSCANForMatches(all_matches)
        best_matches_by_used_tables_unit_fraction = Enumerable(list())
        best_used_tables_unit_fraction = 0.0
        best_value = 0.0
        for match in best_matches_by_value:
            current_used_tables_unit_fraction = self.ComputeMatchUsedTableUnitFraction(match)
            if (current_used_tables_unit_fraction > best_used_tables_unit_fraction) or \
                    ((current_used_tables_unit_fraction == best_used_tables_unit_fraction) and
                     (self.ComputeMatchValue(match) > best_value)):
                best_used_tables_unit_fraction = current_used_tables_unit_fraction
                best_value = self.ComputeMatchValue(match)
                best_matches_by_used_tables_unit_fraction = Enumerable(list())
                best_matches_by_used_tables_unit_fraction.add(match)
            else:
                if current_used_tables_unit_fraction == best_used_tables_unit_fraction and best_value == self.ComputeMatchValue(
                        match):
                    best_matches_by_used_tables_unit_fraction.add(match)
        choice = np.random.randint(0, len(best_matches_by_used_tables_unit_fraction))
        best_match = best_matches_by_used_tables_unit_fraction.element_at(choice)
        self.current_best_value = self.WEIGHT * (
                    self.ComputeMatchValue(best_match) + self.ComputeMatchUsedTableUnitFraction(best_match))
        return list(best_match)

    def ComputeMatchUsedTableUnitFraction(self, match):
        used_tables = Enumerable(list())
        for fcr in match:
            used_tables.append(fcr.column.tableName)
        return 1.0 / len(used_tables.distinct())

    def ComputeMatchValue(self, match):
        value = 0.0
        for fc in match:
            value = value + fc.value
        return value / len(match)
