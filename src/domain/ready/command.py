from core.manager import UserNotificationManager
from db.models.room import Room
from domain.command.base import Command

from domain.game.schema import GameSchema
from domain.ready.schema import ReadyRequestSchema, ReadyResponseSchema
from domain.user.schema import BaseUserSchema


class ReadyCommand(Command):
    async def execute(
        self, request: ReadyRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.seats[request.user.user_id].user.is_ready = True
        return game

    async def rollback(
        self, request: ReadyRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        raise NotImplementedError

    async def notify_room(
        self, user: BaseUserSchema, game: GameSchema, room: Room
    ) -> None:
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=ReadyResponseSchema(
                user=user, position=game.seats[user.user_id].position, command="ready"
            ).model_dump(mode="json"),
        )

    async def notify_personal(
        self, user: BaseUserSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError
