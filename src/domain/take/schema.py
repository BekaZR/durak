from typing import Literal

from schemas.base import BaseSchema

from domain.user.schema import BaseUserSchema


class TakeRequestSchema(BaseSchema):
    command: Literal["take"]
    user: BaseUserSchema
