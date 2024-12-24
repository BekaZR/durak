from domain.command.game.schema import GameSchema
from domain.state.base import GameState
from domain.state.schema import GameStateSchema
from db.models.room import Room


class WinState(GameState):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        ...
        return game
