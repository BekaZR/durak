from exception.base import BackendError


class TrumpNotExistsException(BackendError):
    code = "trump_not_exist"
    description = "Trump does not exist"


class TurnNotExistError(BackendError):
    code = "turn_not_exist"
    description = "Turn not exist"
