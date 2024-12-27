from typing_extensions import Optional
from domain.command.card.service import CardService
from domain.command.defence.schema import DefenceRequestSchema
from domain.command.game.schema import GameSchema
from domain.state.base import GameState
from domain.state.schema import GameStateSchema
from db.models.room import Room
from domain.command.round.exception import RoundNotExistError
from exception.support import RequestNotSupportedError


class DefenceNewCardInTableState(GameState):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        obj_in: Optional[DefenceRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, DefenceRequestSchema):
            raise RequestNotSupportedError()
        if not game.round:
            raise RoundNotExistError()
        card_service = CardService()
        cards = await card_service.get_all_cards_in_table(game)
        if obj_in.card not in cards:
            request.update_turn = True
        return game
