from datetime import datetime, timezone
from functools import partial

from sqlalchemy import Boolean, DateTime, Enum, Integer, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String

from db.base import Base
from db.enums.room import (
    CardTransferPermission,
    DeckSize,
    PlayerCount,
    RoomStatus,
    WalletType,
)


class Room(Base):
    __tablename__ = "room"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bet_amount: Mapped[int] = mapped_column(Integer, nullable=False)

    # Game Modes and Rules
    player_count: Mapped[PlayerCount] = mapped_column(
        Enum(PlayerCount, native_enum=True),
        nullable=False,
    )
    deck_size: Mapped[DeckSize] = mapped_column(
        Enum(DeckSize, native_enum=True),
        nullable=True,
    )
    is_speed_mode: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_transfer_allowed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_cheating_allowed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_draw_allowed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    card_transfer_permission: Mapped[CardTransferPermission] = mapped_column(
        Enum(CardTransferPermission, native_enum=True), nullable=False
    )

    # Access Controls
    is_test: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
    is_private: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
    password: Mapped[str] = mapped_column(String, nullable=True)

    # Game State
    trump_card: Mapped[str] = mapped_column(String, nullable=True)
    balance_type: Mapped[WalletType] = mapped_column(
        Enum(WalletType, native_enum=True), index=True
    )
    status: Mapped[RoomStatus] = mapped_column(
        Enum(RoomStatus, native_enum=True),
        nullable=False,
        default=RoomStatus.WAITING,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=partial(datetime.now, timezone.utc),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        index=True,
    )
