from app.presentation.api.v1.dependencies import SessionDep, RedisDep
from app.infrastructure.adapters.repositories import UserRepository, TokenRepository, MessageRepo

from typing import Annotated
from fastapi import Depends

def get_user_repository(session: SessionDep):
    return UserRepository(session)

def get_token_repository(redis: RedisDep):
    return TokenRepository(redis)

UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
TokenRepositoryDep = Annotated[TokenRepository, Depends(get_token_repository)]

def get_message_repository(session: SessionDep):
    return MessageRepo(session)

MessageRepoDep = Annotated[MessageRepo, Depends(get_message_repository)]