from fastapi import APIRouter

from app.presentation.api.v1.endpoints import auth_router, chat_router

api_router = APIRouter(
    prefix="/api/v1"
)
api_router.include_router(auth_router)
#api_router.include_router(messages_router)
#api_router.include_router(messages_ws)
api_router.include_router(chat_router)