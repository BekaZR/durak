from typing_extensions import Optional
from db.models.room import Room
from domain.command.beat.exception import DefenderCannotBeatError
from domain.command.beat.schema import BeatRequestSchema
from domain.command.game.schema import GameSchema
from domain.command.round.exception import RoundInProgressError, RoundNotExistError
from domain.command.round.enum import RoundEnum
from domain.command.turn.exception import (
    NotYourTurnError,
    QueueIsBlankError,
    TurnNotExistError,
)
from domain.state.schema import GameStateSchema
from domain.validate.base import BaseValidate
from exception.support import RequestNotSupportedError


class UserNotEnemyValidate(BaseValidate):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_in: Optional[BeatRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, BeatRequestSchema):
            raise RequestNotSupportedError()
        if game.turn is None:
            raise TurnNotExistError()
        if obj_in.user.user_id == game.turn.current_defender_user_id:
            raise DefenderCannotBeatError()


class NotUserMoveValidate(BaseValidate):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_in: Optional[BeatRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, BeatRequestSchema):
            raise RequestNotSupportedError()
        if game.turn is None:
            raise TurnNotExistError()
        if not game.turn.queue:
            raise QueueIsBlankError()
        if obj_in.user.user_id != game.turn.queue[0]:
            raise NotYourTurnError()


class BeatPermissionValidate(BaseValidate):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        if game.turn is None:
            raise TurnNotExistError()
        if game.round is None:
            raise RoundNotExistError()
        if game.round.status == RoundEnum.PROCESSING:
            raise RoundInProgressError()
