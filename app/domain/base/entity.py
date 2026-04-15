from abc import ABC
from dataclasses import dataclass


@dataclass(eq=False)
class BaseEntity(ABC):
    id: int

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)