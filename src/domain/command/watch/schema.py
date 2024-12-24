from typing import Literal

from domain.schema import BaseRequestSchema


class WatchRequestSchema(BaseRequestSchema):
    command: Literal["watch"]


class WatchResponseSchema(BaseRequestSchema):
    command: Literal["watch"]
