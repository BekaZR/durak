import asyncio
from db.crud.timer import TimerCRUD
from db.models.room import Room
from domain.command.game.schema import GameSchema
from domain.command.round.enum import RoundEnum
from domain.command.round.exception import RoundNotExistError
from domain.command.slot.command import MaximumCommand
from domain.command.timer.schema import TimerStatus
from domain.controller.base import GameController
from domain.state.schema import GameStateSchema
from domain.strategy.base import GameStrategy
from domain.strategy.defence import DefenceStrategy
from domain.validate.beat import (
    BeatPermissionValidate,
    NotUserMoveValidate,
    UserNotEnemyValidate,
)
from exception.support import RequestNotSupportedError
from domain.command.beat.schema import BeatRequestSchema
from domain.command.beat.command import BeatCommand


class BeatRequestStrategy(GameStrategy):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        await UserNotEnemyValidate().validate(request=request, game=game, room=room)
        await NotUserMoveValidate().validate(request=request, game=game, room=room)
        await BeatPermissionValidate().validate(request=request, game=game, room=room)

    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if request.request is None or not isinstance(
            request.request, BeatRequestSchema
        ):
            raise RequestNotSupportedError()
        _ = await BeatCommand().execute(request=request, game=game, room=room)
        if not game.round:
            raise RoundNotExistError()
        if game.round.status == RoundEnum.TAKE:
            request.next_strategy = self
        else:
            request.next_strategy = DefenceStrategy
        _ = await MaximumCommand().execute(request=request, game=game, room=room)
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

    async def execute_delay(
        self, request: GameStateSchema, game: GameSchema, room: Room, delay: int = 0
    ) -> GameSchema:
        if request.request is None or not isinstance(
            request.request, BeatRequestSchema
        ):
            raise RequestNotSupportedError()
        await asyncio.sleep(delay)
        obj_in = request.request
        timer_crud = TimerCRUD()
        timer = await timer_crud.get_by_user_id(
            room_id=room.id, user_id=obj_in.user.user_id
        )
        if timer.status != TimerStatus.CANCELED:
            return game
        return await self.execute(request=request, game=game, room=room)
