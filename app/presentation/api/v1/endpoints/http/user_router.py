from fastapi import APIRouter

from app.presentation.api.v1.dependencies import AuthorizationDep
from app.presentation.api.v1.schemas.responses import UserInfoResponse

user_router = APIRouter(
    tags=["Operations with users"],
    prefix="/user"
)

@user_router.get("/me", response_model=UserInfoResponse)
async def get_user_info(current_user: AuthorizationDep):
    return UserInfoResponse(succeed=True, detail="Returning user info", info=current_user.to_dict())
