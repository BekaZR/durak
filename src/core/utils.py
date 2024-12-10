import httpx

from core.logger import service_logger


async def read_response(response: httpx.Response) -> None:
    await response.aread()
    service_logger.info(
        f"{response.url} got {response.status_code}:{response.content!r}",
    )


async def logger_hook(request: httpx.Request) -> None:
    service_logger.info(f"Sending {request.content!r} to {request.url}")
