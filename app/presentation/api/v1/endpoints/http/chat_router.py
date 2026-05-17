from fastapi import APIRouter, Body, HTTPException, status
from app.presentation.api.v1.dependencies.auth_dep import AuthorizationDep
from app.presentation.api.v1.dependencies import ChatServiceDep
from app.presentation.api.v1.schemas.responses import AddedToChatResponse, UserChatsResponse

chat_router = APIRouter(
    prefix="/chat",
    tags=["Chat operation"]
)

@chat_router.post(path="/add_direct_chat", response_model=AddedToChatResponse)
async def add_user_to_contact(user: AuthorizationDep, chat_service: ChatServiceDep, contact_username: str = Body(embed=True)):
    try:
        await chat_service.add_to_direct_chat(user, contact_username)
        return AddedToChatResponse(succeed=True, detail="User added to contact")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

@chat_router.get(path="/get_chats", response_model=UserChatsResponse)
async def get_chats(user: AuthorizationDep, chat_service: ChatServiceDep):
    chats = await chat_service.get_chats(user)
    return UserChatsResponse(succeed=True, detail="Spend previews of user chats", chats=chats)


