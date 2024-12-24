from typing import Optional
from core.manager import UserNotificationManager
from db.models.room import Room

from domain.command.base import Command
from domain.command.game.schema import GameSchema
from domain.state.schema import GameStateSchema
from domain.command.timer.exception import TimerUserEmptyError
from domain.command.timer.schema import TimerResponseSchema
from domain.command.timer.service import TimerService
from exception.support import ObjNotSupportedError


class CreateTimerCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if request.user is None:
            raise TimerUserEmptyError()
        timer_service = TimerService()
        await timer_service.create(
            user_id=request.user.user_id, room_id=room.id, delay=60
        )
        # await self.notify_room(request, game, room)
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if request.user is None:
            raise TimerUserEmptyError()
        timer_service = TimerService()
        await timer_service.cancel(user_id=request.user.user_id, room_id=room.id)
        await timer_service.delete(room.id)
        return game

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_out: Optional[TimerResponseSchema] = request.response
        if obj_out is None or isinstance(obj_out, TimerResponseSchema):
            raise ObjNotSupportedError()
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=obj_out.model_dump(mode="json"),
        )

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError


class CancelTimerCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if request.user is None:
            raise TimerUserEmptyError()
        timer_service = TimerService()
        await timer_service.cancel(user_id=request.user.user_id, room_id=room.id)
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if request.user is None:
            raise TimerUserEmptyError()
        timer_service = TimerService()
        await timer_service.create(
            user_id=request.user.user_id, room_id=room.id, delay=60
        )
        return game

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_out: Optional[TimerResponseSchema] = request.response
        if obj_out is None or isinstance(obj_out, TimerResponseSchema):
            raise ObjNotSupportedError()
        await UserNotificationManager.send_room_message(
            room_id=room.id, message=obj_out.model_dump(mode="json")
        )

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError


class DeleteAllTimerCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        timer_service = TimerService()
        all_timer = await timer_service.get_all_timer(room.id)
        for timer in all_timer:
            await timer_service.cancel(user_id=timer.user_id, room_id=room.id)
            request.user = game.seats[timer.user_id].user.user
            await self.notify_room(request, game, room)
            await timer_service.delete_by_user_id(room.id, user_id=timer.user_id)
        await timer_service.delete(room.id)
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        return game

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_out: Optional[TimerResponseSchema] = request.response
        if obj_out is None or isinstance(obj_out, TimerResponseSchema):
            raise ObjNotSupportedError()
        await UserNotificationManager.send_room_message(
            room_id=room.id, message=obj_out.model_dump(mode="json")
        )
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=obj_out.model_dump(mode="json"),
        )

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError
