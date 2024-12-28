from db.models.room import Room
from domain.command.game.schema import GameSchema
from domain.command.timer.exception import TimerNotFound
from domain.command.turn.exception import QueueIsBlankError, TurnNotExistError
from domain.state.schema import GameStateSchema
from domain.strategy.attack import AttackStrategyClassic
from domain.timer.base import BaseDelay
from domain.command.timer.command import CreateTimerCommand


class AttackTimer(BaseDelay):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        if game.turn is None:
            raise TurnNotExistError()
        if not game.turn.queue:
            raise QueueIsBlankError()
        current_attacker_user_id = game.turn.queue[0]

        request.user = game.seats[current_attacker_user_id].user.user

        _ = await CreateTimerCommand().execute(request=request, game=game, room=room)
        if request.timer is None:
            raise TimerNotFound()

        await CreateTimerCommand().notify_room(request=request, game=game, room=room)
        await AttackStrategyClassic().execute_delay(
            request=request, game=game, room=room
        )
