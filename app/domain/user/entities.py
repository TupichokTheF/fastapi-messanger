from dataclasses import dataclass

from app.domain.base.entity import BaseEntity
from app.domain.user.value_objects import UserEmail, UserPassword, UserUsername

from bcrypt import checkpw


@dataclass(eq=False)
class User(BaseEntity):
    email: UserEmail
    username: UserPassword
    password: UserUsername

    def verify_password(self, users_password: UserPassword):
        return checkpw(users_password.value.encode("utf-8"), self.password.value.encode("utf-8"))
