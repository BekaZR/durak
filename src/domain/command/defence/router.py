from typing import Any
from fastapi import APIRouter

from domain.command.defence.schema import DefenceRequestSchema
from domain.command.round.schemas import RoundSchema


router = APIRouter()


@router.post("/defence", response_model=RoundSchema)
async def attack(room_id: int, request: DefenceRequestSchema) -> Any:
    return request
