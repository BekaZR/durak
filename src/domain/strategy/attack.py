from db.enums.room import CardTransferPermission
import asyncio
from db.models.room import Room
from domain.command.attack.command import AttackCommand
from domain.command.attack.schema import AttackRequestSchema
from domain.command.card.command import (
    RemoveUserCardCommand,
)
from domain.command.game.enums import GameStatus
from domain.command.game.schema import GameSchema
from domain.command.round.enum import RoundEnum
from domain.command.round.exception import RoundNotExistError
from domain.command.turn.command import (
    CreateAllPlayersTurnCommand,
    CreateNeighborsTurnCommand,
)
from domain.controller.base import GameController
from domain.state.schema import GameStateSchema
from domain.strategy.base import GameStrategy
from domain.strategy.beat_execute import BeatExecuteStrategy
from domain.strategy.ready import ReadyStrategy
from domain.strategy.take_execute import TakeExecuteStrategy
from domain.strategy.win import UserWinStrategy
from exception.support import RequestNotSupportedError
from domain.strategy.game import GameEndStrategy
from domain.state.game import GameEndState
from domain.state.round import RoundEndState
from domain.strategy.game import GameStartExecuteClassicStrategy
from domain.strategy.round import RoundCreateStrategy, RoundEndStrategy


class AttackStrategyClassic(GameStrategy):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if request.request is None or not isinstance(
            request.request, AttackRequestSchema
        ):
            raise RequestNotSupportedError()

        if game.round is None:
            raise RoundNotExistError()

        await AttackCommand().execute(request=request, game=game, room=room)
        await RemoveUserCardCommand().execute(request=request, game=game, room=room)
        # check round is end
        await RoundEndState().execute(request=request, game=game, room=room)

        # if round is end
        if game.round.is_finalized:
            # and enemy take card
            if game.round.status == RoundEnum.TAKE:
                # enemy must be take cards
                await TakeExecuteStrategy().execute(
                    request=request, game=game, room=room
                )
            else:
                # cards must be move to beat
                await BeatExecuteStrategy().execute(
                    request=request, game=game, room=room
                )
            await RoundEndStrategy().execute(request=request, game=game, room=room)
            await RoundCreateStrategy().execute(request=request, game=game, room=room)
            return game

        user_cards = game.seats[request.request.user.user_id].user.cards

        if not user_cards and not game.deck:
            request.user = request.request.user
            await UserWinStrategy().execute(request=request, game=game, room=room)

        # game end
        await GameEndState().execute(request=request, game=game, room=room)

        if game.status == GameStatus.FINISHED:
            request.seats = game.seats
            request.next_strategy = GameEndStrategy
            await GameController().switch(request=request, game=game, room=room)
            request.next_strategy = GameStartExecuteClassicStrategy
            await GameController().switch(request=request, game=game, room=room)
            request.next_strategy = ReadyStrategy
            await GameController().switch(request=request, game=game, room=room)
            return game

        match room.card_transfer_permission:
            case CardTransferPermission.NEIGHBORS_ONLY:
                await CreateNeighborsTurnCommand().execute(
                    request=request, game=game, room=room
                )
            case CardTransferPermission.ALL_PLAYERS:
                await CreateAllPlayersTurnCommand().execute(
                    request=request, game=game, room=room
                )
        asyncio.create_task(
            GameController().switch_delay(request=request, game=game, room=room)
        )
        request.current_command = self
        return await GameController().switch(request=request, game=game, room=room)
