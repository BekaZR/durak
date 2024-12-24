from exception.base import BackendError


class NotEveryoneReady(BackendError):
    code = "not_everyone_ready"
    description = "Not everyone ready"
