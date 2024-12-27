from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.crud.game import GameCRUD
from db.crud.room import RoomCRUD
from db.dependencies import get_db_session
from domain.command.game.command import CreateGameCommand
from domain.room.schema import RoomCreateSchema, RoomSchema
from domain.state.schema import GameStateSchema

router = APIRouter()


@router.post("/room", response_model=RoomSchema)
async def create_room(
    request: RoomCreateSchema, session: AsyncSession = Depends(get_db_session)
) -> Any:
    room_crud = RoomCRUD(session=session)
    room = await room_crud.create(request)
    game_crud = GameCRUD()
    game_state_schema: GameStateSchema = GameStateSchema()
    game = await CreateGameCommand().execute(game_state_schema, Any, room)
    await game_crud.create(game, room.id)
    return room


@router.delete("/room/{room_id}")
async def delete_room(
    room_id: int, session: AsyncSession = Depends(get_db_session)
) -> Any:
    room_crud = RoomCRUD(session=session)
    await room_crud.delete(room_id)
    game_crud = GameCRUD()
    await game_crud.delete(room_id)
    return None
