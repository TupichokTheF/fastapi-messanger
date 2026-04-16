from dataclasses import dataclass

from app.domain.base.entity import BaseEntity
from app.domain.user.value_objects import UserEmail, UserPassword, UserUsername

from bcrypt import checkpw


@dataclass(eq=False, kw_only=True)
class User(BaseEntity):
    email: UserEmail
    username: UserUsername
    password: UserPassword

    def verify_password(self, users_password: str):
        return checkpw(users_password.encode("utf-8"), self.password.value.encode("utf-8"))
