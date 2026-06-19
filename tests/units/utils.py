from app.domain.user import User
from app.domain.chat import Chat


def create_user(username: str, password: str, email: str, id_: int) -> User:
    user = User.create(username, email, password)
    user.id = id_
    return user

def create_chat(chat_name: str, chat_type: str, members: set[User]):
    chat = Chat.create(chat_name, members, chat_type)
    return chat