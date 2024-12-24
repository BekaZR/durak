from db.models.room import Room
from domain.controller.base import GameController
from domain.command.game.schema import GameSchema
from domain.command.join.command import JoinCommand
from domain.command.join.schema import JoinRequestSchema
from domain.state.schema import GameStateSchema
from domain.strategy.base import GameStrategy


class JoinStrategy(GameStrategy):
    async def execute(
        self, request: JoinRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game_state = GameStateSchema(
            current_command=JoinCommand(),
            current_strategy=self,
            request=request,
            user=request.user,
        )
        game = await JoinCommand().execute(request=game_state, game=game, room=room)
        return await GameController().switch(game_state, game, room)
