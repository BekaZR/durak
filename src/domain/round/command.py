from typing import Any
from db.models.room import Room
from domain.command.base import Command
from domain.game.schema import GameSchema
from domain.round.enum import RoundEnum
from domain.round.schemas import RoundSchema


class RoundCreateCommand(Command):
    async def execute(self, request: Any, game: GameSchema, room: Room) -> GameSchema:
        request.round = RoundSchema(
            slots=[],
            status=RoundEnum.PROCESSING,
        )
        return request

    async def rollback(self, request: Any, game: GameSchema, room: Room) -> GameSchema:
        raise NotImplementedError
