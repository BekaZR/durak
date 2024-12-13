from typing import Literal

from pydantic import field_validator

from domain.schema import BaseRequestSchema
from domain.seat.exception import SeatPositionException


class JoinRequestSchema(BaseRequestSchema):
    command: Literal["join"]
    position: int

    @field_validator("position")
    def check_position(cls, position: int) -> int:
        if position < 0 or position > 6:
            raise SeatPositionException
        return position
