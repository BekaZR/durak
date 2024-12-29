from typing import Any

from core.manager import UserNotificationManager
from db.crud.game import GameCRUD
from db.models.room import Room
from domain.command.base import Command

from domain.command.game.enums import GameStatus
from domain.command.game.schema import GameSchema
from pydantic import TypeAdapter
from domain.command.user.schema import UserAchieved
from domain.room.schema import RoomResponseSchema, RoomSchema
from domain.state.schema import GameStateSchema


class CreateGameCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: Any, room: Room
    ) -> GameSchema:
        game_crud = GameCRUD()
        game = GameSchema(
            seats={},
            deck=[],
            round=None,
            status=GameStatus.STARTED,
            beats=[],
            is_first_round=True,
        )
        await game_crud.create(game, room.id)
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game_crud = GameCRUD()
        await game_crud.delete(room.id)
        return game

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        room_schema = TypeAdapter(RoomSchema).validate_python(room)
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=RoomResponseSchema(command="room", room=room_schema).model_dump(
                mode="json"
            ),
        )

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError


class GameReadyCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.status = GameStatus.READY
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.status = GameStatus.STARTED
        return game

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message={},
        )

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError


class GameStartCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.status = GameStatus.STARTED
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.status = GameStatus.READY
        return game

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message={},
        )

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError


class GameEndCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        active_user_count: int = 0
        for _, seat in game.seats.items():
            if seat.user.achieved == UserAchieved.PROCESSING:
                active_user_count += 1
        match active_user_count:
            case 1:
                game.status = GameStatus.FINISHED
            case _:
                pass
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.status = GameStatus.READY
        return game

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message={},
        )

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError
