from typing import Annotated

from fastapi import Depends

from app.application.services import (
    AuthService,
    ChatService,
    JWTService,
    MessageService,
    UserService,
)
from app.presentation.api.v1.dependencies.cache_deps import (
    ChatCacheDep,
    MessageCacheDep,
    TokenCacheDep,
)
from app.presentation.api.v1.dependencies.repositories_deps import (
    ChatRepoDep,
    MessageRepoDep,
    UserRepositoryDep,
)


def get_jwt_service(token_cache: TokenCacheDep):
    return JWTService(token_cache)

JWTServiceDep = Annotated[JWTService, Depends(get_jwt_service)]

def get_user_service(user_repo: UserRepositoryDep):
    return UserService(user_repo)

def get_chat_service(user_repo: UserRepositoryDep, chats_repo: ChatRepoDep, chats_cache: ChatCacheDep):
    return ChatService(user_repo, chats_repo, chats_cache)

def get_auth_service(user_repo: UserRepositoryDep, token_cache: TokenCacheDep, jwt_service: JWTServiceDep):
    return AuthService(user_repo, token_cache, jwt_service)

def get_message_service(message_repo: MessageRepoDep,
                        user_repo: UserRepositoryDep,
                        chat_cache: ChatCacheDep,
                        chat_repo: ChatRepoDep,
                        message_cache: MessageCacheDep):
    return MessageService(message_repo, user_repo, chat_cache, chat_repo, message_cache)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]
MessageServiceDep = Annotated[MessageService, Depends(get_message_service)]
