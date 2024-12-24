from pydantic import field_validator
from domain.command.seat.exception import SeatPositionException
from domain.command.user.schema import UserOutSchema, UserSchema
from schemas.base import BaseSchema


class SeatSchema(BaseSchema):
    user: UserSchema
    position: int

    @field_validator("position")
    def check_position(cls, position: int) -> int:
        if position < 0 or position > 6:
            raise SeatPositionException
        return position


class SeatOutSchema(BaseSchema):
    user: UserOutSchema
    position: int

    @field_validator("position")
    def check_position(cls, position: int) -> int:
        if position < 0 or position > 6:
            raise SeatPositionException
        return position
