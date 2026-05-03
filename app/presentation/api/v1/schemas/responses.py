import datetime

from pydantic import BaseModel
from app.domain.user.value_objects import UserUsername

class BaseResponse(BaseModel):
    succeed: bool = False
    detail: str

class SignUpResponse(BaseResponse):
    id: int

class AddedToChatResponse(BaseResponse):
    pass

class UserChatsResponse(BaseResponse):
    chats: list

class ErrorResponse(BaseResponse):
    pass

class MessageSendResponse(BaseResponse):
    created_at: datetime.datetime

class MessageToSend(BaseModel):
    text: str
    spender: str
    created_at: datetime.datetime