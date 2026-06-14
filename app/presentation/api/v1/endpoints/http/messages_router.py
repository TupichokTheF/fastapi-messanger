from fastapi import APIRouter

from app.presentation.api.v1.dependencies import AuthorizationDep, MessageServiceDep


messages_router = APIRouter(
    tags = ["HTTP operations with messages"],
    prefix = "/message"
)


@messages_router.get("/get_latest")
async def get_latest_messages(current_user: AuthorizationDep, messages_service: MessageServiceDep):
    latest_messages = await messages_service.get_latest_messages(current_user)