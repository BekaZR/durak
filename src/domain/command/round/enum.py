from enum import StrEnum


class RoundEnum(StrEnum):
    BEAT = "beat"
    TAKE = "take"
    PROCESSING = "processing"


class RoundState(StrEnum):
    FIRST = "first"
    OTHER = "other"
