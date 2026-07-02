from app.domain import DomainError

class ValidationError(DomainError):
    pass

class InvalidArgument(DomainError):
    pass

class ChatAccessDenied(DomainError):
    pass