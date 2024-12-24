import random
from typing import Literal, Optional

from domain.command.card.exception import TrumpNotExist
from domain.command.card.schema import CardSchema
from domain.command.game.schema import GameSchema
from domain.command.slot.schema import SlotOutSchema
from domain.command.user.exception import UserNotFound
from domain.command.user.schema import BaseUserSchema, UserAchieved
from domain.command.user.types import UserID
from domain.command.round.exception import RoundNotExistError
from domain.command.user.exception import UserAlreadyWinError
from domain.command.card.exception import CardNotInHandError, CardNotInTableError
from domain.command.slot.exception import CantBeatError


class CardService:
    def get_ranks(self) -> list[str]:
        return ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A",]

    def get_suits(self) -> list[Literal["hearts", "diamonds", "clubs", "spades"]]:
        return [
            "hearts",
            "diamonds",
            "clubs",
            "spades",
        ]

    def create_deck(self, deck_size: int) -> list[CardSchema]:
        ranks: list[str] = self.get_ranks()
        suits: list[Literal["hearts", "diamonds", "clubs", "spades"]] = self.get_suits()

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

    def attack_with_card_validate(
        self,
        game: GameSchema,
        user_id: UserID,
        card: CardSchema,
    ) -> None:
        """
        Validate if a player can attack with a specific card.

        Args:
            game: Current game state
            user_id: ID of the attacking player
            card: Card to attack with

        Returns:
            bool: True if the attack is valid, False otherwise

        Raises:
            RoundNotExistError: If there's no active round
        """
        # Basic validations
        if not game.round:
            raise RoundNotExistError()

        # Player must be in game and active
        if user_id not in game.seats:
            raise UserNotFound()

        player = game.seats[user_id].user
        if player.achieved != UserAchieved.PROCESSING:
            raise UserAlreadyWinError()

        # Card must be in player's hand
        if card not in player.cards:
            raise CardNotInHandError()

        # If this is the first attack of the round
        if not game.round.slots:
            return None

        # For subsequent attacks in the round
        allowed_ranks = {
            slot.attacker_card.rank for slot in game.round.slots if slot.attacker_card
        }
        allowed_ranks.update({
            slot.enemy_card.rank for slot in game.round.slots if slot.enemy_card
        })
        if not card.rank in allowed_ranks:
            raise CardNotInTableError()
        return None


    def is_higher(self, attacker_card: CardSchema, enemy_card: CardSchema, trump_card: CardSchema) -> bool:
        ranks = self.get_ranks()
        if attacker_card.suit == enemy_card.suit:
            if not ranks.index(enemy_card.rank) > ranks.index(attacker_card.rank):
                raise CantBeatError()
        if enemy_card.suit == trump_card.suit and attacker_card.suit != trump_card.suit:
            return True
        return False

    def can_beat(self, attacking_card: CardSchema, defending_card: CardSchema, trump_card: CardSchema) -> bool:
        if defending_card.suit == attacking_card.suit:
            return self.is_higher(defending_card, attacking_card, trump_card)
        if defending_card.suit == trump_card.suit:
            return True
        return False
