from datetime import datetime
from enum import StrEnum
from typing import Literal
from schemas.base import BaseSchema


class TimerStatus(StrEnum):
    ACTIVE = "ACTIVE"
    CANCELED = "CANCELED"


class TimerCreateSchema(BaseSchema):
    user_id: int
    created_at: datetime
    expired_at: datetime
    status: TimerStatus


class TimerResponseSchema(BaseSchema):
    command: Literal["create_timer"]
    user_id: int
    created_at: datetime
    expired_at: datetime
    status: TimerStatus
    position: int
