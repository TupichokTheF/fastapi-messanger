from dataclasses import asdict, dataclass, field

from app.domain.user import User


@dataclass(kw_only=True)
class UserDTO:
    id: int = field(default=None)
    username: str
    email: str

    @classmethod
    def from_entity(cls, user: User):
        return cls(id=user.id, username=user.username, email=user.email)

    def to_dict(self):
        return asdict(self)

@dataclass(kw_only=True)
class UserSignUpDTO(UserDTO):
    password: str = field(default=None)

    @classmethod
    def from_entity(cls, user: User):
        user_base = super().from_entity(user)
        return user_base

    def to_entity(self):
        return User.create(self.username, self.email, self.password)
