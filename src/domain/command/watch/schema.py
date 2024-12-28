from typing import Literal

from domain.command.game.schema import GameOutSchema
from domain.command.timer.schema import TimerCreateSchema
from domain.schema import BaseRequestSchema


class WatchRequestSchema(BaseRequestSchema):
    command: Literal["watch"]


class WatchResponseSchema(BaseRequestSchema):
    command: Literal["watch"]
    game_state: GameOutSchema
    timers: list[TimerCreateSchema]
