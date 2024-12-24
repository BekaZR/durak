from typing import Any
from fastapi import APIRouter

from domain.command.ready.schema import ReadyRequestSchema
from domain.command.round.schemas import RoundSchema


router = APIRouter()


@router.post("/ready", response_model=RoundSchema)
async def attack(room_id: int, request: ReadyRequestSchema) -> Any:
    return request
