from fastapi import APIRouter
from fastapi.params import Depends

from app.core.schemas.message_schema import MessageBase
from app.infrastructure.adapters.repositories.message_repository import MessageRepo
from app.infrastructure.adapters.repositories.user_repository import UserRepositoryDep

message_router = APIRouter(
    prefix="/message"
)

@message_router.post("/create")
async def create_message(message: MessageBase, user_repo: UserRepositoryDep, mes_repo: MessageRepo = Depends(MessageRepo)):
    user = await user_repo.get_user_by_username(message.spender)
    message.spender = user
    await mes_repo.add_message(message)
    return "class"
