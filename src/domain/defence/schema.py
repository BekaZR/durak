from typing import Literal

from domain.schema import BaseRequestSchema

from domain.card.schema import CardSchema


class DefenceRequestSchema(BaseRequestSchema):
    command: Literal["defence"]
    card: CardSchema
    slot: int
