from typing import Literal

from schemas.base import BaseSchema

from domain.user.schema import BaseUserSchema


class BeatRequestSchema(BaseSchema):
    command: Literal["beat"]
    user: BaseUserSchema
