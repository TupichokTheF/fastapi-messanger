from fastapi import APIRouter, Body
from app.presentation.api.v1.dependencies.auth_dep import AuthorizationDep
from app.presentation.api.v1.dependencies import ChatServiceDep
from app.presentation.api.v1.schemas.responses import AddedToChatResponse, UserChatsResponse

chat_router = APIRouter(
    prefix="/chat",
    tags=["Chat operation"]
)

@chat_router.post("/add_chat", response_model=AddedToChatResponse)
async def add_user_to_contact(user: AuthorizationDep, chat_service: ChatServiceDep, contact_username: str = Body(embed=True)):
    await chat_service.add_to_contact(user, contact_username)
    return AddedToChatResponse(succeed=True, detail="User added to contact")

@chat_router.get("/get_chats", response_model=UserChatsResponse)
async def get_chats(user: AuthorizationDep, chat_service: ChatServiceDep):
    chats = await chat_service.get_chats(user)
    return UserChatsResponse(succeed=True, detail="Spend list of user contacts", chats=chats)


