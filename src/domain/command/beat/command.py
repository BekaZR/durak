from typing import Optional
from core.manager import UserNotificationManager
from db.models.room import Room
from domain.command.base import Command

from domain.command.beat.schema import BeatRequestSchema, BeatResponseSchema
from domain.command.game.schema import GameSchema
from domain.command.round.exception import RoundNotExistError
from domain.command.turn.exception import TurnNotExistError
from domain.state.schema import GameStateSchema
from exception.support import RequestNotSupportedError


class BeatCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        obj_in: Optional[BeatRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, BeatRequestSchema):
            raise RequestNotSupportedError()
        if not game.round:
            raise RoundNotExistError()
        if game.turn is None:
            raise TurnNotExistError()
        if game.turn:
            game.turn.queue.pop(0)
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        raise NotImplementedError

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_in: Optional[BeatRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, BeatRequestSchema):
            raise RequestNotSupportedError()
        if not game.round:
            raise RoundNotExistError()
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=BeatResponseSchema(
                command="beat",
                user=obj_in.user,
                position=game.seats[obj_in.user.user_id].position,
            ).model_dump(mode="json"),
        )

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError
