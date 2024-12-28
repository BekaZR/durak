from db.models.room import Room
from domain.command.game.schema import GameSchema
from domain.command.timer.exception import TimerNotFound
from domain.command.timer.schema import TimerType
from domain.command.turn.exception import TurnNotExistError
from domain.state.schema import GameStateSchema, TimerStateSchema
from domain.strategy.defence import DefenceStrategy
from domain.timer.base import BaseDelay
from domain.command.timer.command import CreateTimerCommand


class DefenceTimer(BaseDelay):
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
        _ = await DefenceStrategy().execute_delay(request=request, game=game, room=room)
