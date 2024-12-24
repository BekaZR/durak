from typing import Literal

from domain.schema import BaseRequestSchema

from domain.command.card.schema import CardSchema


class DefenceRequestSchema(BaseRequestSchema):
    command: Literal["defence"]
    card: CardSchema
    slot: int


class DefenceResponseSchema(DefenceRequestSchema):
    command: Literal["defence"]
    card: CardSchema
    slot: int
    position: int
