from typing import Optional
from db.models.room import Room
from domain.card.service import CardService
from domain.game.schema import GameSchema


class TurnService:
    async def _reorder_user_ids(
        self, user_ids: list[int], start_user_id: int
    ) -> list[int]:
        """Reorder user_ids to start from given user_id"""
        if not user_ids or start_user_id not in user_ids:
            return user_ids

        # Find index of start user_id
        start_idx = user_ids.index(start_user_id)
        # Reorder list to start from that user_id
        return user_ids[start_idx:] + user_ids[:start_idx]

    async def init_turn(self, game: GameSchema, room: Room) -> GameSchema:
        game.turn = list(game.seats.keys())
        return game

    async def remove_user_from_turn(self, game: GameSchema, room: Room) -> GameSchema:
        game.turn = game.turn[1:]
        return game

    async def restore_turn(self, game: GameSchema, room: Room) -> GameSchema:
        game.turn = list(game.seats.keys())
        return game

    async def remove_turn(self, game: GameSchema, room: Room) -> GameSchema:
        game.turn = []
        return game

arr = [
    [1, 2, 3],
    [1, 2, 3],
    [1, 2, 3],
    [1, 2, 3],
]
