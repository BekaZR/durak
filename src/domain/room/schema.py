from datetime import datetime
from typing import Literal
from db.enums.room import CardTransferPermission, DeckSize, PlayerCount, WalletType
from schemas.base import BaseSchema


class RoomCreateSchema(BaseSchema):
    bet_amount: int

    # Game Modes and Rules
    player_count: PlayerCount
    deck_size: DeckSize
    is_speed_mode: bool
    is_transfer_allowed: bool
    is_cheating_allowed: bool
    is_draw_allowed: bool
    card_transfer_permission: CardTransferPermission
    # Access Controls
    is_test: bool
    is_private: bool
    password: str

    # Game State
    balance_type: WalletType
    created_at: datetime


class RoomSchema(BaseSchema):
    id: int
    bet_amount: int

    # Game Modes and Rules
    player_count: PlayerCount
    deck_size: DeckSize
    is_speed_mode: bool
    is_transfer_allowed: bool
    is_cheating_allowed: bool
    is_draw_allowed: bool
    card_transfer_permission: CardTransferPermission
    # Access Controls
    is_test: bool
    is_private: bool
    password: str

    # Game State
    balance_type: WalletType
    created_at: datetime


class RoomResponseSchema(BaseSchema):
    command: Literal["room"]
    room: RoomSchema
