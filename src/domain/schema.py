from schemas.base import BaseSchema

from domain.command.user.schema import BaseUserSchema


class BaseRequestSchema(BaseSchema):
    user: BaseUserSchema
