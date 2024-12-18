from typing import Any
from db.models.room import Room
from domain.game.command import GameReadyCommand
from domain.game.schema import GameSchema
from domain.ready.command import ReadyCommand
from domain.ready.schema import ReadyRequestSchema
from domain.strategy.base import GameStrategy
from domain.timer.command import CreateTimerCommand
from domain.user.schema import BaseUserSchema


class SwitchReadyStrategy(GameStrategy):
    async def execute(self, request: Any, game: GameSchema, room: Room) -> GameSchema:
        await GameReadyCommand().execute(request=None, game=game, room=room)
        await GameReadyCommand().notify_room(
            user=BaseUserSchema(user_id=0, username=""), game=game, room=room
        )
        for _, player in game.seats.items():
            await CreateTimerCommand().execute(
                user=player.user.user, game=game, room=room
            )
            await CreateTimerCommand().notify_room(
                user=player.user.user, game=game, room=room
            )
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
