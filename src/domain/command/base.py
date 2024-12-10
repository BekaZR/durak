from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from db.models.room import Room
from domain.game.schema import GameSchema


TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")


class Command(Generic[TRequest, TResponse], ABC):
    @abstractmethod
    async def execute(
        self, request: TRequest, game: GameSchema, room: Room
    ) -> TResponse:
        pass

    @abstractmethod
    async def rollback(
        self, request: TRequest, game: GameSchema, room: Room
    ) -> TResponse:
        pass
