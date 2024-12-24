from exception.base import BackendError


class ObjNotSupportedError(BackendError):
    code = "obj_not_supported"
    description = "Object not supported"


class RequestNotSupportedError(BackendError):
    code = "request_not_supported"
    description = "Request not supported"
