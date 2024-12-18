from typing import Any
from db.models.room import Room
from domain.command.base import Command

from domain.game.schema import GameSchema
from domain.ready.schema import ReadyRequestSchema
from domain.user.schema import BaseUserSchema


class ReadyCommand(Command):
    async def execute(self, request: Any, game: GameSchema, room: Room) -> GameSchema:

        return game

    async def rollback(
        self, request: ReadyRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        raise NotImplementedError

    async def notify(
        self, user: BaseUserSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        raise NotImplementedError
