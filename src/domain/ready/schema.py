from typing import Literal


from domain.schema import BaseRequestSchema


class ReadyRequestSchema(BaseRequestSchema):
    command: Literal["ready"]
