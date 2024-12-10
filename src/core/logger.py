import sys
import logging

uvicorn_access_logger = logging.getLogger("uvicorn.access")

from loguru import logger  # noqa: E402

PRIME_DIR = "../../../logs/"

config = {
    "handlers": [
        {"sink": sys.stdout, "level": "DEBUG"},
    ],
}

logger.configure(**config)  # type: ignore

service_logger = logger
