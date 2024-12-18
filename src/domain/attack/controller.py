from sqlalchemy.ext.asyncio import AsyncSession
from db.crud.game import GameCRUD
from db.crud.room import RoomCRUD
from domain.attack.schema import AttackRequestSchema
from domain.game.exception import GameNotFound
from domain.game.schema import GameSchema
from domain.room.exception import RoomNotFound


class AttackController:
    async def attack(
        self, request: AttackRequestSchema, room_id: int, session: AsyncSession
    ) -> GameSchema:
        game_crud = GameCRUD()
        room_crud = RoomCRUD(session=session)
        room = await room_crud.get_by_id(room_id)
        if not room:
            raise RoomNotFound
        game_db_obj = await game_crud.get_by_id(room_id)
        if not game_db_obj:
            raise GameNotFound
        return game_db_obj
