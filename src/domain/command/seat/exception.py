from exception.base import BackendError


class SeatPositionException(BackendError):
    code = "seat_position_invalid"
    description = "Seat position is invalid"


class SeatNotExist(BackendError):
    code = "seat_not_exist"
    description = "Seat not exist"
