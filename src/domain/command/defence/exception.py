from exception.base import BackendError


class CannotDefenceError(BackendError):
    code = "you_cannot_defence"
    description = "You can`t defence"
