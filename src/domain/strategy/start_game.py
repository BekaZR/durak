from typing import Any
from db.models.room import Room
from domain.card.command import CreateDeckCardCommand
from domain.game.command import GameStartCommand
from domain.game.schema import GameSchema
from domain.ready.command import ReadyCommand
from domain.ready.schema import ReadyRequestSchema
from domain.strategy.base import GameStrategy
from domain.turn.command import InitTurnCommand


class SwitchStartGameStrategy(GameStrategy):
    async def execute(self, request: Any, game: GameSchema, room: Room) -> GameSchema:
        game = await GameStartCommand().execute(request=None, game=game, room=room)
        game = await CreateDeckCardCommand().execute(request=None, game=game, room=room)
        game = await InitTurnCommand().execute(request=None, game=game, room=room)
        game = await ...
        return game


class ReadyStrategy(GameStrategy):
    async def execute(
        self, request: ReadyRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game = await ReadyCommand().execute(request=request, game=game, room=room)
        for _, player in game.seats.items():
            if not player.user.is_ready:
                return game

        return game
