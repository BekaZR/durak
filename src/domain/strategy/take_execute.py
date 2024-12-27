from db.models.room import Room
from domain.command.card.command import AddUserCardTableCommand
from domain.command.card.schema import CardSchema
from domain.command.game.schema import GameSchema
from domain.command.round.exception import RoundNotExistError
from domain.command.user.exception import UserNotFound
from domain.controller.base import GameController
from domain.state.schema import GameStateSchema
from domain.strategy.base import GameStrategy


class TakeExecuteStrategy(GameStrategy):
    """
    WARNING: request.user required!!!
    """

    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if game.round is None:
            raise RoundNotExistError()
        if request.user is None:
            raise UserNotFound()

        all_cards_table: list[CardSchema] = []
        for slot_schema in game.round.slots:
            all_cards_table.append(slot_schema.attacker_card)
            if not slot_schema.enemy_card:
                continue
            all_cards_table.append(slot_schema.enemy_card)
        request.cards = all_cards_table

        await AddUserCardTableCommand().execute(request=request, game=game, room=room)
        return await GameController().switch(request=request, game=game, room=room)
