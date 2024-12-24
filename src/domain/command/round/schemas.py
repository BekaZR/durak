from domain.command.round.enum import RoundEnum
from domain.command.slot.schema import SlotOutSchema
from schemas.base import BaseSchema


class RoundSchema(BaseSchema):
    slots: list[SlotOutSchema]
    status: RoundEnum
    is_finalized: bool = False
