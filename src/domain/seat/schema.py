from pydantic import field_validator
from domain.seat.exception import SeatPositionException
from domain.user.schema import UserSchema
from schemas.base import BaseSchema


class SeatSchema(BaseSchema):
    user: UserSchema
    position: int

    @field_validator("position")
    def check_position(cls, position: int) -> int:
        if position < 0 or position > 6:
            raise SeatPositionException
        return position
