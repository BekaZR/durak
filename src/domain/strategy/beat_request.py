import asyncio
from db.crud.timer import TimerCRUD
from db.models.room import Room
from domain.command.game.enums import GameStatus
from domain.command.game.schema import GameSchema
from domain.command.round.enum import RoundEnum
from domain.command.round.exception import RoundNotExistError
from domain.command.timer.command import CancelTimerCommand
from domain.command.timer.schema import TimerStatus
from domain.controller.base import GameController
from domain.state.beat import BeatRoundEndState
from domain.state.game import GameEndState
from domain.state.schema import GameStateSchema
from domain.strategy.base import GameStrategy
from domain.strategy.beat_execute import BeatExecuteStrategy
from domain.strategy.game import GameEndStrategy, GameStartExecuteClassicStrategy
from domain.strategy.ready import SwitchToReadyStrategy
from domain.strategy.round import RoundCreateStrategy, RoundEndStrategy
from domain.strategy.take_execute import TakeExecuteStrategy
from domain.timer.attack import AttackTimer
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

        request.user = request.request.user

        _ = await BeatCommand().execute(request=request, game=game, room=room)
        _ = await CancelTimerCommand().execute(request=request, game=game, room=room)
        _ = await BeatRoundEndState().execute(request=request, game=game, room=room)
        _ = await GameEndState().execute(request=request, game=game, room=room)

        if not game.round:
            raise RoundNotExistError()

        if game.round.is_finalized:
            # and enemy take card
            if game.round.status == RoundEnum.TAKE:
                # enemy must be take cards
                await TakeExecuteStrategy().execute(
                    request=request, game=game, room=room
                )
            else:
                await BeatExecuteStrategy().execute(
                    request=request, game=game, room=room
                )
            await RoundEndStrategy().execute(request=request, game=game, room=room)

        if game.status == GameStatus.FINISHED:
            request.seats = game.seats
            request.next_strategy = GameEndStrategy
            _ = await GameController().switch(request=request, game=game, room=room)
            request.next_strategy = GameStartExecuteClassicStrategy
            _ = await GameController().switch(request=request, game=game, room=room)
            request.next_strategy = SwitchToReadyStrategy
            _ = await GameController().switch(request=request, game=game, room=room)
            return game

        if game.round.is_finalized:
            await RoundCreateStrategy().execute(request=request, game=game, room=room)
            asyncio.create_task(
                AttackTimer().execute(request=request, game=game, room=room)
            )
            return game

        asyncio.create_task(
            AttackTimer().execute(request=request, game=game, room=room)
        )
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
