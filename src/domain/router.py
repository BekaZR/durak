from fastapi import APIRouter
from domain.command.join.router import router as join
from domain.room.router import router as room

router = APIRouter()

router.include_router(join)
router.include_router(room)
