import asyncio
from db.crud.timer import TimerCRUD
from db.models.room import Room
from domain.command.timer.schema import TimerStatus
from domain.command.user.exception import UserNotFound
from domain.command.game.schema import GameSchema
from domain.command.join.command import DeleteUserCommand
from domain.state.schema import GameStateSchema
from domain.strategy.base import GameStrategy


class DisconnectStrategy(GameStrategy):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        return game

    async def execute_delay(
        self, request: GameStateSchema, game: GameSchema, room: Room, delay: int = 0
    ) -> GameSchema:
        await asyncio.sleep(delay)
        timer_crud = TimerCRUD()
        if request.user is None:
            raise UserNotFound()
        timer = await timer_crud.get_by_user_id(
            room_id=room.id, user_id=request.user.user_id
        )
        if timer.status != TimerStatus.CANCELED:
            return game

        await DeleteUserCommand().execute(request=request, game=game, room=room)
        return game
