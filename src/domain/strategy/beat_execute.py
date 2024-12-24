import asyncio
from db.models.room import Room
from domain.command.attack.command import AttackCommand
from domain.command.attack.schema import AttackRequestSchema
from domain.command.card.command import (
    RemoveUserCardCommand,
)
from domain.command.game.schema import GameSchema
from domain.command.round.enum import RoundEnum
from domain.command.round.exception import RoundNotExistError
from domain.command.slot.command import MaximumCommand
from domain.controller.base import GameController
from domain.state.schema import GameStateSchema
from domain.strategy.base import GameStrategy
from domain.strategy.defence import DefenceStrategy
from exception.support import RequestNotSupportedError
from domain.command.card.command import AddCardToBeatCommand

class BeatExecuteStrategy(GameStrategy):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        await AddCardToBeatCommand().execute(request=request, game=game, room=room)
        return game
