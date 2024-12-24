from abc import ABC, abstractmethod
from typing import TypeVar

from db.models.room import Room
from domain.command.game.schema import GameSchema
from domain.state.schema import GameStateSchema

TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")


class Command(ABC):
    @abstractmethod
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        pass

    @abstractmethod
    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        pass

    @abstractmethod
    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        pass

    @abstractmethod
    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        pass
