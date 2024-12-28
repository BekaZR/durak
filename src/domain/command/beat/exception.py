from exception.base import BackendError


class DefenderCannotBeatError(BackendError):
    code = "defender_cannot_beat"
    description = "Defender cannot beat"
