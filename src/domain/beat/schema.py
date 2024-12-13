from typing import Literal

from domain.schema import BaseRequestSchema


class BeatRequestSchema(BaseRequestSchema):
    command: Literal["beat"]
