from exception.base import BackendError


class RoomNotFound(BackendError):
    def __init__(self, extra_info: str | None = None) -> None:
        self.extra_info = extra_info

    code = "room_not_found"
    description = "Room not found"
