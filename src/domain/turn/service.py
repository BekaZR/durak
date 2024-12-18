from typing import Optional

from domain.card.schema import CardSchema
from domain.game.schema import GameSchema
from domain.seat.schema import SeatSchema
from domain.turn.exception import TrumpNotExistsException
from domain.turn.schema import TurnSchema
from domain.user.exception import AttackerNotFound, DefenderNotFound
from domain.user.schema import UserAchieved
from domain.user.types import UserID


class TurnService:
    @staticmethod
    def find_lowest_card_player(game: GameSchema) -> Optional[UserID]:
        """Find the player with the lowest card."""
        lowest_card: Optional[CardSchema] = None
        lowest_card_user_id: Optional[UserID] = None
        seats = game.seats
        if not game.trump:
            raise TrumpNotExistsException()
        for user_id, seat in seats.items():
            if not seat.user.cards:  # Skip players without cards
                continue

            for card in seat.user.cards:
                # Initialize if this is the first valid card
                if lowest_card is None:
                    lowest_card = card
                    lowest_card_user_id = user_id
                    continue

                # Compare current card with lowest card (considering trump)
                if (
                    (
                        card.suit != game.trump.suit
                        and lowest_card.suit == game.trump.suit
                    )
                    or (card.suit == lowest_card.suit and card.rank < lowest_card.rank)
                    or (
                        card.suit != game.trump.suit
                        and lowest_card.suit != game.trump.suit
                        and card.rank < lowest_card.rank
                    )
                ):
                    lowest_card = card
                    lowest_card_user_id = user_id

        return lowest_card_user_id

    @staticmethod
    def find_next_active_player(
        seats: dict[UserID, SeatSchema], current_position: int
    ) -> Optional[UserID]:
        """Find the next active player in clockwise direction."""
        max_position = max(seat.position for seat in seats.values())
        next_position = current_position + 1 if current_position < max_position else 0

        # Look through all positions until we find an active player or complete a full circle
        start_position = next_position
        while True:
            # Find seat with this position
            for user_id, seat in seats.items():
                if (
                    seat.position == next_position
                    and seat.user.achieved == UserAchieved.PROCESSING
                ):
                    return user_id

            next_position = next_position + 1 if next_position < max_position else 0
            if next_position == start_position:
                break

        return None

    @staticmethod
    def build_turn_queue(game: GameSchema) -> TurnSchema:
        """Build the turn queue based on game state."""
        # Find player with lowest card
        attacker_id = TurnService.find_lowest_card_player(game=game)
        if not attacker_id:
            raise AttackerNotFound()
        attacker_position = game.seats[attacker_id].position

        # Find next active player as defender
        defender_id = TurnService.find_next_active_player(game.seats, attacker_position)
        if not defender_id:
            raise DefenderNotFound()
        # Build queue of remaining active players in clockwise order
        queue: list[UserID] = []
        current_position = game.seats[defender_id].position

        while True:
            next_player_id = TurnService.find_next_active_player(
                game.seats, current_position
            )
            if not next_player_id or next_player_id == attacker_id:
                break

            queue.append(next_player_id)
            current_position = game.seats[next_player_id].position

        return TurnSchema(
            currenct_attacker_user_id=attacker_id,
            current_defender_user_id=defender_id,
            queue=queue,
        )

    @staticmethod
    def initialize_game_turn(game: GameSchema) -> GameSchema:
        """Initialize or update game turn."""
        # Create turn queue
        game.turn = TurnService.build_turn_queue(game)

        # Ensure all active players have cards
        for _, seat in game.seats.items():
            if seat.user.achieved == UserAchieved.PROCESSING and not seat.user.cards:
                # Deal cards to player (assuming 6 cards per player)
                cards_needed = 6 - len(seat.user.cards)
                if cards_needed > 0:
                    dealt_cards = game.deck[:cards_needed]
                    game.deck = game.deck[cards_needed:]
                    seat.user.cards.extend(dealt_cards)

        return game
