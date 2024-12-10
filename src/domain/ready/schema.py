from typing import Literal


from schemas.base import BaseSchema

from domain.user.schema import BaseUserSchema


class ReadyRequestSchema(BaseSchema):
    command: Literal["ready"]
    user: BaseUserSchema
