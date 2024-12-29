from typing_extensions import Optional
from domain.command.attack.schema import AttackRequestSchema
from domain.command.defence.schema import DefenceRequestSchema
from domain.command.game.schema import GameSchema
from domain.command.round.enum import RoundEnum
from domain.command.seat.service import SeatService
from domain.command.slot.service import SlotService
from domain.command.turn.exception import TurnNotExistError
from domain.state.base import GameState
from domain.state.schema import GameStateSchema
from db.models.room import Room
from domain.command.round.exception import RoundNotExistError
from exception.support import RequestNotSupportedError


class AttackRoundEndState(GameState):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if not game.round:
            raise RoundNotExistError()
        if request.request is None or not isinstance(
            request.request, AttackRequestSchema
        ):
            raise RequestNotSupportedError()
        if game.turn is None:
            raise TurnNotExistError()
        attacker = request.request.user
        attacker_cards = game.seats[attacker.user_id].user.cards

        seat_service = SeatService()
        slot_service = SlotService()
        if not attacker_cards and not game.deck:
            if await seat_service.get_user_count_with_cards(game.seats) <= 1:
                game.round.is_finalized = True

        free_slots = await slot_service.get_free_slots(game.round.slots)
        enemy_cards = game.seats[game.turn.current_defender_user_id].user.cards
        is_can_attack_with_new_card = len(free_slots) >= len(enemy_cards)
        is_maximum_slots = await slot_service.is_maximum_slots(
            game.round.slots, game.is_first_round
        )

        if game.round.status == RoundEnum.TAKE and any(
            [is_can_attack_with_new_card, is_maximum_slots]
        ):
            game.round.is_finalized = True
        return game


class DefenceRoundEndState(GameState):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        obj_in: Optional[DefenceRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, DefenceRequestSchema):
            raise RequestNotSupportedError()
        if not game.round:
            raise RoundNotExistError()
        if game.turn is None:
            raise TurnNotExistError()
        if len(game.seats[obj_in.user.user_id].user.cards) == 0:
            game.round.is_finalized = True

        slot_service = SlotService()
        slots_status = await slot_service.get_all_slots_status(game.round.slots)
        is_maximum_slot = await slot_service.is_maximum_slots(
            slots=game.round.slots, is_fisrt_round=game.is_first_round
        )
        free_slots = await slot_service.get_free_slots(game.round.slots)
        enemy_cards = game.seats[game.turn.current_defender_user_id].user.cards
        is_can_attack_with_new_card = len(free_slots) >= len(enemy_cards)
        if all(slots_status):
            if (
                any([is_can_attack_with_new_card, is_maximum_slot])
                or not game.turn.queue
            ):
                game.round.is_finalized = True
        return game
