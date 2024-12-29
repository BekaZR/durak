from typing_extensions import Optional
from db.models.room import Room
from domain.command.attack.schema import AttackRequestSchema
from domain.command.card.exception import CardNotInHandError, CardNotInTableError
from domain.command.game.schema import GameSchema
from domain.command.round.enum import RoundEnum
from domain.command.round.exception import RoundNotExistError
from domain.command.slot.exception import MaximumSlotsError
from domain.command.slot.service import SlotService
from domain.command.turn.exception import (
    NotYourTurnError,
    QueueIsBlankError,
    TurnNotExistError,
)
from domain.state.schema import GameStateSchema
from domain.validate.base import BaseValidate
from exception.support import RequestNotSupportedError


class AttackIsMyTurnValidate(BaseValidate):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_in: Optional[AttackRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, AttackRequestSchema):
            raise RequestNotSupportedError()
        if game.turn is None:
            raise TurnNotExistError()
        if not game.turn.queue:
            raise QueueIsBlankError()
        if obj_in.user.user_id == game.turn.queue[0]:
            raise NotYourTurnError()


class AttackMaximumSlotsValidate(BaseValidate):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_in: Optional[AttackRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, AttackRequestSchema):
            raise RequestNotSupportedError()
        if game.turn is None:
            raise TurnNotExistError()
        if game.round is None:
            raise RoundNotExistError()
        slot_service = SlotService()

        free_slots = await slot_service.get_free_slots(game.round.slots)
        enemy_cards = game.seats[game.turn.current_defender_user_id].user.cards

        if len(free_slots) >= len(enemy_cards):
            raise MaximumSlotsError()

        match game.round.status:
            case RoundEnum.PROCESSING:
                if game.is_first_round and len(game.round.slots) == 5:
                    raise MaximumSlotsError()

                if len(game.round.slots) == 5:
                    raise MaximumSlotsError()

                if not game.is_first_round and len(game.round.slots) == 6:
                    raise MaximumSlotsError()
            case RoundEnum.TAKE:
                if len(game.round.slots) == 6:
                    raise MaximumSlotsError()
            case _:
                pass


# TODO rename pls)))
class AttackCanAttackCardValidate(BaseValidate):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_in: Optional[AttackRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, AttackRequestSchema):
            raise RequestNotSupportedError()
        if game.round is None:
            raise RoundNotExistError()
        allowed_ranks = {
            slot.attacker_card.rank for slot in game.round.slots if slot.attacker_card
        }
        allowed_ranks.update(
            {slot.enemy_card.rank for slot in game.round.slots if slot.enemy_card}
        )
        if obj_in.card.rank not in allowed_ranks:
            raise CardNotInTableError()


class AttackCardInHandValidate(BaseValidate):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_in: Optional[AttackRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, AttackRequestSchema):
            raise RequestNotSupportedError()
        if game.round is None:
            raise RoundNotExistError()

        if obj_in.card not in game.seats[obj_in.user.user_id].user.cards:
            raise CardNotInHandError()
