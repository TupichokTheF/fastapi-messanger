
class ApplicationError(Exception):
    pass

class NotFoundError(ApplicationError):
    pass

class WrongPasswordError(ApplicationError):
    pass