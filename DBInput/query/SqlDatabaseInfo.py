from typing import Any


class SqlDatabaseInfo:

    def __init__(self):
        self.driver = "{ODBC Driver 17 for SQL Server}"
        self.server = "DESKTOP-FQM5DAJ"
        self.database = "test"
        self.uid = "root"
        self.pwd = "password"

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)