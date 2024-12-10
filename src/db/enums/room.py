from enum import IntEnum, StrEnum


class WalletType(StrEnum):
    """
    Defines the type of wallet used for betting in the game.
    Attributes:
    - BALANCE: Main balance wallet
    - BONUS_BALANCE: Bonus/promotional balance wallet
    - CLUB_BALANCE: Club-specific balance wallet
    """

    BALANCE = "BALANCE"
    BONUS_BALANCE = "BONUS_BALANCE"
    CLUB_BALANCE = "CLUB_BALANCE"


class CardTransferPermission(StrEnum):
    """
    Defines the rules for card transfers between players.
    Attributes:
    - NEIGHBORS_ONLY: Card transfers are allowed only between adjacent players
    - ALL_PLAYERS: Card transfers are allowed between any players at the table
    """

    NEIGHBORS_ONLY = "NEIGHBORS_ONLY"
    ALL_PLAYERS = "ALL_PLAYERS"


class RoomStatus(StrEnum):
    """
    Defines the current status of the game room.
    Attributes:
    - WAITING: Room is waiting for players to join
    - READY: All players are ready to start
    - IN_GAME: Game is currently in progress
    - FINISHED: Game has ended
    """

    WAITING = "WAITING"
    READY = "READY"
    IN_GAME = "IN_GAME"
    FINISHED = "FINISHED"


class DeckSize(IntEnum):
    """
    Sizes of card decks available for the game.

    Attributes:
        SMALL: 24 cards (9 to Ace).
        MEDIUM: 36 cards (6 to Ace).
        FULL: 52 cards (2 to Ace).
    """

    SMALL = 24
    MEDIUM = 36
    FULL = 52


class PlayerCount(IntEnum):
    """Available player counts for game rooms"""

    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
