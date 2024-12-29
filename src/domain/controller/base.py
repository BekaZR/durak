from typing import TYPE_CHECKING
from db.models.room import Room
from domain.controller.service import ControllerService
from domain.controller.validator.join.validator import (
    JoinToReadyStateValidator,
    JoinToReadyValidator,
)
from domain.controller.validator.ready.validator import (
    ReadyToStartStateValidator,
    ReadyToStartValidator,
)
from domain.command.game.schema import GameSchema
from domain.state.schema import GameStateSchema

if TYPE_CHECKING:
    pass


class GameController:
    async def switch(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        controller_service = ControllerService()

        # Импортируем здесь для избежания циклических импортов
        from domain.strategy.join import JoinStrategy
        from domain.strategy.ready import ReadyStrategy, SwitchToReadyStrategy
        from domain.strategy.start import StartGameStrategy

        if isinstance(
            request.current_strategy, JoinStrategy
        ) and await controller_service.validate(
            request, game, room, [JoinToReadyStateValidator(), JoinToReadyValidator()]
        ):
            await SwitchToReadyStrategy().execute(request=request, game=game, room=room)
            return game

        if isinstance(
            request.current_strategy, ReadyStrategy
        ) and await controller_service.validate(
            request, game, room, [ReadyToStartStateValidator(), ReadyToStartValidator()]
        ):
            await StartGameStrategy().execute(request=request, game=game, room=room)
            return game

        if isinstance(
            request.current_strategy, StartGameStrategy
        ) and await controller_service.validate(request, game, room, []):
            return game
        return game
