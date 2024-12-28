from db.models.room import Room
from domain.command.game.schema import GameSchema
from domain.command.watch.command import WatchCommand
from domain.state.schema import GameStateSchema
from domain.strategy.base import GameStrategy


class WatchStrategy(GameStrategy):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        pass

    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        await WatchCommand().execute(request=request, game=game, room=room)
        return game
