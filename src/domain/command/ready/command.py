from typing import Optional
from core.manager import UserNotificationManager
from db.models.room import Room
from domain.command.base import Command

from domain.command.game.schema import GameSchema
from domain.command.ready.schema import ReadyRequestSchema, ReadyResponseSchema
from domain.state.schema import GameStateSchema
from exception.support import RequestNotSupportedError


class ReadyCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        obj_in: Optional[ReadyRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, ReadyRequestSchema):
            raise RequestNotSupportedError()
        game.seats[obj_in.user.user_id].user.is_ready = True
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        obj_in: Optional[ReadyRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, ReadyRequestSchema):
            raise RequestNotSupportedError()
        game.seats[obj_in.user.user_id].user.is_ready = False
        raise NotImplementedError

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_in: Optional[ReadyRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, ReadyRequestSchema):
            raise RequestNotSupportedError()
        game.seats[obj_in.user.user_id].user.is_ready = True
        response = ReadyResponseSchema(
            command="ready",
            position=game.seats[obj_in.user.user_id].position,
            user=obj_in.user,
        )
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=response.model_dump(mode="json"),
        )

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError
