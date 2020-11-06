from DBInput.database.Column import Column
from DBInput.database.Table import Table
from DBInput.relations.FieldColumnRelation import FieldColumnRelation
from DBInput.relations.PageDatabaseRelation import PageDatabaseRelation
from DBInput.relations.TablePageRelation import TablePageRelation
from DBInput.relations.fieldcolumncomparer.stringcomparer.DamerauLevenshteinStringComparer import \
    DamerauLevenshteinStringComparer
from DBInput.relations.fieldcolumncomparer.stringcomparer.EditDistanceStringComparer import EditDistanceStringComparer
from DBInput.relations.fieldcolumncomparer.stringcomparer.JaroWinklerStringComparer import JaroWinklerStringComparer
from DBInput.relations.fieldcolumncomparer.stringcomparer.Tokenizer import SplitCamelCase, SplitSeparators
from DBInput.webapp.Field import Field
from DBInput.webapp.Label import Label
from DBInput.webapp.Page import Page
from DBInput.relations.fieldcolumncomparer.StringTransformation import CleanString

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
dl_string_comp = DamerauLevenshteinStringComparer()
dl_string_comp_value = dl_string_comp.StringSimilarity(stringA, stringB)
jw_string_comp = JaroWinklerStringComparer()
jw_string_comp_value = jw_string_comp.StringSimilarity(stringA, stringB)
stringA = "GioVanNi"
stringB = SplitCamelCase("Gi o Van Ni1")
stringA = SplitCamelCase(stringA)
stringC = SplitSeparators("Giov*Anni")
stringA = "CiaoCiaoCiaoCiao"
stringB = "fjfjfjfjfjfjfAfFFFFAaas"
edsc = EditDistanceStringComparer()
test20 = edsc.Functtest(stringA, stringB)
print(test20)
test0 = edsc.Diff(stringA, stringB)
print(test0)
test1 = edsc.GetEditDistance(stringA, stringB)
print(test1)
test2 = edsc.StringSimilarity(stringA, stringB)
print(test2)

#Da testare tutto stringcomparer per bene
#exec(open("DBInput\ValuesTests.py").read())