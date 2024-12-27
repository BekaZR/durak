from exception.base import BackendError


class CantBeatError(BackendError):
    code = "cannot_beat"
    description = "You can`t beat"


class SlotIDOutOfRangeError(BackendError):
    code = "slot_id_out_of_range"
    description = "Slot ID out of range"


class SlotAlreadyClosedError(BackendError):
    code = "slot_already_closed"
    description = "Slot already closed"
