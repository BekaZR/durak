from typing import Literal

from pydantic import field_validator

from domain.seat.exception import SeatPositionException
from schemas.base import BaseSchema

from domain.user.schema import BaseUserSchema


class JoinRequestSchema(BaseSchema):
    command: Literal["join"]
    user: BaseUserSchema
    position: int

    @field_validator("position")
    def check_position(cls, position: int) -> int:
        if position < 0 or position > 6:
            raise SeatPositionException
        return position
