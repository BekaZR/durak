from typing import Optional
from domain.command.card.service import CardService
from domain.command.defence.exception import CannotDefenceError
from domain.command.defence.schema import DefenceRequestSchema
from domain.command.round.enum import RoundEnum
from domain.command.round.exception import RoundNotExistError
from domain.command.slot.exception import SlotAlreadyClosedError, SlotIDOutOfRangeError
from domain.command.turn.exception import TrumpNotExistsException, TurnNotExistError
from domain.command.user.exception import UserNotDefenderError
from domain.state.schema import GameStateSchema
from domain.command.game.schema import GameSchema
from db.models.room import Room
from domain.validate.base import BaseValidate
from exception.support import RequestNotSupportedError


class DefenceValidate(BaseValidate):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        if game.round is None:
            raise RoundNotExistError()
        if game.round.status != RoundEnum.PROCESSING:
            raise CannotDefenceError()


class DefenceSlotValidate(BaseValidate):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        if game.round is None:
            raise RoundNotExistError()
        obj_in: Optional[DefenceRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, DefenceRequestSchema):
            raise RequestNotSupportedError()
        if game.round.slots[obj_in.slot]:
            raise SlotAlreadyClosedError()


class DefenceCandDefenceRoundValidate(BaseValidate):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        if game.round is None:
            raise RoundNotExistError()
        if game.round.status != RoundEnum.PROCESSING:
            raise CannotDefenceError()


class DefenceCandBeatValidate(BaseValidate):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_in: Optional[DefenceRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, DefenceRequestSchema):
            raise RequestNotSupportedError()
        if game.round is None:
            raise RoundNotExistError()
        if game.trump is None:
            raise TrumpNotExistsException()
        attacking_card = game.round.slots[obj_in.slot].attacker_card
        defending_card = obj_in.card
        CardService().can_beat_validate(
            attacking_card=attacking_card,
            defending_card=defending_card,
            trump_card=game.trump,
        )


class DefenceUserIsEnemyValidate(BaseValidate):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_in: Optional[DefenceRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, DefenceRequestSchema):
            raise RequestNotSupportedError()
        if game.round is None:
            raise RoundNotExistError()
        if game.trump is None:
            raise TrumpNotExistsException()
        if game.turn is None:
            raise TurnNotExistError()
        if obj_in.user.user_id != game.turn.current_defender_user_id:
            raise UserNotDefenderError()


class DefenceSlotIDValidate(BaseValidate):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_in: Optional[DefenceRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, DefenceRequestSchema):
            raise RequestNotSupportedError()
        if game.round is None:
            raise RoundNotExistError()

        if len(game.round.slots) < obj_in.slot:
            raise SlotIDOutOfRangeError()
