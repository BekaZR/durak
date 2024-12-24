from typing import Any
from fastapi import APIRouter

from domain.command.attack.schema import AttackRequestSchema
from domain.command.round.schemas import RoundSchema


router = APIRouter()


@router.post("/attack", response_model=RoundSchema)
async def attack(room_id: int, request: AttackRequestSchema) -> Any:
    return request
