from abc import ABC, abstractmethod
from typing import Generic, TypeVar


TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")


class GameStrategy(Generic[TRequest, TResponse], ABC):
    """Abstract base class for game strategies"""

    @abstractmethod
    async def execute(
        self, request: TRequest, game: TRequest, room: TRequest
    ) -> TResponse:
        pass
