from typing import Annotated

from fastapi import Depends

from app.infrastructure.websockets.con_manager import (
    ConnectionManager,
    connection_manager,
)


def get_connection_manager() -> ConnectionManager:
    return connection_manager

ConManagerDep = Annotated[ConnectionManager, Depends(get_connection_manager)]
