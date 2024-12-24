from re import I
from exception.base import BackendError


class DefenderNotFound(BackendError):
    code = "defender_not_found"
    description = "Defender not found"


class AttackerNotFound(BackendError):
    code = "defender_not_found"
    description = "Defender not found"


class UserNotFound(BackendError):
    code = "user_not_found"
    description = "User not found"


class UserAlreadyWinError(BackendError):
    code = "user already win"
    description = "User already win"
