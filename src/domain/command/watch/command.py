from typing import Optional
from core.manager import UserNotificationManager
from db.models.room import Room
from domain.command.base import Command
from domain.command.game.schema import GameSchema
from domain.state.schema import GameStateSchema
from domain.command.watch.schema import WatchRequestSchema, WatchResponseSchema
from exception.support import RequestNotSupportedError
from domain.command.watch.service import WatchService


class WatchCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        # В режиме наблюдения мы только читаем состояние
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        return game

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        # Оповещение всей комнаты не требуется в режиме наблюдения
        pass

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_in: Optional[WatchRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, WatchRequestSchema):
            raise RequestNotSupportedError()

        watch_service = WatchService()
        game_state = await watch_service.get_game_state(game, room)
        timers = await watch_service.get_timers(room.id)

        response = WatchResponseSchema(
            command="watch", game_state=game_state, timers=timers, user=obj_in.user
        )

        await UserNotificationManager.send_personal_message(
            room_id=room.id,
            user=obj_in.user,
            message=response.model_dump(mode="json"),
        )
