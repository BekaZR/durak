import asyncio
from db.enums.room import CardTransferPermission
from db.models.room import Room
from domain.command.card.command import (
    RemoveUserCardCommand,
)
from domain.command.defence.schema import DefenceRequestSchema
from domain.command.game.schema import GameSchema
from domain.command.round.exception import RoundNotExistError
from domain.command.turn.command import (
    CreateAllPlayersTurnCommand,
    CreateNeighborsTurnCommand,
)
from domain.controller.base import GameController
from domain.state.round import DefenceRoundEndState
from domain.state.schema import GameStateSchema
from domain.state.slot import DefenceNewCardInTableState
from domain.strategy.base import GameStrategy
from domain.strategy.beat_execute import BeatExecuteStrategy
from domain.strategy.round import RoundCreateStrategy, RoundEndStrategy
from exception.support import RequestNotSupportedError
from domain.command.defence.command import DefenceCommand


class DefenceStrategy(GameStrategy):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if request.request is None or not isinstance(
            request.request, DefenceRequestSchema
        ):
            raise RequestNotSupportedError()
        if not game.round:
            raise RoundNotExistError()
        await DefenceCommand().execute(request=request, game=game, room=room)
        await RemoveUserCardCommand().execute(request=request, game=game, room=room)
        await DefenceNewCardInTableState().execute(
            request=request, game=game, room=room
        )

        if request.update_turn:
            match room.card_transfer_permission:
                case CardTransferPermission.NEIGHBORS_ONLY:
                    await CreateNeighborsTurnCommand().execute(
                        request=request, game=game, room=room
                    )
                case CardTransferPermission.ALL_PLAYERS:
                    await CreateAllPlayersTurnCommand().execute(
                        request=request, game=game, room=room
                    )
            request.update_turn = False
        await DefenceRoundEndState().execute(request=request, game=game, room=room)

        if game.round.is_finalized:
            await BeatExecuteStrategy().execute(request=request, game=game, room=room)
            await RoundEndStrategy().execute(request=request, game=game, room=room)
            await RoundCreateStrategy().execute(request=request, game=game, room=room)

            return game

        request.next_strategy = DefenceStrategy()
        asyncio.create_task(
            GameController().switch_delay(request=request, game=game, room=room)
        )
        request.current_command = self
        return await GameController().switch(request=request, game=game, room=room)
