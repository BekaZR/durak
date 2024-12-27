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
from core.logger import service_logger


class StartGameStrategy(GameStrategy):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        await GameStartCommand().execute(request=request, game=game, room=room)
        await CreateDeckCardCommand().execute(request=request, game=game, room=room)
        service_logger.debug(f"deck: {game.deck}")
        await InitialDealStrategy().execute(request=request, game=game, room=room)
        service_logger.debug(f"dealing: {game.seats}")
        await RoundCreateCommand().execute(request=request, game=game, room=room)
        service_logger.debug(f"create round: {game.round}")
        await FindLowestCardPlayerCommand().execute(
            request=request, game=game, room=room
        )
        service_logger.debug(f"lower card: {request.user}")
        if room.card_transfer_permission == CardTransferPermission.NEIGHBORS_ONLY:
            await CreateNeighborsTurnCommand().execute(
                request=request, game=game, room=room
            )
        else:
            await CreateAllPlayersTurnCommand().execute(
                request=request, game=game, room=room
            )
        return await GameController().switch(request=request, game=game, room=room)
