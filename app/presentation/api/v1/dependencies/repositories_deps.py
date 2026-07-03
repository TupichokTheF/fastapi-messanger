from typing import Annotated

from fastapi import Depends

from app.infrastructure.adapters.repositories import (
    ChatRepository,
    MessageRepository,
    UserRepository,
)
from app.presentation.api.v1.dependencies.session_dep import SessionDep


def get_user_repository(session: SessionDep):
    return UserRepository(session)

def get_message_repository(session: SessionDep):
    return MessageRepository(session)

def get_chat_repository(session: SessionDep):
    return ChatRepository(session)

UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
MessageRepoDep = Annotated[MessageRepository, Depends(get_message_repository)]
ChatRepoDep = Annotated[ChatRepository, Depends(get_chat_repository)]
