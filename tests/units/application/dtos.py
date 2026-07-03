from collections.abc import Callable

from app.application.dtos import UserSignUpDTO
from app.domain.user import User


class TestUserDTO:

    def test_creation_from_entity(self, user_maker: Callable[[str, str, str, int], User]):
        first_user = user_maker("test_username", "1Q2w3e", "m@mail.ru", 1)
        user_signup_dto = UserSignUpDTO.from_entity(first_user)
        expected_fields = {"username", "password", "email", "id"}

        assert user_signup_dto.to_dict().keys() & expected_fields
        assert user_signup_dto.password is not None
