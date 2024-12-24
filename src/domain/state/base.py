from abc import ABC, abstractmethod
from typing import Generic, TypeVar


TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")


class GameState(Generic[TRequest, TResponse], ABC):
    """Abstract base class for game state"""

    @abstractmethod
    async def execute(
        self, request: TRequest, game: TRequest, room: TRequest
    ) -> TResponse:
        pass
