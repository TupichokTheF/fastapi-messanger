from app.domain.base import DomainError


class IncorrectNameError(DomainError):
    pass

class UserAlreadyAdded(DomainError):
    pass