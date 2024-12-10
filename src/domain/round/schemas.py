from pydantic import Field
from domain.round.enum import RoundEnum
from domain.slot.schema import SlotOutSchema
from schemas.base import BaseSchema


class RoundSchema(BaseSchema):
    slots: list[SlotOutSchema]
    status: RoundEnum
    slot: int | None = Field(default=None)
