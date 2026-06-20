import pytest

from ..utils import create_user

from app.application.dtos import UserDTO, UserSignUpDTO

class TestUserDTO:

    def test_creation_from_entity(self):
        first_user = create_user("test_username", "1Q2w3e", "m@mail.ru", 1)
        user_signup_dto = UserSignUpDTO.from_entity(first_user)
        expected_fields = {"username", "password", "email", "id"}

        assert user_signup_dto.to_dict().keys() & expected_fields
        assert user_signup_dto.password is not None