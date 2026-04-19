from fastapi import APIRouter

from app.presentation.api.v1.endpoints import auth_router, message_router, test_router, user_router

api_router = APIRouter(
    prefix="/api/v1"
)
api_router.include_router(auth_router)
api_router.include_router(message_router)
api_router.include_router(test_router)
api_router.include_router(user_router)