from core.manager import UserNotificationManager
from db.models.room import Room
from domain.command.base import Command

from domain.game.schema import GameSchema
from domain.join.schema import JoinRequestSchema, JoinResponseSchema
from domain.seat.schema import SeatSchema
from domain.user.schema import BaseUserSchema, UserAchieved, UserConnect, UserSchema


class JoinCommand(Command):
    async def execute(
        self, request: JoinRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.seats[request.user.user_id] = SeatSchema(
            user=UserSchema(
                user=request.user,
                cards=[],
                connect=UserConnect.CONNECTED,
                achieved=UserAchieved.PROCESSING,
            ),
            position=request.position,
        )
        return game

    async def rollback(
        self, request: JoinRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if request.user.user_id in game.seats:
            del game.seats[request.user.user_id]
        return game

    async def notify_room(
        self, user: BaseUserSchema, game: GameSchema, room: Room
    ) -> None:
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=JoinResponseSchema(
                user=user, command="join", position=game.seats[user.user_id].position
            ).model_dump(mode="json"),
        )

    async def notify_personal(
        self, user: BaseUserSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError
