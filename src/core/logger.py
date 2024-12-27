import logging
from contextvars import ContextVar
from dataclasses import dataclass

from core.settings import settings


@dataclass
class RequestContext:
    request_id: str = ""
    method: str = ""
    path: str = ""
    status_code: int | None = None
    client_ip: str | None = None


request_context_var: ContextVar[RequestContext] = ContextVar("request_context_var")

SERVICE_LOG_FORMAT = (
    "[%(levelname)s][%(method)s][%(path)s][%(request_id)s] - %(message)s"
)
UVICORN_LOG_FORMAT = (
    "[%(levelname)s][%(method)s][%(path)s][%(request_id)s] - Status: %(status_code)s"
)


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        request_context = request_context_var.get()
        record.request_id = request_context.request_id
        record.method = request_context.method
        record.path = request_context.path
        record.status_code = request_context.status_code
        return True


def setup_logger(
    logger_name: str,
    log_format: str,
    log_level: int = logging.INFO,
) -> None:
    logger = logging.getLogger(logger_name)
    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(log_format))

    logger.addHandler(handler)
    logger.addFilter(RequestIdFilter())
    logger.setLevel(log_level)


service_logger_log_level = logging.DEBUG if settings.DEBUG else logging.INFO
setup_logger("service_logger", SERVICE_LOG_FORMAT, service_logger_log_level)
setup_logger("uvicorn.access", UVICORN_LOG_FORMAT)

service_logger = logging.getLogger("service_logger")
