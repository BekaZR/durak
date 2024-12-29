from db.models.room import Room
from domain.command.beat.schema import BeatRequestSchema
from domain.command.game.schema import GameSchema
from domain.command.timer.exception import TimerNotFound
from domain.command.turn.exception import QueueIsBlankError, TurnNotExistError
from domain.state.schema import GameStateSchema
from domain.strategy.beat_request import BeatRequestStrategy
from domain.timer.base import BaseDelay
from domain.command.timer.command import CreateTimerCommand
from core.settings import settings


class BeatTimer(BaseDelay):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        if game.turn is None:
            raise TurnNotExistError()
        if not game.turn.queue:
            raise QueueIsBlankError()
        current_user_id = game.turn.queue[0]

        request.user = game.seats[current_user_id].user.user

        _ = await CreateTimerCommand().execute(request=request, game=game, room=room)
        if request.timer is None:
            raise TimerNotFound()
        obj_in = BeatRequestSchema(
            command="beat",
            user=request.user,
        )
        request.request = obj_in
        await BeatRequestStrategy().execute_delay(
            request=request, game=game, room=room, delay=settings.TIMER_EXPIRE_SECONDS
        )
