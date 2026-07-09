from dataclasses import dataclass, asdict


@dataclass(kw_only=True)
class FilterParamsDTO:
    offset: int
    limit: int

    def as_dict(self):
        return asdict(self)