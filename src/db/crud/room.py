from db.crud.base import BaseCRUD
from db.models.room import Room
from domain.room.exception import RoomNotFound
from sqlalchemy.ext.asyncio import AsyncSession

from domain.room.schema import RoomCreateSchema


class RoomCRUD(BaseCRUD):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def create(
        self,
        obj_in: RoomCreateSchema,
    ) -> Room:
        json_data = obj_in.model_dump()
        db_obj = Room(**json_data)
        self.session.add(db_obj)
        await self.session.commit()
        return db_obj

    async def get_by_id(self, id: int) -> Room:
        room = await self.session.get(Room, id)
        if not room:
            raise RoomNotFound
        return room

    async def delete(self, id: int) -> None:
        user = await self.get_by_id(id)
        await self.session.delete(user)
        await self.session.commit()
