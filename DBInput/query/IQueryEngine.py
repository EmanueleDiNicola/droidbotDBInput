class IQueryEngine:
    def GetTableNames(self):
        # return table names
        pass

    def GetTableColumnNames(self, table_name):
        # return column names of specified table
        pass

    def GetRows(self, table_name, max_number_of_rows):
        # return max_number_of_rows of table table_name
        pass