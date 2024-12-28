from typing_extensions import Optional
from db.models.room import Room
from domain.command.beat.schema import BeatRequestSchema
from domain.command.game.schema import GameSchema
from domain.command.round.exception import RoundNotExistError
from domain.command.slot.service import SlotService
from domain.command.take.exception import CannotTakeError
from domain.command.turn.exception import (
    TurnNotExistError,
)
from domain.state.schema import GameStateSchema
from domain.validate.base import BaseValidate
from exception.support import RequestNotSupportedError


class UserEnemyValidate(BaseValidate):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_in: Optional[BeatRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, BeatRequestSchema):
            raise RequestNotSupportedError()
        if game.turn is None:
            raise TurnNotExistError()
        if obj_in.user.user_id != game.turn.current_defender_user_id:
            raise CannotTakeError()


class TakePermissionValidate(BaseValidate):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        if game.turn is None:
            raise TurnNotExistError()
        if game.round is None:
            raise RoundNotExistError()
        slot_service = SlotService()
        slots_status_in_list = await slot_service.get_all_slots_status(
            slots=game.round.slots
        )

        if all(slots_status_in_list):
            raise CannotTakeError()
