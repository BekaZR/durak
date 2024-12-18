from db.models.room import Room
from domain.attack.schema import AttackRequestSchema
from domain.command.base import Command
from domain.game.schema import GameSchema
from domain.round.exception import RoundNotExistError
from domain.slot.schema import SlotOutSchema


class AttackCommand(Command):
    async def execute(self, request: AttackRequestSchema, game: GameSchema, room: Room) -> GameSchema:
        if not game.round:
            raise RoundNotExistError()
        game.round.slots.append(SlotOutSchema(attacker=request.user, attacker_card=request.card, status=False))
        return game

    async def rollback(self, request: AttackRequestSchema, game: GameSchema, room: Room) -> GameSchema:
        raise NotImplementedError
