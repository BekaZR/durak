from db.models.room import Room
from domain.command.game.schema import GameSchema
from domain.command.take.schema import TakeRequestSchema
from domain.command.timer.exception import TimerNotFound
from domain.command.timer.schema import TimerType
from domain.command.turn.exception import TurnNotExistError
from domain.state.schema import GameStateSchema, TimerStateSchema
from domain.strategy.take_request import TakeRequestStrategy
from domain.timer.base import BaseDelay
from domain.command.timer.command import CreateTimerCommand
from core.settings import settings


class TakeTimer(BaseDelay):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        if game.turn is None:
            raise TurnNotExistError()
        currenct_defence_user_id = game.turn.current_defender_user_id

        request.user = game.seats[currenct_defence_user_id].user.user

        request.timer = TimerStateSchema(timer_type=TimerType.TAKE)
        _ = await CreateTimerCommand().execute(request=request, game=game, room=room)
        if request.timer is None:
            raise TimerNotFound()
        await CreateTimerCommand().notify_room(request=request, game=game, room=room)
        obj_in = TakeRequestSchema(command="take", user=request.user)
        request.request = obj_in
        _ = await TakeRequestStrategy().execute_delay(
            request=request, game=game, room=room, delay=settings.TIMER_EXPIRE_SECONDS
        )
