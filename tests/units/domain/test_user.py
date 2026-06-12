import pytest

from app.domain.user import User, UserUsername, UserEmail
from app.domain.user.exceptions import ValidationError, InvalidArgument
from .utils import create_user


class TestUsername:

    @staticmethod
    def create_username(value: str):
        username = UserUsername(value)
        return username

    @pytest.mark.parametrize("invalid_username", ["abc", "1q2w", "aaSFSAFsaDSAdcacsacwacxaa"])
    def test_validation_of_username(self, invalid_username):
        with pytest.raises(ValidationError):
            self.create_username(invalid_username)

    def test_username_equality(self):
        username_1 = self.create_username("MaximTheFucker")
        username_2 = self.create_username("MaximTheSucker")
        username_3 = self.create_username("MaximTheFucker")

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
            self.create_email(invalid_email)

    def test_email_equality(self):
        email_1 = self.create_email("Maks@mail.ru")
        email_2 = self.create_email("maks@mail.ru")
        email_3 = self.create_email("mak@mail.ru")

        assert email_1 == email_2
        assert email_1 != email_3

class TestUser:

    def test_user_equality(self):
        user1 = self.user_create("test12345", "1Q2w3e", "maks1@mail.ru", 1)
        user2 = self.user_create("test23456", "1Q2w3e", "maks2@mail.ru", 2)
        user3 = self.user_create("test12345", "1Q2w3e", "maks1@mail.ru", 1)

        assert user1 != user2
        assert user1 == user3

    @pytest.mark.parametrize("username, password, email, id",[
                             ("", "1q2w3e", "dasd@mail.ru", 1),
                             ("ssdadwad", "", "dasd@mail.ru", 1),
                             ("dawdwda", "1q2w3e", "", 1)])
    def test_user_creation(self, username: str, password: str, email: str, id: int):
        with pytest.raises(InvalidArgument):
            self.user_create(username, password, email, id)

    def test_dict_view(self):
        user_1 = self.user_create("Maxim1", "1Q2w3e", "maks@mail.ru", 1)

        assert user_1.to_dict() == {"username": "Maxim1", "email": "maks@mail.ru", "id": 1}

    def test_password_verification(self):
        user_1 = self.user_create("ssdadwad", "1Q2w3e", "dasd@mail.ru", 1)

        assert user_1.verify_password("") == False
        assert user_1.verify_password("sad") == False
        assert user_1.verify_password("1Q2w3e")

