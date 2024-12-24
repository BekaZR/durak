from exception.base import BackendError


class GameNotFound(BackendError):
    code = "game_not_found"
    description = "Game not found"


class GameCannotSwitchReady(BackendError):
    code = "game_cannot_switch_ready"
    description = "Game cannot switch ready"


class GameCannotSwitchStart(BackendError):
    code = "game_cannot_switch_start"
    description = "Game cannot switch start"
