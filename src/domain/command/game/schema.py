from pydantic import Field
from domain.command.card.schema import CardSchema
from domain.command.game.enums import GameStatus
from domain.command.seat.schema import SeatOutSchema, SeatSchema
from domain.command.turn.schema import TurnSchema
from domain.command.user.types import UserID
from schemas.base import BaseSchema
from domain.command.round.schemas import RoundSchema


class GameSchema(BaseSchema):
    seats: dict[UserID, SeatSchema]
    round: RoundSchema | None = Field(default=None)
    deck: list[CardSchema]
    beats: list[CardSchema]
    turn: TurnSchema | None = Field(default=None)
    trump: CardSchema | None = Field(default=None)
    status: GameStatus
    is_first_round: bool


class GameOutSchema(BaseSchema):
    seats: dict[UserID, SeatOutSchema]
    round: RoundSchema | None = Field(default=None)
    deck: list[CardSchema]
    turn: TurnSchema | None = Field(default=None)
    trump: CardSchema | None = Field(default=None)
    status: GameStatus
