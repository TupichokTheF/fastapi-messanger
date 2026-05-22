import datetime

from pydantic import BaseModel


class BaseResponse(BaseModel):
    succeed: bool = False
    detail: str

class SignUpResponse(BaseResponse):
    id: int

class AddedToChatResponse(BaseResponse):
    pass

class UserChatsResponse(BaseResponse):
    chats: list[dict]

class ErrorResponse(BaseResponse):
    pass

class MessageSendResponse(BaseResponse):
    created_at: datetime.datetime

class MessageToSend(BaseModel):
    text: str
    spender: str
    created_at: datetime.datetime

class UserInfoResponse(BaseResponse):
    info: dict