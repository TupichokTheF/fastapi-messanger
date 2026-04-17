from dataclasses import dataclass

from app.domain.base.entity import BaseEntity
from app.domain.user.value_objects import UserEmail, UserPassword, UserUsername

from bcrypt import checkpw


@dataclass(eq=False, kw_only=True)
class User(BaseEntity):
    _email: UserEmail
    _username: UserUsername
    _password: UserPassword

    def verify_password(self, users_password: str):
        return checkpw(users_password.encode("utf-8"), self.password.encode("utf-8"))

    @property
    def username(self):
        return self._username.value

    @property
    def email(self):
        return self._email.value

    @property
    def password(self):
        return self._password.value
