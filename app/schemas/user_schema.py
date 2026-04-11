from pydantic import BaseModel, Field, field_validator, ConfigDict, EmailStr


class UserBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    user_id: int

class PasswordValidator(BaseModel):
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, password_: str):
        if password_.upper() == password_:
            raise ValueError('Треубется хотя бы одна буква в нижнем регистре')
        if password_.lower() == password_:
            raise ValueError('Треубется хотя бы одна буква в верхнем регистре')
        if not any(symbol.isdigit() for symbol in password_):
            raise ValueError('Треубется хотя бы одна цифра')
        return password_

class UserSignUp(PasswordValidator):
    username: str = Field(min_length=6, max_length=20)
    email: EmailStr

class UserSignIn(PasswordValidator):
    username: str
