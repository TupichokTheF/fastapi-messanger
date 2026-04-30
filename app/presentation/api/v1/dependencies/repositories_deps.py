from app.presentation.api.v1.dependencies import SessionDep
from app.infrastructure.adapters.repositories import UserRepository, MessageRepo

from typing import Annotated
from fastapi import Depends

def get_user_repository(session: SessionDep):
    return UserRepository(session)

UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]

def get_message_repository(session: SessionDep):
    return MessageRepo(session)

MessageRepoDep = Annotated[MessageRepo, Depends(get_message_repository)]