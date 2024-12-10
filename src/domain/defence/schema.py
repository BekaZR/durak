from typing import Literal

from schemas.base import BaseSchema

from domain.card.schema import CardSchema
from domain.user.schema import BaseUserSchema


class DefenceRequestSchema(BaseSchema):
    command: Literal["defence"]
    user: BaseUserSchema
    card: CardSchema
    slot: int
