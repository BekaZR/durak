from typing import Any
from fastapi import APIRouter

from domain.command.beat.schema import BeatRequestSchema
from domain.command.round.schemas import RoundSchema


router = APIRouter()


@router.post("/beat", response_model=RoundSchema)
async def attack(room_id: int, request: BeatRequestSchema) -> Any:
    return request
