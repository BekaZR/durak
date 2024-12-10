from db.models.room import Room
from domain.command.base import Command

from domain.game.schema import GameSchema
from domain.round.enum import RoundEnum
from domain.take.schema import TakeRequestSchema


class TakeCommand(Command):
    async def execute(
        self, request: TakeRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.round.status = RoundEnum.TAKE
        return game

    async def rollback(
        self, request: TakeRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.round.status = RoundEnum.PROCESSING
        return game
