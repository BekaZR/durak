from typing import Literal


from domain.schema import BaseRequestSchema


class ReadyRequestSchema(BaseRequestSchema):
    command: Literal["ready"]


class ReadyResponseSchema(BaseRequestSchema):
    command: Literal["ready"]
    position: int
