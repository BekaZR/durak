from typing import Any
from fastapi import APIRouter, Depends

from db.crud.game import GameCRUD
from db.crud.room import RoomCRUD
from db.dependencies import get_db_session
from domain.command.join.schema import JoinRequestSchema, JoinResponseSchema
from domain.strategy.join import JoinStrategy
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/{room_id}/join", response_model=JoinRequestSchema)
async def attack(
    room_id: int,
    request: JoinRequestSchema,
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    game_crud = GameCRUD()
    game = await game_crud.get_by_id(room_id)
    room_crud = RoomCRUD(session=session)
    room = await room_crud.get_by_id(room_id)
    await JoinStrategy().execute(request=request, game=game, room=room)
    response = JoinResponseSchema(
        command="join",
        user=request.user,
        position=game.seats[request.user.user_id].position,
    )
    await game_crud.update(game, room_id)
    return response
