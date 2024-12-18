from db.crud.base import BaseCRUD
from domain.game.schema import GameSchema


class GameCRUD(BaseCRUD):
    PREFIX = "game"

    def _key_prefix(self, value: int) -> str:
        return f"{self.PREFIX}:{value}"

    async def create(self, obj_in: GameSchema, room_id: int) -> GameSchema:
        key = self._key_prefix(room_id)
        await self.redis.set(key, obj_in.model_dump_json())
        return obj_in

    async def update(self, obj_in: GameSchema, room_id: int) -> GameSchema:
        key = self._key_prefix(room_id)
        await self.redis.set(key, obj_in.model_dump_json())
        return obj_in

    async def get_by_id(self, room_id: int) -> GameSchema:
        key = self._key_prefix(room_id)
        data = await self.redis.get(key)
        return GameSchema.model_validate_json(data)

    async def delete(self, room_id: int) -> None:
        key = self._key_prefix(room_id)
        await self.redis.delete(key)