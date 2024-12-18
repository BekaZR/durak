from exception.base import BackendError


class TimerNotFound(BackendError):
    code = "timer_not_found"
    description = "Timer not found"
