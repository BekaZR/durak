from db.models.room import Room
from domain.command.base import Command

from domain.game.schema import GameSchema
from domain.join.schema import JoinRequestSchema


class ReadyCommand(Command):
    async def execute(
        self, request: JoinRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.seats[request.user.user_id].user.is_ready = True
        return game

    async def rollback(
        self, request: JoinRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        raise NotImplementedError
