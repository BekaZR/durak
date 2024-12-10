from typing import Any
from db.models.room import Room
from domain.attack.schema import AttackRequestSchema
from domain.card.service import CardService
from domain.command.base import Command

from domain.game.schema import GameSchema


class CreateDeckCardCommand(Command):
    async def execute(self, request: Any, game: GameSchema, room: Room) -> GameSchema:
        cards = CardService.create_deck(room.player_count)
        game.deck = cards
        return game

    async def rollback(self, request: Any, game: GameSchema, room: Room) -> GameSchema:
        game.deck = []
        return game


class RemoveUserCardCommand(Command):
    async def execute(
        self, request: AttackRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.seats[request.user.user_id].user.cards.remove(request.card)
        return game

    async def rollback(
        self, request: AttackRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.deck = []
        return game


class AddUserCardCommand(Command):
    async def execute(
        self, request: AttackRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.seats[request.user.user_id].user.cards.remove(request.card)
        return game

    async def rollback(
        self, request: AttackRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.deck = []
        return game
