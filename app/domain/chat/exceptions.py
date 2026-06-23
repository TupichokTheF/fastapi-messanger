from app.domain.base import DomainError


class IncorrectNameError(DomainError):
    pass

class UserAlreadyAdded(DomainError):
    pass

class IncorrectChatMembers(DomainError):
    pass

class ChatAccessDenied(DomainError):
    pass