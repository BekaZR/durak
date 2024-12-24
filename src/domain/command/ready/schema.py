from typing import Literal


from domain.schema import BaseRequestSchema


class ReadyRequestSchema(BaseRequestSchema):
    command: Literal["ready"]


class ReadyResponseSchema(ReadyRequestSchema):
    command: Literal["ready"]
    position: int
