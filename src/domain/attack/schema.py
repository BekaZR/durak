from typing import Literal

from domain.schema import BaseRequestSchema

from domain.card.schema import CardSchema


class AttackRequestSchema(BaseRequestSchema):
    command: Literal["attack"]
    card: CardSchema
