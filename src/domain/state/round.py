from domain.command.game.schema import GameSchema
from domain.state.base import GameState
from domain.state.schema import GameStateSchema
from db.models.room import Room
from domain.command.round.exception import RoundNotExistError
from domain.command.round.enum import RoundEnum


class RoundEndState(GameState):
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
