from app.application.services import JWTService, UserService, AuthService, MessageService
from app.presentation.api.v1.dependencies import UserRepositoryDep, MessageRepoDep, TokenCacheDep, ContactsCacheDep, MessagesCacheDep

from typing import Annotated
from fastapi import Depends

def get_jwt_service(token_cache: TokenCacheDep):
    return JWTService(token_cache)

JWTServiceDep = Annotated[JWTService, Depends(get_jwt_service)]

def get_user_service(user_repo: UserRepositoryDep, contacts_cache: ContactsCacheDep):
    return UserService(user_repo, contacts_cache)

def get_auth_service(user_repo: UserRepositoryDep, token_cache: TokenCacheDep, jwt_service: JWTServiceDep):
    return AuthService(user_repo, token_cache, jwt_service)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

def get_message_service(message_repo: MessageRepoDep,
                        user_repo: UserRepositoryDep,
                        contacts_cache: ContactsCacheDep,
                        user_service: UserServiceDep,
                        messages_cache: MessagesCacheDep):
    return MessageService(message_repo, user_repo, contacts_cache, user_service, messages_cache)

MessageServiceDep = Annotated[MessageService, Depends(get_message_service)]