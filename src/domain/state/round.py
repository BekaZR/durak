from typing_extensions import Optional
from domain.command.attack.schema import AttackRequestSchema
from domain.command.defence.schema import DefenceRequestSchema
from domain.command.game.schema import GameSchema
from domain.command.seat.service import SeatService
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
        attacker = request.request.user
        attacker_cards = game.seats[attacker.user_id].user.cards

        seat_service = SeatService()
        if not attacker_cards and not game.deck:
            if await seat_service.get_user_count_with_cards(game.seats) <= 1:
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
        if len(game.seats[obj_in.user.user_id].user.cards) == 0:
            game.round.is_finalized = True
        return game
