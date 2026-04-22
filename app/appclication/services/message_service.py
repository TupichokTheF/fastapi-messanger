from app.infrastructure.adapters.repositories import UserRepositoryDep
from app.infrastructure.websockets.con_manager import ConManagerDep


class MessageService:

    def __init__(self, user_repo: UserRepositoryDep, con_manager: ConManagerDep):
        self._user_repo = user_repo
        self._con_manager = con_manager


