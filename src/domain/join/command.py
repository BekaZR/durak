from db.models.room import Room
from domain.command.base import Command

from domain.game.schema import GameSchema
from domain.join.schema import JoinRequestSchema
from domain.seat.schema import SeatSchema
from domain.user.schema import UserAchieved, UserConnect, UserSchema


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
        raise NotImplementedError
