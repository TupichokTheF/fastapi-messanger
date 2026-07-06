from app.infrastructure.websockets.con_manager import connection_manager, ConnectionManager

from typing import Annotated
from fastapi import Depends

def get_connection_manager() -> ConnectionManager:
    return connection_manager

ConManagerDep = Annotated[ConnectionManager, Depends(get_connection_manager)]