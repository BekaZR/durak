from db.models.room import Room
from domain.command.game.schema import GameSchema
from domain.command.round.exception import RoundNotExistError
from domain.command.turn.exception import TurnNotExistError
from domain.state.base import GameState
from domain.state.schema import GameStateSchema


class BeatRoundEndState(GameState):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if game.turn is None:
            raise TurnNotExistError()

        if game.round is None:
            raise RoundNotExistError()
        if not game.turn.queue:
            game.round.is_finalized = True
        return game
