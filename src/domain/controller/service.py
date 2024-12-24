from typing import TYPE_CHECKING, TypeVar
from db.models.room import Room
from domain.command.game.schema import GameSchema
from domain.state.schema import GameStateSchema
from exception.base import BackendError

if TYPE_CHECKING:
    from domain.controller.validator.base import ControllerValidator


TValidator = TypeVar("TValidator", bound="ControllerValidator")


class ControllerService:
    async def validate(
        self,
        request: GameStateSchema,
        game: GameSchema,
        room: Room,
        validators: list[TValidator],
    ) -> bool:
        for validator in validators:
            try:
                await validator.validate(request=request, game=game, room=room)
            except BackendError:
                return False
        return True
