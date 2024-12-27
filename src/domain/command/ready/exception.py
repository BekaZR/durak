from exception.base import BackendError


class UserAlreadyReadyError(BackendError):
    code = "user_already_ready"
    description = "User already ready"
