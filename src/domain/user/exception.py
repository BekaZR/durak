from exception.base import BackendError


class DefenderNotFound(BackendError):
    code = "defender_not_found"
    description = "Defender not found"


class AttackerNotFound(BackendError):
    code = "defender_not_found"
    description = "Defender not found"
