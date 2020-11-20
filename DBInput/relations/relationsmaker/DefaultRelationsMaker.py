from DBInput.DBIExceptions import ArgumentNullException
from py_linq import Enumerable
from DBInput.relations.FieldColumnRelation import FieldColumnRelation
from DBInput.relations.PageDatabaseRelation import PageDatabaseRelation
from DBInput.relations.clustering.MyDBSCAN import MyDBSCAN
from DBInput.relations.fieldcolumncomparer.MaxQualityComparer import MaxQualityComparer
from DBInput.relations.fieldcolumncomparer.MeanQualityComparer import MeanQualityComparer
from DBInput.relations.fieldcolumncomparer.stringcomparer.DamerauLevenshteinStringComparer import \
    DamerauLevenshteinStringComparer
from DBInput.relations.fieldcolumncomparer.stringcomparer.EditDistanceStringComparer import EditDistanceStringComparer
from DBInput.relations.fieldcolumncomparer.stringcomparer.MaxComposedStringComparer import MaxComposedStringComparer
from DBInput.relations.fieldcolumncomparer.stringcomparer.MeanComposedStringComparer import MeanComposedStringComparer
from DBInput.relations.fieldcolumncomparer.stringcomparer.SynonymStringComparer import SynonymStringComparer
from DBInput.relations.fieldcolumncomparer.stringcomparer.Word2VecComparer import Word2VecComparer
from DBInput.relations.relationsmaker.IRelationsMaker import IRelationsMaker
from DBInput.relations.setcover.MinimumSetCoverAlgorithm import MinimumSetCoverAlgorithm


class DefaultRelationsMaker(IRelationsMaker):
    NUM_BREAKS = 13

    def __init__(self, relation_maker_type, field_column_comparer=None, set_cover_algorithm=None):
        if field_column_comparer is None and set_cover_algorithm is None:
            if relation_maker_type == "MAXSIMILARITY_MAXLABELS_OLD":
                string_comparer = MaxComposedStringComparer()
                string_comparer.AddComparer(EditDistanceStringComparer())
                string_comparer.AddComparer(SynonymStringComparer())
                string_comparer.AddComparer(DamerauLevenshteinStringComparer())
                self.field_column_comparer = MaxQualityComparer(string_comparer)
            if relation_maker_type == "MEANSIMILARITY_MAXLABELS_OLD":
                string_comparer = MeanComposedStringComparer()
                string_comparer.AddComparer(EditDistanceStringComparer())
                string_comparer.AddComparer(SynonymStringComparer())
                string_comparer.AddComparer(DamerauLevenshteinStringComparer())
                self.field_column_comparer = MaxQualityComparer(string_comparer)
            if relation_maker_type == "MAXSIMILARITY_MEANLABELS_OLD":
                string_comparer = MaxComposedStringComparer()
                string_comparer.AddComparer(EditDistanceStringComparer())
                string_comparer.AddComparer(SynonymStringComparer())
                string_comparer.AddComparer(DamerauLevenshteinStringComparer())
                self.field_column_comparer = MeanQualityComparer(string_comparer)
            if relation_maker_type == "MEANSIMILARITY_MEANLABELS_OLD":
                string_comparer = MeanComposedStringComparer()
                string_comparer.AddComparer(EditDistanceStringComparer())
                string_comparer.AddComparer(SynonymStringComparer())
                string_comparer.AddComparer(DamerauLevenshteinStringComparer())
                self.field_column_comparer = MeanQualityComparer(string_comparer)
            if relation_maker_type == "MAXSIMILARITY_MAXLABELS_NEW":
                string_comparer = MaxComposedStringComparer()
                string_comparer.AddComparer(EditDistanceStringComparer())
                string_comparer.AddComparer(Word2VecComparer(False))
                self.field_column_comparer = MaxQualityComparer(string_comparer)
            if relation_maker_type == "MEANSIMILARITY_MAXLABELS_NEW":
                string_comparer = MeanComposedStringComparer()
                string_comparer.AddComparer(EditDistanceStringComparer())
                string_comparer.AddComparer(Word2VecComparer(False))
                self.field_column_comparer = MaxQualityComparer(string_comparer)
            if relation_maker_type == "MAXSIMILARITY_MEANLABELS_NEW":
                string_comparer = MaxComposedStringComparer()
                string_comparer.AddComparer(EditDistanceStringComparer())
                string_comparer.AddComparer(Word2VecComparer(False))
                self.field_column_comparer = MeanQualityComparer(string_comparer)
            if relation_maker_type == "MEANSIMILARITY_MEANLABELS_NEW":
                string_comparer = MeanComposedStringComparer()
                string_comparer.AddComparer(EditDistanceStringComparer())
                string_comparer.AddComparer(Word2VecComparer(False))
                self.field_column_comparer = MeanQualityComparer(string_comparer)
            self.set_cover_algorithm = MinimumSetCoverAlgorithm()
        else:
            self.field_column_comparer = field_column_comparer
            self.set_cover_algorithm = set_cover_algorithm

    def FindBestMatch(self, page, database):
        if page is None:
            raise ArgumentNullException("Page")
        if database is None:
            raise ArgumentNullException("Database")
        if len(page.get_fields()) == 0:
            return self.CreatePageDatabaseRelation(list(), page)
        all_sims = self.ComputeAllSimilarities(page, database)
        filtered_sims = self.FilterSimilarities(page, all_sims)
        all_matches = self.GenerateAllMatches(page, filtered_sims)
        best_match = self.EvaluateBestMatch(page, all_matches)
        return self.CreatePageDatabaseRelation(best_match, page)

    def CreatePageDatabaseRelation(self, choosen_relations, page):
        field_column_relation = dict()
        for field in page.get_fields():
            field_column_relation[field] = Enumerable(choosen_relations).where(lambda fc: fc.field.equals(field)) \
                .first()
        return PageDatabaseRelation(page, field_column_relation.values(), MinimumSetCoverAlgorithm().current_best_value)

    def ComputeAllSimilarities(self, page, database):
        all_sims = list()
        for field in page.get_fields():
            for table in database.tables:
                for column in table.columns:
                    value = self.field_column_comparer.Compare(field, column)
                    sim = FieldColumnRelation(field, column, value)
                    all_sims.append(sim)
        return all_sims

    def FilterSimilarities(self, page, all_sims):
        filtered_sims = Enumerable(list())
        all_sims_enum = Enumerable(all_sims)
        for field in page.get_fields():
            sim_for_field = all_sims_enum.where(lambda s: s.field.same(field)).to_list()
            filtered_sims = filtered_sims.concat(MyDBSCAN().DBSCANForSims(sim_for_field)).to_list()
        schemas = dict()
        for fc in filtered_sims:
            if fc.column.tableName not in schemas:
                columns = list()
                schemas[fc.column.tableName] = columns.append(fc.column.name)
            else:
                if fc.column.name not in schemas[fc.column.tableName]:
                    schemas[fc.column.tableName] = schemas[fc.column.tableName].append(fc.column.name)
        for schema in schemas.keys():
            print("Columns for " + schema + ":")
            print(schemas[schema])
            print("---------------------------------")
        work_list = list(schemas.keys())
        for first_schema in schemas.keys():
            work_list.remove(first_schema)
            first_schema_similarity = self.ComputePageTableSimilarity(page, first_schema)
            for second_schema in work_list:
                first_schema_enum = Enumerable(schemas[first_schema])
                second_schema_enum = Enumerable(schemas[second_schema])
                first_contained = first_schema_enum.all(lambda i: i in schemas[second_schema])
                second_contained = second_schema_enum.all(lambda i: i in schemas[first_schema])
                equal = first_contained and second_contained
                second_schema_similarity = self.ComputePageTableSimilarity(page, second_schema)
                if (first_contained and not equal) or (equal and first_schema_similarity <= second_schema_similarity):
                    filtered_sims = filter(lambda element: element.column.tableName == second_schema,
                                           filtered_sims.to_list())
                    break
                if (second_contained and not equal) or (equal and second_schema_similarity <= first_schema_similarity):
                    filtered_sims = filter(lambda element: element.column.tableName == first_schema,
                                           filtered_sims.to_list())
                    break
        schemas = dict()
        for fc in filtered_sims:
            if fc.column.tableName not in schemas:
                columns = list()
                schemas[fc.column.tableName] = columns.append(fc.column.name)
            else:
                if fc.column.name not in schemas[fc.column.tableName]:
                    schemas[fc.column.tableName] = schemas[fc.column.tableName].append(fc.column.name)
        for schema in schemas.keys():
            print("Columns for " + schema + ":")
            print(schemas[schema])
            print("---------------------------------")
        return filtered_sims

    def GenerateAllMatches(self, page, filtered_sims):
        return self.set_cover_algorithm.GenerateAllMaches(page, filtered_sims)

    def EvaluateBestMatch(self, page, all_matches):
        return self.set_cover_algorithm.EvaluateBestMatch(page, all_matches)

    def ComputePageTableSimilarity(self, page, table):
        comparers = self.field_column_comparer.GetComparer().GetComparers()
        title = page.get_title()
        url = self.CutAllButPageName(page.get_url())
        title_syntactic_similarity = comparers[0].StringSimilarity(title, table)
        title_semantic_similarity = comparers[1].StringSimilarity(title, table)
        title_similarity = max(title_semantic_similarity, title_syntactic_similarity)
        utl_syntactic_similarity = comparers[0].StringSimilarity(url, table)
        url_semantic_similarity = comparers[1].StringSimilarity(url, table)
        url_similarity = max(utl_syntactic_similarity, url_semantic_similarity)
        return (title_similarity + url_similarity) / 2

    def CutAllButPageName(self, url):
        index = url.rfind('/')
        if index > 0:
            url = url[index + 1:]
        index = url.rfind('/')
        if index > 0:
            url = url[:index]
        return url
