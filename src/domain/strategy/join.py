from db.models.room import Room
from domain.game.schema import GameSchema
from domain.join.command import JoinCommand
from domain.join.schema import JoinRequestSchema
from domain.strategy.base import GameStrategy
from domain.strategy.ready import SwitchReadyStrategy


class JoinStrategy(GameStrategy):
    async def execute(
        self, request: JoinRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game = await JoinCommand().execute(request=request, game=game, room=room)
        if len(game.seats) == room.player_count.value:
            await SwitchReadyStrategy().execute(request=None, game=game, room=room)
        return game
