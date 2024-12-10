from typing import Literal

from schemas.base import BaseSchema

from domain.card.schema import CardSchema
from domain.user.schema import BaseUserSchema


class AttackRequestSchema(BaseSchema):
    command: Literal["attack"]
    user: BaseUserSchema
    card: CardSchema
