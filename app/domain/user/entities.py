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

    @staticmethod
    def create(username: str, email: str, password: str):
        username = UserUsername(username)
        email = UserEmail(email)
        password = UserPassword.create(password)
        return User(_username=username,
                    _email=email,
                    _password=password)


@dataclass(kw_only=True)
class Contact:
    _user: User
    _contact: User

    @property
    def user(self):
        return self._user

    @property
    def contact(self):
        return self._contact

    @staticmethod
    def create(user: User, contact: User):
        return Contact(_user=user, _contact=contact)