from exception.base import BackendError


class CantBeatError(BackendError):
    code = "cannot_beat"
    description = "You can`t beat"
