from exception.base import BackendError


class GameNotFound(BackendError):
    code = "game_not_found"
    description = "Game not found"
