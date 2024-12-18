from core.manager import UserNotificationManager
from db.models.room import Room
from domain.command.base import SupportCommand

from domain.game.schema import GameSchema, GameSwitchReadySchema
from domain.timer.schema import TimerResponseSchema
from domain.timer.service import TimerService
from domain.user.schema import BaseUserSchema


class CreateTimerCommand(SupportCommand):
    async def execute(
        self, user: BaseUserSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        timer_service = TimerService()
        await timer_service.create(user_id=user.user_id, room_id=room.id, delay=60)
        return game

    async def rollback(
        self, user: BaseUserSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        timer_service = TimerService()
        await timer_service.cancel(user_id=user.user_id, room_id=room.id)
        await timer_service.delete(room.id)
        return game

    async def notify_room(
        self, user: BaseUserSchema, game: GameSchema, room: Room
    ) -> None:
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=TimerResponseSchema(command="create_timer").model_dump(mode="json"),
        )

    async def notify_personal(
        self, user: BaseUserSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError


class CancelTimerCommand(SupportCommand):
    async def execute(
        self, user: BaseUserSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        timer_service = TimerService()
        await timer_service.cancel(user_id=user.user_id, room_id=room.id)
        return game

    async def rollback(
        self, user: BaseUserSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        timer_service = TimerService()
        await timer_service.create(user_id=user.user_id, room_id=room.id, delay=60)
        return game

    async def notify_room(
        self, user: BaseUserSchema, game: GameSchema, room: Room
    ) -> None:
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=GameSwitchReadySchema(command="switch_ready").model_dump(
                mode="json"
            ),
        )

    async def notify_personal(
        self, user: BaseUserSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError


class DeleteAllTimerCommand(SupportCommand):
    async def execute(
        self, user: BaseUserSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        timer_service = TimerService()
        all_timer = await timer_service.get_all_timer(room.id)
        for timer in all_timer:
            await timer_service.cancel(user_id=user.user_id, room_id=room.id)
            await timer_service.delete_by_user_id(room.id, user_id=user.user_id)
        await timer_service.delete(room.id)
        return game

    async def rollback(
        self, user: BaseUserSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        return game

    async def notify_room(
        self, user: BaseUserSchema, game: GameSchema, room: Room
    ) -> None:
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=GameSwitchReadySchema(command="switch_ready").model_dump(
                mode="json"
            ),
        )

    async def notify_personal(
        self, user: BaseUserSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError
