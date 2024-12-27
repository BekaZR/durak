from db.enums.room import CardTransferPermission
from db.models.room import Room
from domain.command.game.schema import GameSchema
from domain.command.round.command import RoundCreateCommand, RoundEndCommand
from domain.command.turn.command import (
    CreateAllPlayersTurnCommand,
    CreateNeighborsTurnCommand,
)
from domain.command.turn.exception import TurnNotExistError
from domain.state.schema import GameStateSchema
from domain.state.turn import SetNextAttackerState
from domain.strategy.base import GameStrategy


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
        if game.turn is None:
            raise TurnNotExistError()
        await RoundCreateCommand().execute(request=request, game=game, room=room)
        game.is_first_round = False

        await SetNextAttackerState().execute(request=request, game=game, room=room)

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
