from typing import Literal

from domain.schema import BaseRequestSchema


class TakeRequestSchema(BaseRequestSchema):
    command: Literal["take"]
