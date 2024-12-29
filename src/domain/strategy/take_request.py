import asyncio
from db.crud.timer import TimerCRUD
from db.models.room import Room
from domain.command.game.enums import GameStatus
from domain.command.game.schema import GameSchema
from domain.command.round.enum import RoundEnum
from domain.command.round.exception import RoundNotExistError
from domain.command.take.command import TakeCommand
from domain.command.timer.command import CancelTimerCommand
from domain.command.timer.schema import TimerStatus
from domain.controller.base import GameController
from domain.state.game import GameEndState
from domain.state.schema import GameStateSchema
from domain.state.take import TakeRoundEndState
from domain.strategy.base import GameStrategy
from domain.strategy.game import GameEndStrategy, GameStartExecuteClassicStrategy
from domain.strategy.ready import SwitchToReadyStrategy
from domain.strategy.round import RoundCreateStrategy
from domain.strategy.take_execute import TakeExecuteStrategy
from domain.timer.attack import AttackTimer
from domain.validate.take import TakePermissionValidate, UserEnemyValidate
from exception.support import RequestNotSupportedError
from domain.command.take.schema import TakeRequestSchema
from domain.timer.beat import BeatTimer


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
        _ = await CancelTimerCommand().execute(request=request, game=game, room=room)
        _ = await TakeRoundEndState().execute(request=request, game=game, room=room)
        _ = await GameEndState().execute(request=request, game=game, room=room)

        if not game.round:
            raise RoundNotExistError()
        if game.round.status == RoundEnum.TAKE:
            await TakeExecuteStrategy().execute(request=request, game=game, room=room)
        if game.status == GameStatus.FINISHED:
            request.seats = game.seats
            request.next_strategy = GameEndStrategy
            await GameController().switch(request=request, game=game, room=room)
            request.next_strategy = GameStartExecuteClassicStrategy
            await GameController().switch(request=request, game=game, room=room)
            request.next_strategy = SwitchToReadyStrategy
            await GameController().switch(request=request, game=game, room=room)
            return game

        if game.round.is_finalized:
            await RoundCreateStrategy().execute(request=request, game=game, room=room)
            asyncio.create_task(
                AttackTimer().execute(request=request, game=game, room=room)
            )
            return game
        asyncio.create_task(BeatTimer().execute(request=request, game=game, room=room))
        return game

    async def execute_delay(
        self, request: GameStateSchema, game: GameSchema, room: Room, delay: int = 0
    ) -> GameSchema:
        if request.request is None or not isinstance(
            request.request, TakeRequestSchema
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
