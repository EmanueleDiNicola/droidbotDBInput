from typing import Any

from DBInput.query.SqlDatabaseInfo import SqlDatabaseInfo


class DefaultSqlDatabaseInfo:
    def __init__(self):
        self.default_info = SqlDatabaseInfo()

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

