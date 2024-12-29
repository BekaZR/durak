from db.models.room import Room
from domain.command.game.schema import GameSchema
from domain.state.schema import GameStateSchema
from domain.strategy.base import GameStrategy
from domain.command.achieve.command import UserLoseCommand, UserWinCommand


class UserWinStrategy(GameStrategy):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        await UserWinCommand().execute(request=request, game=game, room=room)
        return game


class UserLostStrategy(GameStrategy):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        await UserLoseCommand().execute(request=request, game=game, room=room)
        return game
