from inspect import currentframe
from fastapi import status
from pydantic import BaseModel
from core.settings import settings


class ErrorLocation(BaseModel):
    """Stores information about where an error occurred"""

    filename: str
    line_number: int
    function_name: str

    def __str__(self) -> str:
        return f"{self.filename}:{self.line_number} in {self.function_name}"


class BackendError(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    code: str | None = None
    description: str | None = None
    extra_info: str | None = None

    def __init__(self) -> None:
        if not settings.DEBUG:
            return super().__init__(self.code, self.description, self.extra_info)
        caller_frame = currentframe()
        if not caller_frame:
            return super().__init__(self.code, self.description, self.extra_info)
        frame = caller_frame.f_back
        if not frame:
            return super().__init__(self.code, self.description, self.extra_info)
        # Get file name, line number and function name
        filename = frame.f_code.co_filename
        line_number = frame.f_lineno
        function_name = caller_frame.f_code.co_name
        self.extra_info = str(
            ErrorLocation(
                filename=filename, line_number=line_number, function_name=function_name
            )
        )
        super().__init__(self.code, self.description, self.extra_info)
