from typing import Optional
from db.models.room import Room
from domain.command.base import Command

from domain.command.game.schema import GameSchema
from domain.command.round.enum import RoundEnum
from domain.command.round.exception import RoundNotExistError
from domain.state.schema import GameStateSchema
from domain.command.take.schema import TakeRequestSchema
from exception.support import RequestNotSupportedError


class TakeCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        obj_in: Optional[TakeRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, TakeRequestSchema):
            raise RequestNotSupportedError()
        if game.round is None:
            raise RoundNotExistError()
        game.round.status = RoundEnum.TAKE
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if game.round is None:
            return game
        game.round.status = RoundEnum.PROCESSING
        return game
