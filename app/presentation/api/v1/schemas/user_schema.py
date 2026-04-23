from pydantic import BaseModel, Field


class UserSignUp(BaseModel):
    username: str = Field(min_length=6, max_length=20)
    email: str
    password: str

class UserSignIn(BaseModel):
    username: str
    password: str



