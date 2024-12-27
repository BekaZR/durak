from typing import Any, Generic, Optional, TypeVar
from pydantic import Field
from domain.command.card.schema import CardSchema
from domain.command.seat.schema import SeatSchema
from domain.command.user.schema import BaseUserSchema
from domain.command.user.types import UserID
from domain.schema import BaseRequestSchema
from schemas.base import BaseSchema

TBaseSchema = TypeVar("TBaseSchema", bound=BaseRequestSchema)


class GameStateSchema(BaseSchema, Generic[TBaseSchema]):
    attacker: Optional[BaseUserSchema] = Field(default=None)
    enemy: Optional[BaseUserSchema] = Field(default=None)
    current_command: Optional[Any] = Field(default=None)  # Command
    current_strategy: Optional[Any] = Field(default=None)  # GameStrategy
    next_strategy: Optional[Any] = Field(default=None)  # GameStrategy

    request: Optional[TBaseSchema] = Field(default=None)
    response: Optional[TBaseSchema] = Field(default=None)

    user: Optional[BaseUserSchema] = Field(default=None)
    trump: Optional[CardSchema] = Field(default=None)
    cards: Optional[list[CardSchema]] = Field(default=None)

    seats: Optional[dict[UserID, SeatSchema]] = Field(default=None)

    update_turn: bool = Field(default=False)
