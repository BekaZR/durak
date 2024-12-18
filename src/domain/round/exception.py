from exception.base import BackendError


class RoundNotExistError(BackendError):
    code = "round_not_exist"
    description = "Round not exist"
