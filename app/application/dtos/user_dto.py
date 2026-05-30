from dataclasses import dataclass, asdict

from app.domain.user import User


@dataclass(kw_only=True)
class UserDTO:
    id: int
    username: str
    email: str

    @classmethod
    def from_entity(cls, user: User):
        return cls(id=user.id, username=user.username, email=user.email)

    def to_dict(self):
        return asdict(self)