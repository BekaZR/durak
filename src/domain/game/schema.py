from typing import Literal
from pydantic import Field
from domain.card.schema import CardSchema
from domain.game.enums import GameStatus
from domain.seat.schema import SeatSchema
from domain.turn.schema import TurnSchema
from domain.user.types import UserID
from schemas.base import BaseSchema
from domain.round.schemas import RoundSchema


class GameSchema(BaseSchema):
    seats: dict[UserID, SeatSchema]
    round: RoundSchema | None = Field(default=None)
    deck: list[CardSchema]
    turn: TurnSchema | None = Field(default=None)
    trump: CardSchema | None = Field(default=None)
    status: GameStatus


class GameSwitchReadySchema(BaseSchema):
    command: Literal["switch_ready"]
