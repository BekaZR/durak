from db.models.room import Room
from domain.controller.base import GameController
from domain.command.game.schema import GameSchema
from domain.command.join.command import JoinCommand
from domain.state.schema import GameStateSchema
from domain.strategy.base import GameStrategy
from domain.validate.join import DublicateJoinValidate


class JoinStrategy(GameStrategy):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        await DublicateJoinValidate().validate(request=request, game=game, room=room)

    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        request.current_strategy = self
        game = await JoinCommand().execute(request=request, game=game, room=room)
        return await GameController().switch(request, game, room)
