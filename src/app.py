from typing import Any
from fastapi import FastAPI

from core.lifespan import lifespan
from domain.router import router

app = FastAPI(lifespan=lifespan)


app.include_router(router)


@app.get("/")
async def root() -> Any:
    return {"message": "Hello World"}
