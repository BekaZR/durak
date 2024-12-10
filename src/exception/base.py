from fastapi import status


class BackendError(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    code: str | None = None
    description: str | None = None
    extra_info: str | None = None

    def __init__(self) -> None:
        super().__init__(self.code, self.description, self.extra_info)
