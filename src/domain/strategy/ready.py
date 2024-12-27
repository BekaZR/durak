from typing import Any
from db.models.room import Room
from domain.controller.base import GameController
from domain.command.ready.command import ReadyCommand
from domain.command.game.command import GameReadyCommand
from domain.command.game.schema import GameSchema
from domain.state.schema import GameStateSchema
from domain.strategy.base import GameStrategy
from domain.validate.ready import DublicateReadyValidate


class SwitchToReadyStrategy(GameStrategy):
    async def execute(self, request: Any, game: GameSchema, room: Room) -> GameSchema:
        game_state_schema = GameStateSchema(current_strategy=self)
        await GameReadyCommand().execute(
            request=game_state_schema, game=game, room=room
        )
        return await GameController().switch(
            request=game_state_schema, game=game, room=room
        )


class ReadyStrategy(GameStrategy):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        await DublicateReadyValidate().validate(request=request, game=game, room=room)

    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        request.current_strategy = self
        await ReadyCommand().execute(request=request, game=game, room=room)
        return await GameController().switch(request=request, game=game, room=room)
