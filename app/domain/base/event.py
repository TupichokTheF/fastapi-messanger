from abc import ABC

from dataclasses import dataclass, asdict

@dataclass(kw_only=True, eq=True)
class BaseEvent(ABC):


    def as_dict(self):
        return asdict(self)

