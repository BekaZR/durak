import asyncio
from db.models.room import Room
from domain.command.game.schema import GameSchema
from domain.command.round.enum import RoundEnum
from domain.command.round.exception import RoundNotExistError
from domain.command.take.command import TakeCommand
from domain.controller.base import GameController
from domain.state.schema import GameStateSchema
from domain.strategy.base import GameStrategy
from domain.validate.take import TakePermissionValidate, UserEnemyValidate
from exception.support import RequestNotSupportedError
from domain.command.take.schema import TakeRequestSchema


class TakeRequestStrategy(GameStrategy):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        await UserEnemyValidate().validate(request=request, game=game, room=room)
        await TakePermissionValidate().validate(request=request, game=game, room=room)

    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if request.request is None or not isinstance(
            request.request, TakeRequestSchema
        ):
            raise RequestNotSupportedError()
        _ = await TakeCommand().execute(request=request, game=game, room=room)
        if not game.round:
            raise RoundNotExistError()
        if game.round.status == RoundEnum.TAKE:
            request.next_strategy = self
        asyncio.create_task(
            GameController().switch_delay(request=request, game=game, room=room)
        )
        # await CreateRound
        request.current_command = self
        return await GameController().switch(request=request, game=game, room=room)
