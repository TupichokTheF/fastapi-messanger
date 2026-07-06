from app.infrastructure.websockets.con_manager import ConnectionManager

from typing import Annotated
from fastapi import Depends

def get_connection_manager() -> ConnectionManager:
    return ConnectionManager()

ConManagerDep = Annotated[ConnectionManager, Depends(get_connection_manager)]