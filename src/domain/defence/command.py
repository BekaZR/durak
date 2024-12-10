from db.models.room import Room
from domain.command.base import Command

from domain.defence.schema import DefenceRequestSchema
from domain.game.schema import GameSchema
from domain.slot.schema import SlotOutSchema


class DefenceCommand(Command):
    async def execute(
        self, request: DefenceRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.round.slots.append(
            SlotOutSchema(enemy=request.user, enemy_card=request.card, status=True)
        )
        return game

    async def rollback(
        self, request: DefenceRequestSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        raise NotImplementedError
