from abc import ABC
from dataclasses import dataclass
from typing import Optional


@dataclass(eq=False, kw_only=True)
class BaseEntity(ABC):
    id: Optional[int] = None

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)