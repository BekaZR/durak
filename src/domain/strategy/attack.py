from db.crud.timer import TimerCRUD
import asyncio
from db.models.room import Room
from domain.command.attack.command import AttackCommand
from domain.command.attack.schema import AttackRequestSchema
from domain.command.card.command import (
    RemoveUserCardCommand,
)
from domain.command.game.enums import GameStatus
from domain.command.game.schema import GameSchema
from domain.command.round.enum import RoundEnum
from domain.command.round.exception import RoundNotExistError
from domain.command.timer.command import CancelTimerCommand
from domain.command.timer.schema import TimerStatus
from domain.command.turn.command import (
    UpdateTurnCommand,
)
from domain.controller.base import GameController
from domain.state.schema import GameStateSchema
from domain.strategy.base import GameStrategy
from domain.strategy.ready import SwitchToReadyStrategy
from domain.strategy.take_execute import TakeExecuteStrategy
from domain.strategy.win import UserLostStrategy, UserWinStrategy
from domain.timer.attack import AttackTimer
from domain.timer.take import TakeTimer
from domain.validate.attack import (
    AttackCanAttackCardValidate,
    AttackCardInHandValidate,
    AttackIsMyTurnValidate,
    AttackMaximumSlotsValidate,
)
from exception.support import RequestNotSupportedError
from domain.strategy.game import GameEndStrategy
from domain.state.game import GameEndState
from domain.state.round import AttackRoundEndState
from domain.strategy.game import GameStartExecuteClassicStrategy
from domain.strategy.round import RoundCreateStrategy, RoundEndStrategy


class AttackStrategyClassic(GameStrategy):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        await AttackIsMyTurnValidate().validate(request=request, game=game, room=room)
        await AttackCardInHandValidate().validate(request=request, game=game, room=room)
        await AttackCanAttackCardValidate().validate(
            request=request, game=game, room=room
        )
        await AttackMaximumSlotsValidate().validate(
            request=request, game=game, room=room
        )

    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if request.request is None or not isinstance(
            request.request, AttackRequestSchema
        ):
            raise RequestNotSupportedError()

        if game.round is None:
            raise RoundNotExistError()
        request.user = request.request.user

        _ = await RemoveUserCardCommand().execute(request=request, game=game, room=room)
        _ = await AttackCommand().execute(request=request, game=game, room=room)
        # check round is end
        _ = await AttackRoundEndState().execute(request=request, game=game, room=room)
        _ = await CancelTimerCommand().execute(request=request, game=game, room=room)

        user_cards = game.seats[request.request.user.user_id].user.cards
        if not user_cards and not game.deck:
            request.user = request.request.user
            _ = await UserWinStrategy().execute(request=request, game=game, room=room)

        _ = await GameEndState().execute(request=request, game=game, room=room)

        if game.status == GameStatus.FINISHED:
            _ = await UserLostStrategy().execute(request=request, game=game, room=room)

        # if round is end
        if game.round.is_finalized:
            # and enemy take card
            if game.round.status == RoundEnum.TAKE:
                # enemy must be take cards
                _ = await TakeExecuteStrategy().execute(
                    request=request, game=game, room=room
                )
            _ = await RoundEndStrategy().execute(request=request, game=game, room=room)

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

        await UpdateTurnCommand().execute(request=request, game=game, room=room)
        if game.round.status == RoundEnum.TAKE:
            asyncio.create_task(
                AttackTimer().execute(request=request, game=game, room=room)
            )
        else:
            asyncio.create_task(
                TakeTimer().execute(request=request, game=game, room=room)
            )
        return game

    async def execute_delay(
        self, request: GameStateSchema, game: GameSchema, room: Room, delay: int = 0
    ) -> GameSchema:
        if request.request is None or not isinstance(
            request.request, AttackRequestSchema
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
