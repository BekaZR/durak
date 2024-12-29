from db.models.room import Room
from domain.command.game.schema import GameSchema
from domain.command.timer.exception import TimerNotFound
from domain.command.timer.schema import TimerType
from domain.command.user.exception import UserNotFound
from domain.state.schema import GameStateSchema
from domain.strategy.disconnect import DisconnectStrategy
from domain.timer.base import BaseDelay
from domain.command.timer.command import CreateTimerCommand
from domain.state.schema import TimerStateSchema
from core.settings import settings


class DisconnectTimer(BaseDelay):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        if request.user is None:
            raise UserNotFound()
        request.timer = TimerStateSchema(timer_type=TimerType.DISCONNECT)
        _ = await CreateTimerCommand().execute(request=request, game=game, room=room)
        if request.timer is None:
            raise TimerNotFound()
        await DisconnectStrategy().execute_delay(
            request=request, game=game, room=room, delay=settings.TIMER_EXPIRE_SECONDS
        )
