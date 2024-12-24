from abc import ABC, abstractmethod

from db.models.room import Room
from domain.command.game.schema import GameSchema
from domain.state.schema import GameStateSchema


class ControllerValidator(ABC):
    @abstractmethod
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        ...
