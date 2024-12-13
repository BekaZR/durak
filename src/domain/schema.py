from schemas.base import BaseSchema

from domain.user.schema import BaseUserSchema


class BaseRequestSchema(BaseSchema):
    user: BaseUserSchema
