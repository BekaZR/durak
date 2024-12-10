from enum import StrEnum

from pydantic import Field
from schemas.base import BaseSchema

from domain.card.schema import CardSchema


class BaseUserSchema(BaseSchema):
    user_id: int
    username: str


class UserConnect(StrEnum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"


class UserAchieved(StrEnum):
    WIN = "win"
    LOSE = "lose"
    PROCESSING = "processing"


class UserSchema(BaseSchema):
    user: BaseUserSchema
    cards: list[CardSchema]
    connect: UserConnect = Field(default=UserConnect.DISCONNECTED)
    achieved: UserAchieved = Field(default=UserAchieved.PROCESSING)
    is_ready: bool = False
