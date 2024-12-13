from typing import Literal

from domain.schema import BaseRequestSchema

from domain.user.schema import BaseUserSchema


class TakeRequestSchema(BaseRequestSchema):
    command: Literal["take"]
    user: BaseUserSchema
