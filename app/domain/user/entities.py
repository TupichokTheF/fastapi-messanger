from dataclasses import dataclass

from bcrypt import checkpw

from app.domain.base.entity import BaseEntity
from app.domain.user.exceptions import InvalidArgument
from app.domain.user.value_objects import UserEmail, UserPassword, UserUsername


@dataclass(eq=False, kw_only=True)
class User(BaseEntity):
    _email: UserEmail
    _username: UserUsername
    _password: UserPassword

    def verify_password(self, users_password: str):
        if not users_password:
            return False
        return checkpw(users_password.encode("utf-8"), self.password.encode("utf-8"))

    def to_dict(self) -> dict:
        info = super().to_dict()
        info.pop("_password")
        info["email"] = info["_email"]["value"]
        info["username"] = info["_username"]["value"]
        info.pop("_email")
        info.pop("_username")
        return info

    @property
    def username(self):
        return self._username.value

    @property
    def email(self):
        return self._email.value

    @property
    def password(self):
        return self._password.value

    @property
    def raw_username(self):
        return self._username

    @staticmethod
    def create(username: str, email: str, password: str):
        if not all((username, email, password)):
            raise InvalidArgument("Entered empty argument")
        username = UserUsername(username)
        email = UserEmail(email)
        password = UserPassword.create(password)
        return User(_username=username,
                    _email=email,
                    _password=password)
