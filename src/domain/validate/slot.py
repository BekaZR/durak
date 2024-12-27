from typing_extensions import Optional
from db.models.room import Room
from domain.command.card.exception import CardNotInHandError
from domain.command.defence.schema import DefenceRequestSchema
from domain.command.game.schema import GameSchema
from domain.command.round.exception import RoundNotExistError
from domain.state.schema import GameStateSchema
from domain.validate.base import BaseValidate
from exception.support import RequestNotSupportedError


class CardInHandValidate(BaseValidate):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        if game.round is None:
            raise RoundNotExistError()
        obj_in: Optional[DefenceRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, DefenceRequestSchema):
            raise RequestNotSupportedError()
        if obj_in.card not in game.seats[obj_in.user.user_id].user.cards:
            raise CardNotInHandError()
