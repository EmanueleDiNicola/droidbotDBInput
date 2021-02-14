from DBInput.database.Column import Column
from DBInput.database.DatabaseStructureFactory import DatabaseStructureFactory
from DBInput.database.Table import Table
from DBInput.query.CachedMicrosoftSqlQueryEngine import CachedMicrosoftSqlQueryEngine
from DBInput.query.DefaultSqlDatabaseInfo import DefaultSqlDatabaseInfo
from DBInput.query.SqlDatabaseInfo import SqlDatabaseInfo
from DBInput.relations.FieldColumnRelation import FieldColumnRelation
from DBInput.relations.PageDatabaseRelation import PageDatabaseRelation
from DBInput.relations.TablePageRelation import TablePageRelation
from DBInput.relations.fieldcolumncomparer.stringcomparer.DamerauLevenshteinStringComparer import \
    DamerauLevenshteinStringComparer
from DBInput.relations.fieldcolumncomparer.stringcomparer.EditDistanceStringComparer import EditDistanceStringComparer
from DBInput.relations.fieldcolumncomparer.stringcomparer.JaroWinklerStringComparer import JaroWinklerStringComparer
from DBInput.relations.fieldcolumncomparer.stringcomparer.MaxComposedStringComparer import MaxComposedStringComparer
from DBInput.relations.fieldcolumncomparer.stringcomparer.MeanComposedStringComparer import MeanComposedStringComparer
from DBInput.relations.fieldcolumncomparer.stringcomparer.SynonymStringComparer import SynonymStringComparer
from DBInput.relations.fieldcolumncomparer.stringcomparer.Tokenizer import SplitCamelCase, SplitSeparators
from DBInput.relations.fieldcolumncomparer.stringcomparer.Word2VecComparer import Word2VecComparer
from DBInput.relations.fieldcolumncomparer.stringcomparer.Word2VecUtilities import Word2VecUtilities
from DBInput.relations.relationsmaker.DefaultRelationsMaker import DefaultRelationsMaker
from DBInput.webapp.Field import Field
from DBInput.webapp.Label import Label
from DBInput.webapp.Page import Page

"""

labelA = Label("A")
labelB = Label("B")
fieldA = Field([labelA])
fieldB = Field([labelB])
fieldC = Field([labelA, labelB])
pageA = Page([fieldA], "www.ciao.it", "Ciao")
pageB = Page([fieldA, fieldB], "www.ciao2.it", "Ciao2")
columnA = Column("ColonnaA", "TabellaA")
columnB = Column("ColonnaB", "TabellaB")
columnC = Column("ColonnaC", "TabellaC")
columnA.Add(1)
columnB.Add(2)
tableA = Table("TabellaA", [columnA])
tableB = Table("TabellaB", [columnA, columnB])
fcrA = FieldColumnRelation(fieldA, columnA, 0.5)
fcrB = FieldColumnRelation(fieldB, columnB, 0.5)
fcrC = FieldColumnRelation(fieldC, columnC, 0.5)
pdrA = PageDatabaseRelation(None, [fcrA], 0.5)
pdrB = PageDatabaseRelation(None, [fcrB], 0.5)
pdrC = PageDatabaseRelation(None, [fcrA, fcrB], 0.5)
tprA = TablePageRelation(tableA, pageA)
tprAA = TablePageRelation(tableA, pageA)
tprB = TablePageRelation(tableB, pageB)
tprA.AddRelation(fcrA)
tprAA.AddRelation(fcrA)
tprB.AddRelation(fcrB)
tprB.AddRelation(fcrC)
stringA = "mountainbike"
stringB = "Ezechiele"
stringA = "GioVanNi:2_sfd"
stringB = SplitCamelCase("Gi o Van Ni1")
stringA = SplitCamelCase(stringA)
stringA = SplitSeparators(stringA)
stringC = SplitSeparators("Giov*Anni")

"""
dl_string_comp = DamerauLevenshteinStringComparer()
jw_string_comp = JaroWinklerStringComparer()
ed_string_comp = EditDistanceStringComparer()
w2vec_util = Word2VecUtilities()
w2vec_comp_true = Word2VecComparer(True)
w2vec_comp_false = Word2VecComparer(False)
stringB = "ice_water"
stringA = "dog_duck"
test1 = w2vec_util.GetClosestWords(stringA)
syn_string_comp = SynonymStringComparer()
syn_string_comp_value_1 = syn_string_comp.StringSimilarity(stringA, stringB)
syn_string_comp_value_2 = syn_string_comp.StringSimilarity2(stringA, stringB)
ed_string_comp_value = ed_string_comp.StringSimilarity(stringA, stringB)
w2vec_comp_res_true = w2vec_comp_true.StringSimilarity(stringB, stringA)
w2vec_comp_res_false = w2vec_comp_false.StringSimilarity(stringB, stringA)
jw_string_comp_value = jw_string_comp.StringSimilarity(stringA, stringB)
dl_string_comp_value = dl_string_comp.StringSimilarity(stringA, stringB)

print("Value synonym old = " + str(syn_string_comp_value_2))
print("Value synonym new = " + str(syn_string_comp_value_1))
print("Value w2vec_True StringComp = " + str(w2vec_comp_res_true))
print("Value w2vec_false StringComp = " + str(w2vec_comp_res_false))

"""
print("Value EditDistance = " + str(ed_string_comp_value))
print("Value w2vec_True StringComp = " + str(w2vec_comp_res_true))
print("Value w2vec_false StringComp = " + str(w2vec_comp_res_false))
print("Value JW string comp = " + str(jw_string_comp_value))
print("Value DL string comp = " + str(dl_string_comp_value))

# Comparers

max_composed_sc = MaxComposedStringComparer()
max_composed_sc.AddComparer(w2vec_comp_true)
max_composed_sc.AddComparer(w2vec_comp_false)
max_composed_sc.AddComparer(jw_string_comp)
max_composed_sc.AddComparer(dl_string_comp)
max_composed_sc.AddComparer(ed_string_comp)
max_composed_sc.AddComparer(syn_string_comp)

mean_composed_sc = MeanComposedStringComparer()
mean_composed_sc.AddComparer(w2vec_comp_true)
mean_composed_sc.AddComparer(w2vec_comp_false)
mean_composed_sc.AddComparer(jw_string_comp)
mean_composed_sc.AddComparer(dl_string_comp)
mean_composed_sc.AddComparer(ed_string_comp)
mean_composed_sc.AddComparer(syn_string_comp)

#print("Max = " + str(max_composed_sc.StringSimilarity(stringA, stringB)))
#print("Mean = " + str(mean_composed_sc.StringSimilarity(stringA, stringB)))

# Query

default_sql_database_info = DefaultSqlDatabaseInfo()
sql_database_info = SqlDatabaseInfo()
cached_sql_query_engine = CachedMicrosoftSqlQueryEngine(sql_database_info)

#print("Nome tabelle = " +str(cached_sql_query_engine.table_names))
#print("Nome colonne delle tabelle = " + str(cached_sql_query_engine.table_column_names))
#print("Righe: " + str(cached_sql_query_engine.table_rows))

# Database

database_struct_fact = DatabaseStructureFactory(cached_sql_query_engine)
database_struct = database_struct_fact.GetDatabaseStructure()

#print(type(database_struct.tables["customers"]))

#print(database_struct_fact.GetDatabaseStructure().GetTable("customers").ToString())
#print(database_struct_fact.GetDatabaseStructure().GetTable("Tabella1").ToString())

# Webapp

label_customer_name = Label("Name and Surname:")
label_code = Label("Code of the card:")
label_last_purchase_date = Label("Date of the last purchase:")
label_last_purchase_time = Label("Time of the last purchase:")

field_customer_name = Field([label_customer_name])
field_customer_card_code = Field([label_code])
field_customer_last_purchase_info = Field([label_last_purchase_date, label_last_purchase_time])

page_customer_info = Page([field_customer_name, field_customer_card_code, field_customer_last_purchase_info],
                          "www.test.it", "customer's info")
page_customer_info_2 = Page([field_customer_name, field_customer_card_code, field_customer_last_purchase_info])

#print(page_customer_info.ToString())
#print(page_customer_info_2.ToString())
# relationsmaker

relations_maker = DefaultRelationsMaker("MAXSIMILARITY_MAXLABELS_OLD")
relations_results = relations_maker.FindBestMatch(page_customer_info, database_struct)
print(relations_results.GetData(field_customer_name, 1))
for element in relations_results.GetRelations():
    print(element.field.ToString() + " - " + element.column.ToString() + " = " + str(element.value))
example_dict = dict()
for relation in relations_results.GetRelations():
    example_dict[relation.field] = relations_results.GetData(relation.field, 1)
print(example_dict)
"""



#exec(open("DBInput\ValuesTests.py").read())