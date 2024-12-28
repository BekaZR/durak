from typing_extensions import Any
from fastapi.responses import ORJSONResponse
import httpx

from core.logger import service_logger
from exception.base import BackendError


async def read_response(response: httpx.Response) -> None:
    await response.aread()
    service_logger.info(
        f"{response.url} got {response.status_code}:{response.content!r}",
    )


async def logger_hook(request: httpx.Request) -> None:
    service_logger.info(f"Sending {request.content!r} to {request.url}")


async def handle_backend_error(_: Any, exc: BackendError) -> ORJSONResponse:
    return ORJSONResponse(
        content={
            "code": exc.code,
            "description": exc.description,
            "detail": exc.extra_info,
        },
        status_code=exc.status_code,
    )
