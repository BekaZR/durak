from typing import Any
from core.manager import UserNotificationManager
from db.models.room import Room
from domain.attack.schema import AttackRequestSchema
from domain.card.service import CardService
from domain.command.base import Command

from domain.game.schema import GameSchema, GameSwitchReadySchema
from domain.user.schema import BaseUserSchema


class CreateDeckCardCommand(Command):
    async def execute(self, request: Any, game: GameSchema, room: Room) -> GameSchema:
        cards = CardService.create_deck(room.player_count)
        game.deck = cards
        return game

    async def rollback(self, request: Any, game: GameSchema, room: Room) -> GameSchema:
        game.deck = []
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


class RemoveUserCardCommand(Command):
    async def execute(
        self, request: AttackRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.seats[request.user.user_id].user.cards.remove(request.card)
        return game

    async def rollback(
        self, request: AttackRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if request.card not in game.seats[request.user.user_id].user.cards:
            game.seats[request.user.user_id].user.cards.append(request.card)
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
