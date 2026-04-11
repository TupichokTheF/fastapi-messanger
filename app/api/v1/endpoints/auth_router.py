from fastapi import APIRouter, Response, HTTPException, status

from app.services.user_service import UserServiceDep
from app.schemas.user_schema import UserSignUp, UserSignIn
from app.schemas.token_schemas import AccessToken

auth_router = APIRouter(
    tags=["Auth endpoints"],
    prefix="/auth"
)

@auth_router.post("/sign_up")
async def create_user(user_service: UserServiceDep, user_data: UserSignUp):
    return await user_service.create_user(user_data)

@auth_router.post("/sign_in", response_model=AccessToken)
async def authenticate_user(user_service: UserServiceDep, user_data: UserSignIn, response: Response):
    user = await user_service.authenticate_user(user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await user_service.generate_token({"sub": user.username})
    refresh_token = await user_service.generate_refresh_token({"sub": user.username})
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        max_age=24 * 60 * 60
    )
    return AccessToken(token=access_token, token_type="bearer")