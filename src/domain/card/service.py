import random
from typing import Literal

from domain.card.schema import CardSchema


class CardService:
    @classmethod
    def create_deck(cls, deck_size: int) -> list[CardSchema]:
        ranks: list[str] = [
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "J",
            "Q",
            "K",
            "A",
        ]
        suits: list[Literal["hearts", "diamonds", "clubs", "spades"]] = [
            "hearts",
            "diamonds",
            "clubs",
            "spades",
        ]

        if deck_size == 24:
            ranks = ranks[7:]  # Используем карты от 9 до A
        elif deck_size == 36:
            ranks = ranks[4:]  # Используем карты от 6 до A
        elif deck_size == 52:
            pass  # Используем все карты

        # deck = [{"rank": rank, "suit": suit} for rank in ranks for suit in suits]
        deck = [CardSchema(rank=rank, suit=suit) for rank in ranks for suit in suits]
        random.shuffle(deck)
        return deck
    
    @staticmethod
    def rank_value(rank: str) -> int:
        rank_order = {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "J": 11,
            "Q": 12,
            "K": 13,
            "A": 14,
        }
        return rank_order.get(rank, 0)
