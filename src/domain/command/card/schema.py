from typing import Literal, Union

from schemas.base import BaseSchema


class CardSchema(BaseSchema):
    rank: str
    suit: Literal["hearts", "diamonds", "clubs", "spades"]


class CardOutSchema(BaseSchema):
    command: Literal["card"]
    action: Literal["remove", "add"]
    cards: Union[list[CardSchema], int]


class DeckOutSchema(BaseSchema):
    command: Literal["deck"]
    trump: CardSchema
    cards: int
