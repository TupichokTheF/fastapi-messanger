from collections.abc import Callable

import pytest

from app.domain.user import User, UserEmail, UserUsername
from app.domain.user.exceptions import InvalidArgument, ValidationError


class TestUsername:


    @pytest.mark.parametrize("invalid_username", ["abc", "1q2w", "aaSFSAFsaDSAdcacsacwacxaa"])
    def test_validation_of_username(self, invalid_username):
        with pytest.raises(ValidationError):
            UserUsername(invalid_username)

    def test_username_equality(self):
        username_1 = UserUsername("MaximTheFucker")
        username_2 = UserUsername("MaximTheSucker")
        username_3 = UserUsername("MaximTheFucker")

        assert username_1 == username_3
        assert username_1 != username_2

class TestUserEmail:

    @staticmethod
    def create_email(value: str):
        email = UserEmail(value)
        return email

    @pytest.mark.parametrize("invalid_email", ["lolol", "kek1213@", "kek@mail", "kek@mail."])
    def test_validation_of_email(self, invalid_email):
        with pytest.raises(ValidationError):
            UserEmail(invalid_email)

    def test_email_equality(self):
        email_1 = UserEmail("Maks@mail.ru")
        email_2 = UserEmail("maks@mail.ru")
        email_3 = UserEmail("mak@mail.ru")

        assert email_1 == email_2
        assert email_1 != email_3

class TestUser:

    def test_user_equality(self, user_maker: Callable[[str, str, str, int], User]):
        user1 = user_maker("test12345", "1Q2w3e", "maks1@mail.ru", 1)
        user2 = user_maker("test23456", "1Q2w3e", "maks2@mail.ru", 2)
        user3 = user_maker("test12345", "1Q2w3e", "maks1@mail.ru", 1)

        assert user1 != user2
        assert user1 == user3

    @pytest.mark.parametrize("username, password, email, id",[
                             ("", "1q2w3e", "dasd@mail.ru", 1),
                             ("ssdadwad", "", "dasd@mail.ru", 1),
                             ("dawdwda", "1q2w3e", "", 1)])
    def test_user_creation(self, username: str,
                           password: str,
                           email: str,
                           id: int,
                           user_maker: Callable[[str, str, str, int], User]):
        with pytest.raises(InvalidArgument):
            user_maker(username, password, email, id)

    def test_dict_view(self, user_maker: Callable[[str, str, str, int], User]):
        user_1 = user_maker("Maxim1", "1Q2w3e", "maks@mail.ru", 1)

        assert user_1.to_dict() == {"username": "Maxim1", "email": "maks@mail.ru", "id": 1}

    def test_password_verification(self, user_maker: Callable[[str, str, str, int], User]):
        user_1 = user_maker("ssdadwad", "1Q2w3e", "dasd@mail.ru", 1)

        assert not user_1.verify_password("")
        assert not user_1.verify_password("sad")
        assert user_1.verify_password("1Q2w3e")

