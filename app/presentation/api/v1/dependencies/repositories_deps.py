from app.presentation.api.v1.dependencies import SessionDep
from app.infrastructure.adapters.repositories import UserRepository, MessageRepository, ChatRepository

from typing import Annotated
from fastapi import Depends

def get_user_repository(session: SessionDep):
    return UserRepository(session)

def get_message_repository(session: SessionDep):
    return MessageRepository(session)

def get_chat_repository(session: SessionDep):
    return ChatRepository(session)

UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
MessageRepoDep = Annotated[MessageRepository, Depends(get_message_repository)]
ChatRepoDep = Annotated[ChatRepository, Depends(get_chat_repository)]