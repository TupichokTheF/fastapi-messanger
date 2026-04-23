from app.application.services import JWTService, UserService, AuthService
from app.presentation.api.v1.dependencies import UserRepositoryDep, TokenRepositoryDep

from typing import Annotated
from fastapi import Depends

def get_jwt_service(token_repo: TokenRepositoryDep):
    return JWTService(token_repo)

JWTServiceDep = Annotated[JWTService, Depends(get_jwt_service)]

def get_user_service(user_repo: UserRepositoryDep, token_repo: TokenRepositoryDep):
    return UserService(user_repo, token_repo)

def get_auth_service(user_repo: UserRepositoryDep, token_repo: TokenRepositoryDep, jwt_service: JWTServiceDep):
    return AuthService(user_repo, token_repo, jwt_service)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]