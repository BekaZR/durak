from exception.base import BackendError


class TrumpNotExistsException(BackendError):
    code = "trump_not_exist"
    description = "Trump does not exist"
