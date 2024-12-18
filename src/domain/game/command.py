from typing import Any

from core.manager import UserNotificationManager
from db.crud.game import GameCRUD
from db.models.room import Room
from domain.command.base import Command

from domain.game.enums import GameStatus
from domain.game.schema import GameSchema, GameSwitchReadySchema
from domain.join.schema import JoinRequestSchema
from domain.user.schema import BaseUserSchema


class CreateGameCommand(Command):
    async def execute(self, request: Any, game: Any, room: Room) -> GameSchema:
        game_crud = GameCRUD()
        game = GameSchema(
            seats={},
            deck=[],
            round=None,
            status=GameStatus.STARTED,
        )
        await game_crud.create(game, room.id)
        return game

    async def rollback(self, request: JoinRequestSchema, game: GameSchema, room: Room) -> GameSchema:
        game_crud = GameCRUD()
        await game_crud.delete(room.id)
        return game

    async def notify_room(self, user: BaseUserSchema, game: GameSchema, room: Room) -> None:
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=GameSwitchReadySchema(command="switch_ready").model_dump(mode="json"),
        )

    async def notify_personal(self, user: BaseUserSchema, game: GameSchema, room: Room) -> None:
        raise NotImplementedError


class GameReadyCommand(Command):
    async def execute(self, request: Any, game: GameSchema, room: Room) -> GameSchema:
        game.status = GameStatus.READY
        return game

    async def rollback(self, request: JoinRequestSchema, game: GameSchema, room: Room) -> GameSchema:
        game.status = GameStatus.STARTED
        return game

    async def notify_room(self, user: BaseUserSchema, game: GameSchema, room: Room) -> None:
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=GameSwitchReadySchema(command="switch_ready").model_dump(mode="json"),
        )

    async def notify_personal(self, user: BaseUserSchema, game: GameSchema, room: Room) -> None:
        raise NotImplementedError


class GameStartCommand(Command):
    async def execute(self, request: Any, game: GameSchema, room: Room) -> GameSchema:
        game.status = GameStatus.STARTED
        return game

    async def rollback(self, request: JoinRequestSchema, game: GameSchema, room: Room) -> GameSchema:
        game.status = GameStatus.READY
        return game

    async def notify_room(self, user: BaseUserSchema, game: GameSchema, room: Room) -> None:
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=GameSwitchReadySchema(command="switch_ready").model_dump(mode="json"),
        )

    async def notify_personal(self, user: BaseUserSchema, game: GameSchema, room: Room) -> None:
        raise NotImplementedError
