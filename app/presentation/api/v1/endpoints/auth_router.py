from fastapi import APIRouter, Response, HTTPException, status

from app.appclication.services.user_service import UserServiceDep
from app.core.schemas.user_schema import UserSignUp, UserSignIn
from app.core.schemas.auth_schema import AccessToken
from app.presentation.api.v1.responses import SignUpResponse
from app.core.auth_dep import AuthorizationDep

auth_router = APIRouter(
    tags=["Auth endpoints"],
    prefix="/auth"
)

@auth_router.post("/sign_up", response_model=SignUpResponse)
async def create_user(user_service: UserServiceDep, user_data: UserSignUp):
    user_id = await user_service.create_user(user_data)
    return SignUpResponse(id=user_id, succeed=True, detail="User successfully added")

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


@auth_router.get("/test")
async def check_auth(cur_user: AuthorizationDep):
    return cur_user