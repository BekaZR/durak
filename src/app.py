from typing import Any
from fastapi import FastAPI

from core.lifespan import lifespan
from core.middleware import LogRequestIdMiddleware
from core.utils import handle_backend_error
from domain.router import router
from exception.base import BackendError

app = FastAPI(lifespan=lifespan)


app.include_router(router)

app.add_exception_handler(BackendError, handler=handle_backend_error)
app.add_middleware(LogRequestIdMiddleware)


@app.get("/")
async def root() -> Any:
    return {"message": "Hello World"}
