from enum import StrEnum


class GameStatus(StrEnum):
    STARTED = "started"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"
