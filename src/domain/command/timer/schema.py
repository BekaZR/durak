from datetime import datetime
from enum import StrEnum
from typing import Literal
from schemas.base import BaseSchema


class TimerStatus(StrEnum):
    ACTIVE = "ACTIVE"
    CANCELED = "CANCELED"


class TimerType(StrEnum):
    ATTACK = "ATTACK"
    TAKE = "TAKE"
    BEAT = "BEAT"


class TimerCreateSchema(BaseSchema):
    user_id: int
    created_at: datetime
    expired_at: datetime
    type: TimerType
    status: TimerStatus


class TimerResponseSchema(BaseSchema):
    command: Literal["create_timer"]
    timer: TimerCreateSchema
    position: int
