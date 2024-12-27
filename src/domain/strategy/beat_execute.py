from db.models.room import Room
from domain.command.game.schema import GameSchema
from domain.state.schema import GameStateSchema
from domain.strategy.base import GameStrategy
from domain.command.card.command import AddCardToBeatCommand


class BeatExecuteStrategy(GameStrategy):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        await AddCardToBeatCommand().execute(request=request, game=game, room=room)
        return game
