import pytest

from app.domain.chat import ChatMember, ChatName, ChatType, Chat
from app.domain.user import User
from app.domain.chat.exceptions import IncorrectNameError, IncorrectChatMembers

from collections.abc import Callable

class TestChatName:

    @pytest.mark.parametrize("test_name", ["", " ", "aaaaaasddddddddddddddddddddddddddddddddddddddddddddd"])
    def test_valid_chat_name(self, test_name):
        with pytest.raises(IncorrectNameError):
            ChatName(test_name)


class TestChat:

    @pytest.mark.parametrize("chat_name, members", [
        ("test_chat_1", []),
        ("test_chat_2", ["user_1", "user_2", "user_3"])
    ])
    def test_creation_of_direct_chat(self, chat_name: str,
                                     members: list[str],
                                     user_maker: Callable[[str, str, str, int], User],
                                     chat_maker: Callable[[str, set[User], ChatType], Chat]):
        members = {user_maker(username, '1Q2w3e', 'm@m.ru', key) for key, username in enumerate(members)}
        with pytest.raises(IncorrectChatMembers):
            chat_maker(chat_name, members, ChatType.DIRECT)


    def test_add_members_to_direct_chat(self,
                                        user_maker: Callable[[str, str, str, int], User],
                                        chat_maker: Callable[[str, set[User], ChatType], Chat]):
        first_user = user_maker("user_1", "1Q2w3e", "m@mail.ru", 1)
        second_user = user_maker("user_2", "1Q2w3e", "s@mail.ru", 2)
        members = {first_user, second_user}
        chat = chat_maker("test_chat", members, ChatType.DIRECT)

        chat_members = set()
        for member in members:
            chat_members.add(ChatMember.create(member, chat))

        assert chat_members == chat._members