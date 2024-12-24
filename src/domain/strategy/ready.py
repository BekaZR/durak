from typing import Any
from db.models.room import Room
from domain.controller.base import GameController
from domain.command.ready.command import ReadyCommand
from domain.command.game.command import GameReadyCommand
from domain.command.game.schema import GameSchema
from domain.command.ready.schema import ReadyRequestSchema
from domain.state.schema import GameStateSchema
from domain.strategy.base import GameStrategy
from domain.command.timer.command import CreateTimerCommand


class SwitchToReadyStrategy(GameStrategy):
    async def execute(self, request: Any, game: GameSchema, room: Room) -> GameSchema:
        game_state_schema: GameStateSchema = GameStateSchema(current_strategy=self)
        await GameReadyCommand().execute(
            request=game_state_schema, game=game, room=room
        )
        for _, player in game.seats.items():
            game_state_schema.user = player.user.user
            await CreateTimerCommand().execute(
                request=game_state_schema, game=game, room=room
            )
        return game


class ReadyStrategy(GameStrategy):
    async def execute(
        self, request: ReadyRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game_state_schema: GameStateSchema = GameStateSchema(
            current_strategy=self,
        )
        game = await ReadyCommand().execute(
            request=game_state_schema, game=game, room=room
        )
        return await GameController().switch(
            request=game_state_schema, game=game, room=room
        )
