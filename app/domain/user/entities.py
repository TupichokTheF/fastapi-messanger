from dataclasses import dataclass
from datetime import datetime

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

    @property
    def raw_username(self):
        return self._username

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
    _created_at: datetime = datetime.now()

    @property
    def user(self):
        return self._user

    @property
    def contact(self):
        return self._contact

    @property
    def created_at(self):
        return self._created_at

    @staticmethod
    def create(user: User, contact: User):
        return Contact(_user=user, _contact=contact)