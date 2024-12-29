import asyncio
from db.crud.timer import TimerCRUD
from db.models.room import Room
from domain.command.card.command import (
    RemoveUserCardCommand,
)
from domain.command.defence.schema import DefenceRequestSchema
from domain.command.game.enums import GameStatus
from domain.command.game.schema import GameSchema
from domain.command.round.exception import RoundNotExistError
from domain.command.slot.service import SlotService
from domain.command.timer.command import CancelTimerCommand
from domain.command.timer.schema import TimerStatus
from domain.command.turn.command import (
    UpdateTurnCommand,
)
from domain.controller.base import GameController
from domain.state.game import GameEndState
from domain.state.round import DefenceRoundEndState
from domain.state.schema import GameStateSchema
from domain.state.slot import DefenceNewCardInTableState
from domain.strategy.base import GameStrategy
from domain.strategy.beat_execute import BeatExecuteStrategy
from domain.strategy.game import GameEndStrategy, GameStartExecuteClassicStrategy
from domain.strategy.ready import SwitchToReadyStrategy
from domain.strategy.round import RoundCreateStrategy, RoundEndStrategy
from domain.timer.attack import AttackTimer
from domain.timer.beat import BeatTimer
from domain.timer.take import TakeTimer
from domain.validate.defence import (
    DefenceCandBeatValidate,
    DefenceCandDefenceRoundValidate,
    DefenceSlotIDValidate,
    DefenceSlotValidate,
    DefenceUserIsEnemyValidate,
    DefenceValidate,
)
from exception.support import RequestNotSupportedError
from domain.command.defence.command import DefenceCommand


class DefenceStrategy(GameStrategy):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        await DefenceUserIsEnemyValidate().validate(
            request=request, game=game, room=room
        )
        await DefenceSlotIDValidate().validate(request=request, game=game, room=room)
        await DefenceCandDefenceRoundValidate().validate(
            request=request, game=game, room=room
        )
        await DefenceSlotValidate().validate(request=request, game=game, room=room)
        await DefenceValidate().validate(request=request, game=game, room=room)
        await DefenceCandBeatValidate().validate(request=request, game=game, room=room)

    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if request.request is None or not isinstance(
            request.request, DefenceRequestSchema
        ):
            raise RequestNotSupportedError()
        if not game.round:
            raise RoundNotExistError()

        _ = await DefenceCommand().execute(request=request, game=game, room=room)
        _ = await RemoveUserCardCommand().execute(request=request, game=game, room=room)
        _ = await DefenceNewCardInTableState().execute(
            request=request, game=game, room=room
        )
        _ = await CancelTimerCommand().execute(request=request, game=game, room=room)

        _ = await DefenceRoundEndState().execute(request=request, game=game, room=room)
        _ = await GameEndState().execute(request=request, game=game, room=room)

        if game.round.is_finalized:
            _ = await BeatExecuteStrategy().execute(
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
            _ = await RoundCreateStrategy().execute(
                request=request, game=game, room=room
            )
            asyncio.create_task(
                AttackTimer().execute(request=request, game=game, room=room)
            )
            return game

        if request.update_turn:
            _ = await UpdateTurnCommand().execute(request=request, game=game, room=room)
            request.update_turn = False

        slot_service = SlotService()
        slots_status = await slot_service.get_all_slots_status(game.round.slots)
        if all(slots_status):
            asyncio.create_task(
                BeatTimer().execute(request=request, game=game, room=room)
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
            request.request, DefenceRequestSchema
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
