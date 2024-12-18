from typing import Any
from core.manager import UserNotificationManager
from db.models.room import Room
from domain.command.base import Command

from domain.game.schema import GameSchema, GameSwitchReadySchema

from domain.schema import BaseRequestSchema
from domain.turn.service import TurnService
from domain.user.schema import BaseUserSchema


class InitTurnCommand(Command):
    async def execute(self, request: Any, game: GameSchema, room: Room) -> GameSchema:
        TurnService.initialize_game_turn(game=game)
        return game

    async def rollback(
        self, request: BaseRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.turn = None
        return game

    async def notify_room(
        self, user: BaseUserSchema, game: GameSchema, room: Room
    ) -> None:
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=GameSwitchReadySchema(command="switch_ready").model_dump(
                mode="json"
            ),
        )

    async def notify_personal(
        self, user: BaseUserSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError


class RemoveUserTurnCommand(Command):
    async def execute(self, request: Any, game: GameSchema, room: Room) -> GameSchema:
        TurnService.initialize_game_turn(game=game)
        return game

    async def rollback(
        self, request: BaseRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.turn = None
        return game

    async def notify_room(
        self, user: BaseUserSchema, game: GameSchema, room: Room
    ) -> None:
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=GameSwitchReadySchema(command="switch_ready").model_dump(
                mode="json"
            ),
        )

    async def notify_personal(
        self, user: BaseUserSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError
