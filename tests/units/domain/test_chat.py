import pytest

from app.domain.chat import ChatMember, ChatName
from app.domain.chat.exceptions import IncorrectNameError, IncorrectChatMembers

from tests.units.utils import create_chat, create_user

class TestChatName:

    @pytest.mark.parametrize("test_name", ["", " ", "aaaaaasddddddddddddddddddddddddddddddddddddddddddddd"])
    def test_valid_chat_name(self, test_name):
        with pytest.raises(IncorrectNameError):
            ChatName(test_name)


class TestChat:

    @pytest.mark.parametrize("chat_name, chat_type, members", [
        ("test_chat_1", "direct", []),
        ("test_chat_2", "direct", ["user_1", "user_2", "user_3"])
    ])
    def test_creation_of_chat(self, chat_name: str, chat_type: str, members: list[str]):
        members = {create_user(username, '1Q2w3e', 'm@m.ru', key) for key, username in enumerate(members)}
        with pytest.raises(IncorrectChatMembers):
            create_chat(chat_name, chat_type, members)


    def test_add_members(self):
        first_user = create_user("user_1", "1Q2w3e", "m@mail.ru", 1)
        second_user = create_user("user_2", "1Q2w3e", "s@mail.ru", 2)
        members = {first_user, second_user}
        chat = create_chat("test_chat", "DIRECT", members)

        chat_members = set()
        for member in members:
            chat_members.add(ChatMember.create(member, chat))

        assert chat_members == chat._members