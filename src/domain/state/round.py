from typing_extensions import Optional
from domain.command.defence.schema import DefenceRequestSchema
from domain.command.game.schema import GameSchema
from domain.state.base import GameState
from domain.state.schema import GameStateSchema
from db.models.room import Room
from domain.command.round.exception import RoundNotExistError
from domain.command.round.enum import RoundEnum
from exception.support import RequestNotSupportedError


class AttackRoundEndState(GameState):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if not game.round:
            raise RoundNotExistError()
        match game.round.status:
            case RoundEnum.PROCESSING:
                if game.is_first_round and len(game.round.slots) == 5:
                    game.round.is_finalized = True
                if not game.is_first_round and len(game.round.slots) == 6:
                    game.round.is_finalized = True
            case RoundEnum.TAKE:
                if len(game.round.slots) == 6:
                    game.round.is_finalized = True
            case _:
                pass
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
