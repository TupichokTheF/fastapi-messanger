from dataclasses import dataclass
import re
from bcrypt import hashpw, gensalt

from app.domain.base.value_object import BaseValueObject

EMAIL_REGEXP = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

@dataclass(frozen=True)
class UserEmail(BaseValueObject):
    value: str

    def __post_init__(self):
        clean_email = self.value.strip().lower()
        object.__setattr__(self, 'value', clean_email)
        if not re.match(EMAIL_REGEXP, self.value):
            raise ValueError(f"Некорректный формат email: {self.value}")


@dataclass(frozen=True)
class UserPassword(BaseValueObject):
    value: str

    @classmethod
    def create(cls, raw_password: str):
        if raw_password.upper() == raw_password:
            raise ValueError('Требуется хотя бы одна буква в нижнем регистре')
        if raw_password.lower() == raw_password:
            raise ValueError('Требуется хотя бы одна буква в верхнем регистре')
        if not any(symbol.isdigit() for symbol in raw_password):
            raise ValueError('Требуется хотя бы одна цифра')

        hashed_password = hashpw(raw_password.encode("utf-8"), gensalt()).decode("utf-8")
        return cls(hashed_password)


@dataclass(frozen=True)
class UserUsername(BaseValueObject):
    value: str

    def __post_init__(self):
        if len(self.value) < 6:
            raise ValueError('Слишком короткий логин!')
        if len(self.value) > 20:
            raise ValueError('Слишком длинный логин!')