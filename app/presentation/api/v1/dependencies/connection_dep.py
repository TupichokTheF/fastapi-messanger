from app.infrastructure.websockets.con_manager import ConnectionManager

from typing import Annotated
from fastapi import Depends

_connection_manager = ConnectionManager()

def get_connection_manager():
    return _connection_manager

ConManagerDep = Annotated[ConnectionManager, Depends(get_connection_manager)]