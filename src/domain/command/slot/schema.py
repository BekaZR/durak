from schemas.base import BaseSchema
from pydantic import Field

from domain.command.card.schema import CardSchema
from domain.command.user.schema import BaseUserSchema

# TODO: Remove None fields option
class SlotOutSchema(BaseSchema):
    attacker: BaseUserSchema
    attacker_card: CardSchema
    enemy: BaseUserSchema | None = Field(default=None)
    enemy_card: CardSchema | None = Field(default=None)
    status: bool = Field(default=False)
