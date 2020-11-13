from typing import Any


class ObjectComparer:
    def __init__(self, l1, l2, similarity):
        self.l1 = l1
        self.l2 = l2
        self.similarity = similarity

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

