class AuthCheckerException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class RequireAdmin(AuthCheckerException):
    pass


class RequireOwnership(AuthCheckerException):
    pass
