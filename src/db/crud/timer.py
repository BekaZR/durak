from db.crud.base import BaseCRUD
from domain.timer.exception import TimerNotFound
from domain.timer.schema import TimerCreateSchema
from pydantic import TypeAdapter


class TimerCRUD(BaseCRUD):
    PREFIX = "timer"

    def _key_prefix(self, value: int) -> str:
        return f"{self.PREFIX}:{value}"

    async def create(
        self, obj_in: TimerCreateSchema, room_id: int
    ) -> TimerCreateSchema:
        key = self._key_prefix(room_id)
        self.redis.hset(key, f"{obj_in.user_id}", obj_in.model_dump_json())
        return obj_in

    async def update(
        self, obj_in: TimerCreateSchema, room_id: int
    ) -> TimerCreateSchema:
        key = self._key_prefix(room_id)
        self.redis.hset(key, f"{obj_in.user_id}", obj_in.model_dump_json())
        return obj_in

    async def get_by_room_id(self, room_id: int) -> list[TimerCreateSchema]:
        key = self._key_prefix(room_id)
        data = self.redis.get(key)
        if not data:
            raise TimerNotFound
        return TypeAdapter(list[TimerCreateSchema]).validate_python(data)

    async def get_by_user_id(self, room_id: int, user_id: int) -> TimerCreateSchema:
        key = self._key_prefix(room_id)
        data = self.redis.hget(key, f"{user_id}")
        if not data:
            raise TimerNotFound
        return TimerCreateSchema.model_validate(data)

    async def delete(self, room_id: int) -> None:
        key = self._key_prefix(room_id)
        await self.redis.delete(key)

    async def delete_by_user_id(self, room_id: int, user_id: int) -> None:
        key = self._key_prefix(room_id)
        self.redis.hdel(key, f"{user_id}")
