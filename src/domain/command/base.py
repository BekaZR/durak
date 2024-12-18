from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from db.models.room import Room
from domain.user.schema import BaseUserSchema

TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")


class Command(Generic[TRequest, TResponse], ABC):
    @abstractmethod
    async def execute(self, request: TRequest, game: TRequest, room: Room) -> TResponse:
        pass

    @abstractmethod
    async def rollback(
        self, request: TRequest, game: TRequest, room: Room
    ) -> TResponse:
        pass

    @abstractmethod
    async def notify_room(
        self, user: BaseUserSchema, game: TRequest, room: Room
    ) -> None:
        pass

    @abstractmethod
    async def notify_personal(
        self, user: BaseUserSchema, game: TRequest, room: Room
    ) -> None:
        pass


class SupportCommand(Generic[TRequest, TResponse], ABC):
    @abstractmethod
    async def execute(
        self, user: BaseUserSchema, game: TRequest, room: Room
    ) -> TResponse:
        pass

    @abstractmethod
    async def rollback(
        self, user: BaseUserSchema, game: TRequest, room: Room
    ) -> TResponse:
        pass

    @abstractmethod
    async def notify_room(
        self, user: BaseUserSchema, game: TRequest, room: Room
    ) -> None:
        pass

    @abstractmethod
    async def notify_personal(
        self, user: BaseUserSchema, game: TRequest, room: Room
    ) -> None:
        pass
