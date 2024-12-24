from db.models.room import Room
from domain.command.game.schema import GameSchema
from domain.state.schema import GameStateSchema
from domain.strategy.base import GameStrategy
from domain.command.round.command import RoundCreateCommand, RoundEndCommand
from db.enums.room import CardTransferPermission
from domain.command.turn.command import CreateNeighborsTurnCommand, CreateAllPlayersTurnCommand


class RoundEndStrategy(GameStrategy):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        await RoundEndCommand().execute(request=request, game=game, room=room)
        return game


class RoundCreateStrategy(GameStrategy):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        await RoundCreateCommand().execute(request=request, game=game, room=room)
        match room.card_transfer_permission:
            case CardTransferPermission.NEIGHBORS_ONLY:
                await CreateNeighborsTurnCommand().execute(
                    request=request, game=game, room=room
                )
            case CardTransferPermission.ALL_PLAYERS:
                await CreateAllPlayersTurnCommand().execute(
                    request=request, game=game, room=room
                )
        return game
