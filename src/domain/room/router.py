from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.crud.room import RoomCRUD
from db.dependencies import get_db_session
from domain.room.schema import RoomCreateSchema, RoomSchema

router = APIRouter()


@router.post("/room", response_model=RoomSchema)
async def create_room(
    request: RoomCreateSchema, session: AsyncSession = Depends(get_db_session)
) -> Any:
    room_crud = RoomCRUD(session=session)
    return await room_crud.create(request)
