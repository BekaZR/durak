from db.models.room import Room
from domain.command.base import Command

from domain.game.schema import GameSchema
from domain.round.enum import RoundEnum

from domain.schema import BaseRequestSchema


class InitCommand(Command):
    async def execute(
        self, request: BaseRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.round.status = RoundEnum.TAKE
        return game

    async def rollback(
        self, request: BaseRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.round.status = RoundEnum.PROCESSING
        return game
