import asyncio
from db.models.room import Room
from domain.command.attack.command import AttackCommand
from domain.command.attack.schema import AttackRequestSchema
from domain.command.card.command import (
    RemoveUserCardCommand,
)
from domain.command.game.schema import GameSchema
from domain.command.round.enum import RoundEnum
from domain.command.round.exception import RoundNotExistError
from domain.command.slot.command import MaximumCommand
from domain.controller.base import GameController
from domain.state.schema import GameStateSchema
from domain.strategy.base import GameStrategy
from domain.strategy.defence import DefenceStrategy
from exception.support import RequestNotSupportedError


class TakeRequestStrategy(GameStrategy):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if request.request is None or not isinstance(
            request.request, AttackRequestSchema
        ):
            raise RequestNotSupportedError()
        game = await AttackCommand().execute(request=request, game=game, room=room)
        game = await RemoveUserCardCommand().execute(
            request=request, game=game, room=room
        )
        if not game.round:
            raise RoundNotExistError()
        if game.round.status == RoundEnum.TAKE:
            request.next_strategy = self
        else:
            request.next_strategy = DefenceStrategy
        game = await MaximumCommand().execute(request=request, game=game, room=room)
        if not game.round:
            raise RoundNotExistError()
        if game.round.is_finalized:
            if game.round.status == RoundEnum.TAKE:
                ...
        asyncio.create_task(
            GameController().switch_delay(request=request, game=game, room=room)
        )
        # await CreateRound
        request.current_command = self
        return await GameController().switch(request=request, game=game, room=room)
