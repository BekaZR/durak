from typing import Literal

from schemas.base import BaseSchema


class CardSchema(BaseSchema):
    rank: str
    suit: Literal["hearts", "diamonds", "clubs", "spades"]
