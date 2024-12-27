from typing_extensions import Optional
from db.models.room import Room
from domain.command.game.schema import GameSchema
from domain.command.ready.exception import UserAlreadyReadyError
from domain.state.schema import GameStateSchema
from domain.validate.base import BaseValidate
from exception.support import RequestNotSupportedError
from domain.command.ready.schema import ReadyRequestSchema


class DublicateReadyValidate(BaseValidate):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_in: Optional[ReadyRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, ReadyRequestSchema):
            raise RequestNotSupportedError()
        if game.seats[obj_in.user.user_id].user.is_ready:
            raise UserAlreadyReadyError()
