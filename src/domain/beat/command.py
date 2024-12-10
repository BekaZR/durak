from db.models.room import Room
from domain.command.base import Command

from domain.beat.schema import BeatRequestSchema
from domain.game.schema import GameSchema
from domain.round.enum import RoundEnum


class BeatCommand(Command):
    async def execute(
        self, request: BeatRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.round.status = RoundEnum.BEAT
        return game

    async def rollback(
        self, request: BeatRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        raise NotImplementedError
