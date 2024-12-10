import httpx

from core.utils import logger_hook, read_response


http_client = httpx.AsyncClient(
    timeout=httpx.Timeout(
        timeout=5.0,
    ),
    event_hooks={
        "request": [logger_hook],
        "response": [read_response],
    },
)
