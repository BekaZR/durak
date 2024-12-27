import random
from typing import Literal, Optional

from domain.command.card.schema import CardSchema
from domain.command.game.schema import GameSchema
from domain.command.turn.exception import TrumpNotExistsException
from domain.command.user.exception import UserNotFound
from domain.command.user.schema import UserAchieved
from domain.command.user.types import UserID
from domain.command.round.exception import RoundNotExistError
from domain.command.user.exception import UserAlreadyWinError
from domain.command.card.exception import CardNotInHandError, CardNotInTableError
from domain.command.slot.exception import CantBeatError


class CardService:
    def get_ranks(self) -> list[str]:
        return [
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
        allowed_ranks.update(
            {slot.enemy_card.rank for slot in game.round.slots if slot.enemy_card}
        )
        if card.rank not in allowed_ranks:
            raise CardNotInTableError()
        return None

    def is_higher(
        self, attacker_card: CardSchema, enemy_card: CardSchema, trump_card: CardSchema
    ) -> None:
        ranks = self.get_ranks()
        if attacker_card.suit == enemy_card.suit:
            if not ranks.index(enemy_card.rank) > ranks.index(attacker_card.rank):
                raise CantBeatError()
        if enemy_card.suit == trump_card.suit and attacker_card.suit != trump_card.suit:
            return None
            raise CantBeatError()

    def can_beat_validate(
        self,
        attacking_card: CardSchema,
        defending_card: CardSchema,
        trump_card: CardSchema,
    ) -> None:
        if defending_card.suit == attacking_card.suit:
            self.is_higher(defending_card, attacking_card, trump_card)
            return None
        if defending_card.suit == trump_card.suit:
            return None
        raise CantBeatError()

    async def find_lowest_card_player(self, game: GameSchema) -> Optional[UserID]:
        """
        Find the player with the lowest trump card, or if no trump cards,
        the lowest card overall.

        Args:
            game: Current game state containing player cards and trump suit

        Returns:
            Optional[UserID]: ID of player with lowest card, or None if no valid cards found

        Raises:
            TrumpNotExistsException: If trump card is not set in the game
        """
        if not game.trump:
            raise TrumpNotExistsException()

        lowest_trump_rank: Optional[str] = None
        lowest_non_trump_rank: Optional[str] = None
        lowest_trump_user_id: Optional[UserID] = None
        lowest_non_trump_user_id: Optional[UserID] = None

        # First pass - look for trump cards
        for user_id, seat in game.seats.items():
            if not seat.user.cards:  # Skip players without cards
                continue
            if seat.user.achieved != UserAchieved.PROCESSING:
                continue

            for card in seat.user.cards:
                current_rank_value = CardService.rank_value(card.rank)

                if card.suit == game.trump.suit:
                    # Handle trump cards
                    if (
                        lowest_trump_rank is None
                        or current_rank_value
                        < CardService.rank_value(lowest_trump_rank)
                    ):
                        lowest_trump_rank = card.rank
                        lowest_trump_user_id = user_id
                else:
                    # Handle non-trump cards
                    if (
                        lowest_non_trump_rank is None
                        or current_rank_value
                        < CardService.rank_value(lowest_non_trump_rank)
                    ):
                        lowest_non_trump_rank = card.rank
                        lowest_non_trump_user_id = user_id

        # Return trump card holder if exists, otherwise non-trump card holder
        return (
            lowest_trump_user_id
            if lowest_trump_user_id is not None
            else lowest_non_trump_user_id
        )

    async def get_all_cards_in_table(self, game: GameSchema) -> list[CardSchema]:
        if game.round is None:
            raise RoundNotExistError()
        cards: list[CardSchema] = []
        for slot in game.round.slots:
            cards.append(slot.attacker_card)
            if not slot.enemy_card:
                continue
            cards.append(slot.enemy_card)
        return cards
