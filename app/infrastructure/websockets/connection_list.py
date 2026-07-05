from fastapi import WebSocket

from collections import defaultdict


class ConnectionList:

    def __init__(self):
        self._user_websocket = defaultdict(set)
        self._chat_users = defaultdict(set)

    def get_websockets_by_chat_id(self, chat_id: int) -> set[WebSocket]:
        receivers_websockets = set()
        for user_of_chat in self._chat_users[chat_id]:
            receivers_websockets.add(self._user_websocket[user_of_chat])

        return receivers_websockets

    def get_websocket_by_user_id(self, user_id: int) -> set[WebSocket]:
        return self._user_websocket[user_id]

    def add_user_to_active_connections(self, user_id: int, websocket: WebSocket):
        self._user_websocket[user_id].add(websocket)

    def add_user_to_chats(self, user_id: int, chat_ids: list[int]):
        for chat_id in chat_ids:
            self._chat_users[chat_id].add(user_id)

connection_list = ConnectionList()