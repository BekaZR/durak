from domain.card.schema import CardSchema
from domain.seat.schema import SeatSchema
from schemas.base import BaseSchema
from domain.round.schemas import RoundSchema


class GameSchema(BaseSchema):
    seats: dict[int, SeatSchema]
    round: RoundSchema
    deck: list[CardSchema]
    turn: list[int]
    trump: CardSchema
