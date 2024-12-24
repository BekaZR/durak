from db.models.room import Room
from domain.command.base import Command
from domain.command.game.schema import GameSchema
from domain.command.user.exception import UserNotFound
from domain.command.user.schema import UserAchieved
from domain.state.schema import GameStateSchema


class UserWinCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if request.user is None:
            raise UserNotFound()
        game.seats[request.user.user_id].user.achieved = UserAchieved.WIN
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        raise NotImplementedError

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError


class UserLoseCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if request.user is None:
            raise UserNotFound()
        game.seats[request.user.user_id].user.achieved = UserAchieved.LOSE
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        raise NotImplementedError

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError
