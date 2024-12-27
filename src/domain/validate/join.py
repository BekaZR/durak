from typing_extensions import Optional
from db.models.room import Room
from domain.command.game.schema import GameSchema
from domain.command.join.exception import UserAlreadyJoinError
from domain.state.schema import GameStateSchema
from domain.validate.base import BaseValidate
from exception.support import RequestNotSupportedError
from domain.command.join.schema import JoinRequestSchema


class DublicateJoinValidate(BaseValidate):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_in: Optional[JoinRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, JoinRequestSchema):
            raise RequestNotSupportedError()
        if obj_in.user.user_id in game.seats:
            raise UserAlreadyJoinError()
