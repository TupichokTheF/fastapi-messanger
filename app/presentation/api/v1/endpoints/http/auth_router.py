from fastapi import APIRouter, Response, HTTPException, status, Cookie

from app.presentation.api.v1.dependencies import UserServiceDep, AuthServiceDep, JWTServiceDep
from app.application.services.exceptions import NotFoundError
from app.application.dtos.user_dto import UserSignUpDTO
from app.presentation.api.v1.schemas.user_schema import UserSignUp, UserSignIn
from app.presentation.api.v1.schemas.auth_schema import AccessToken
from app.presentation.api.v1.schemas.responses import SignUpResponse

import logging


auth_router = APIRouter(
    tags=["Auth endpoints"],
    prefix="/auth"
)

logger = logging.getLogger("chat_app")

@auth_router.post(path="/sign_up", response_model=SignUpResponse)
async def create_user(user_service: UserServiceDep, user_data: UserSignUp):
    user_dto = UserSignUpDTO(**user_data.model_dump())
    user_id = await user_service.create_user(user_dto)

    logger.info(f"User created  | user_id={user_id}", extra={"user_id": user_id})
    return SignUpResponse(id=user_id, succeed=True, detail="User successfully added")


@auth_router.post(path="/sign_in", response_model=AccessToken)
async def authenticate_user(auth_service: AuthServiceDep, jwt_service: JWTServiceDep, user_data: UserSignIn, response: Response):
    try:
        user = await auth_service.authenticate_user(user_data.username, user_data.password)
    except Exception:
        logger.warning(f"Failed authorization | username={user_data.username}", extra={"username": user_data.username})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = await jwt_service.generate_token({"sub": user.username})
    refresh_token = await jwt_service.generate_refresh_token({"sub": user.username})
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        max_age=24 * 60 * 60
    )

    logger.info(f"Authorization succeed | username={user.username}", extra={"username": user.username})
    return AccessToken(token=access_token, token_type="bearer")


@auth_router.post(path="/refresh", response_model=AccessToken)
async def check_auth(jwt_service: JWTServiceDep, refresh_token: str = Cookie()):
    try:
        new_access_token = await jwt_service.refresh_access_token(refresh_token)
    except NotFoundError as exc:
        logger.warning("Failed refresh token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc)
        )

    logger.info("Token was refreshed")
    return AccessToken(token=new_access_token, token_type="bearer")