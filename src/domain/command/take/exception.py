from exception.base import BackendError


class CannotTakeError(BackendError):
    code = "cannot_take"
    description = "You cannot take"
