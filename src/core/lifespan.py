from contextlib import asynccontextmanager
from typing import Any, AsyncIterator
from fastapi import FastAPI
import httpx
from core.settings import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core.utils import logger_hook, read_response


engine = create_async_engine(
    str(settings.POSTGRES_URL),
    echo=settings.POSTGRES_ECHO,
    pool_size=20,
    pool_use_lifo=True,
)
session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


def _setup_httpx(app: FastAPI) -> None:
    app.state.httpx_client = httpx.AsyncClient(
        timeout=httpx.Timeout(
            timeout=5.0,
        ),
        event_hooks={
            "request": [logger_hook],
            "response": [read_response],
        },
    )


def _setup_db(app: FastAPI) -> None:
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[Any]:
    # Setup
    _setup_db(app)
    _setup_httpx(app)

    try:
        yield
    finally:
        # Cleanup
        await engine.dispose()
        await app.state.httpx_client.aclose()
