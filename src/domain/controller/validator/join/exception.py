from exception.base import BackendError


class NotEveryoneJoin(BackendError):
    code = "not_everyone_join"
    description = "Not everyone join"
