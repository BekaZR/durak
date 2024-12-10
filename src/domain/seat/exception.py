from exception.base import BackendError


class SeatPositionException(BackendError):
    code = "seat_position_invalid"
    description = "Seat position is invalid"
