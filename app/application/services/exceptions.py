
class ApplicationError(Exception):
    pass

class NotFoundError(ApplicationError):
    pass

class WrongPasswordError(ApplicationError):
    pass

class WrongTokenError(ApplicationError):
    pass

class InvalidUsername(ApplicationError):
    pass