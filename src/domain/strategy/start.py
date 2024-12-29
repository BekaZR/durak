import asyncio
from db.enums.room import CardTransferPermission
from db.models.room import Room
from domain.command.card.command import (
    CreateDeckCardCommand,
    FindLowestCardPlayerCommand,
)
from domain.command.game.command import GameStartCommand
from domain.command.game.schema import GameSchema
from domain.command.round.command import RoundCreateCommand
from domain.command.turn.command import (
    CreateAllPlayersTurnCommand,
    CreateNeighborsTurnCommand,
)
from domain.controller.base import GameController
from domain.state.schema import GameStateSchema
from domain.strategy.base import GameStrategy
from domain.strategy.distribution import InitialDealStrategy
from domain.timer.attack import AttackTimer


class StartGameStrategy(GameStrategy):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        _ = await GameStartCommand().execute(request=request, game=game, room=room)
        _ = await CreateDeckCardCommand().execute(request=request, game=game, room=room)
        _ = await InitialDealStrategy().execute(request=request, game=game, room=room)
        _ = await RoundCreateCommand().execute(request=request, game=game, room=room)
        _ = await FindLowestCardPlayerCommand().execute(
            request=request, game=game, room=room
        )
        if room.card_transfer_permission == CardTransferPermission.NEIGHBORS_ONLY:
            await CreateNeighborsTurnCommand().execute(
                request=request, game=game, room=room
            )
        else:
            await CreateAllPlayersTurnCommand().execute(
                request=request, game=game, room=room
            )
        asyncio.create_task(
            AttackTimer().execute(request=request, game=game, room=room)
        )
        return await GameController().switch(request=request, game=game, room=room)
