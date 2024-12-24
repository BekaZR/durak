from typing import Any
from db.models.room import Room
from domain.command.base import Command
from domain.command.game.schema import GameSchema
from domain.command.round.enum import RoundEnum
from domain.command.round.schemas import RoundSchema
from domain.state.schema import GameStateSchema


class RoundCreateCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.round = RoundSchema(slots=[], status=RoundEnum.PROCESSING)
        return game

    async def rollback(self, request: Any, game: GameSchema, room: Room) -> GameSchema:
        raise NotImplementedError

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError


class RoundEndCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.round = None
        return game

    async def rollback(self, request: Any, game: GameSchema, room: Room) -> GameSchema:
        raise NotImplementedError

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError
