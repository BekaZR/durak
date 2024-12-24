from exception.base import BackendError


class StateEmptyError(BackendError):
    code = "state_empty"
    description = "State is empty"


class StateValidationError(BackendError):
    code = "state_validation"
    description = "State validation error"
