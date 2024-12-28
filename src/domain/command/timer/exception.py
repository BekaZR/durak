from exception.base import BackendError


class TimerNotFound(BackendError):
    code = "timer_not_found"
    description = "Timer not found"


class TimerUserEmptyError(BackendError):
    code = "timer_user_empty"
    description = "Cannot start timer - user is empty"


class TimerTypeNotExitstError(BackendError):
    code = "timer_type_not_exist"
    description = "Timer type not exist"
