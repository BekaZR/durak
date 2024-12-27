from fastapi import APIRouter
from domain.command.join.router import router as join
from domain.command.ready.router import router as ready
from domain.room.router import router as room

router = APIRouter()

router.include_router(join)
router.include_router(room)
router.include_router(ready)
