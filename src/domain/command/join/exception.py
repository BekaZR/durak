from exception.base import BackendError


class UserAlreadyJoinError(BackendError):
    code = "user_already_join"
    description = "User already join"
