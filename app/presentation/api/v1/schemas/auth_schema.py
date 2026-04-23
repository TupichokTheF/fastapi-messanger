from pydantic import BaseModel

class TokenBase(BaseModel):
    token: str
    token_type: str

class RefreshToken(TokenBase):
    pass

class AccessToken(TokenBase):
    pass

