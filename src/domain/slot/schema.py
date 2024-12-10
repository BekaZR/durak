from schemas.base import BaseSchema
from pydantic import Field

from domain.card.schema import CardSchema
from domain.user.schema import BaseUserSchema


class SlotOutSchema(BaseSchema):
    attacker: BaseUserSchema | None = Field(default=None)
    attacker_card: CardSchema | None = Field(default=None)
    enemy: BaseUserSchema | None = Field(default=None)
    enemy_card: CardSchema | None = Field(default=None)
    status: bool
