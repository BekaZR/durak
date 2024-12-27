from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.game import GameCRUD
from db.crud.room import RoomCRUD
from db.dependencies import get_db_session
from domain.command.ready.schema import ReadyRequestSchema, ReadyResponseSchema

from domain.state.schema import GameStateSchema
from domain.strategy.ready import ReadyStrategy


router = APIRouter()


@router.post("/ready", response_model=ReadyResponseSchema)
async def attack(
    room_id: int,
    request: ReadyRequestSchema,
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    game_crud = GameCRUD()
    game = await game_crud.get_by_id(room_id)
    room_crud = RoomCRUD(session=session)
    room = await room_crud.get_by_id(room_id)
    game_state_request = GameStateSchema(request=request)
    await ReadyStrategy().validate(request=game_state_request, game=game, room=room)
    await ReadyStrategy().execute(request=game_state_request, game=game, room=room)
    response = ReadyResponseSchema(
        command="ready",
        user=request.user,
        position=game.seats[request.user.user_id].position,
    )
    await game_crud.update(game, room.id)
    return response
