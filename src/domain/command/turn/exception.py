from exception.base import BackendError


class TrumpNotExistsException(BackendError):
    code = "trump_not_exist"
    description = "Trump does not exist"


class TurnNotExistError(BackendError):
    code = "turn_not_exist"
    description = "Turn not exist"


class NeigborsNotExistError(BackendError):
    code = "neigbors_not_exist"
    description = "Neigbors not exist"


class QueueIsBlankError(BackendError):
    code = "queue is blank"
    description = "Queue is blank"


class NotYourTurnError(BackendError):
    code = "not_your_turn"
    description = "Not your turn"
