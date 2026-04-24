import datetime

from pydantic import BaseModel
from app.domain.user.value_objects import UserUsername

class BaseResponse(BaseModel):
    succeed: bool = False
    detail: str

class SignUpResponse(BaseResponse):
    id: int

class AddedToContactResponse(BaseResponse):
    pass

class UserContactsResponse(BaseResponse):
    contacts: list[UserUsername]

class ErrorResponse(BaseResponse):
    pass

class MessageSendResponse(BaseResponse):
    created_at: datetime.datetime

class MessageToSend(BaseModel):
    text: str
    spender: str
    created_at: datetime.datetime