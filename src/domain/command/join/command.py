from typing import Optional
from core.manager import UserNotificationManager
from db.models.room import Room
from domain.command.base import Command

from domain.command.game.schema import GameSchema
from domain.command.join.schema import JoinRequestSchema
from domain.command.seat.schema import SeatSchema
from domain.command.user.exception import UserNotFound
from domain.state.schema import GameStateSchema
from domain.command.user.schema import UserAchieved, UserConnect, UserSchema
from exception.support import RequestNotSupportedError


class JoinCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        obj_in: Optional[JoinRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, JoinRequestSchema):
            raise RequestNotSupportedError()
        game.seats[obj_in.user.user_id] = SeatSchema(
            user=UserSchema(
                user=obj_in.user,
                cards=[],
                connect=UserConnect.CONNECTED,
                achieved=UserAchieved.PROCESSING,
            ),
            position=obj_in.position,
        )
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        obj_in: Optional[JoinRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, JoinRequestSchema):
            raise RequestNotSupportedError()
        if obj_in.user.user_id in game.seats:
            del game.seats[obj_in.user.user_id]
        return game

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_in: Optional[JoinRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, JoinRequestSchema):
            raise RequestNotSupportedError()
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=obj_in.model_dump(mode="json"),
        )

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError


class DisconnectCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if not request.user:
            raise UserNotFound()
        if game.seats[request.user.user_id]:
            del game.seats[request.user.user_id]
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if not request.user:
            raise UserNotFound()
        user = request.user
        game.seats[user.user_id] = SeatSchema(
            user=UserSchema(
                user=user,
                cards=[],
                connect=UserConnect.CONNECTED,
                achieved=UserAchieved.PROCESSING,
            ),
            position=0,
        )
        return game

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_in: Optional[JoinRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, JoinRequestSchema):
            raise RequestNotSupportedError()
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=obj_in.model_dump(mode="json"),
        )

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError
