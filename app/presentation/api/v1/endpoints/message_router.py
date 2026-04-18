from fastapi import APIRouter
from app.core.schemas.message_schema import MessageBase
from app.infrastructure.adapters.repositories.message_repository import MessageRepo
from app.infrastructure.adapters.repositories.user_repository import UserRepositoryDep

message_router = APIRouter(
    prefix="/message"
)

@message_router.post("/create")
async def create_message(message: MessageBase, user_repo: UserRepositoryDep):
    pass