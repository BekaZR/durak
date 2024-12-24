from datetime import UTC, datetime, timedelta

from db.crud.timer import TimerCRUD
from domain.command.timer.schema import TimerCreateSchema, TimerStatus
from domain.command.user.types import UserID


class TimerService:
    def __init__(self) -> None:
        self.timer_crud = TimerCRUD()

    async def create(self, user_id: UserID, room_id: int, delay: int) -> None:
        datetime_now = datetime.now(tz=UTC)
        request = TimerCreateSchema(
            user_id=user_id,
            created_at=datetime_now,
            expired_at=datetime_now + timedelta(seconds=delay),
            status=TimerStatus.ACTIVE,
        )
        await self.timer_crud.create(request, room_id)

    async def cancel(self, user_id: UserID, room_id: int) -> None:
        timer = await self.timer_crud.get_by_user_id(room_id, user_id=user_id)
        timer.status = TimerStatus.CANCELED
        await self.timer_crud.update(timer, room_id)

    async def delete(self, room_id: int) -> None:
        await self.timer_crud.delete(room_id=room_id)

    async def delete_by_user_id(self, room_id: int, user_id: UserID) -> None:
        await self.timer_crud.delete_by_user_id(user_id=user_id, room_id=room_id)

    async def get_all_timer(self, room_id: int) -> list[TimerCreateSchema]:
        return await self.timer_crud.get_by_room_id(room_id)
