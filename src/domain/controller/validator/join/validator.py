from db.models.room import Room
from domain.controller.validator.base import ControllerValidator
from domain.controller.validator.join.exception import NotEveryoneJoin
from domain.command.game.enums import GameStatus
from domain.command.game.exception import GameCannotSwitchReady
from domain.command.game.schema import GameSchema
from domain.state.schema import GameStateSchema


class JoinToReadyStateValidator(ControllerValidator):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        if game.status != GameStatus.STARTED:
            raise GameCannotSwitchReady()


class JoinToReadyValidator(ControllerValidator):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        if len(game.seats) < room.player_count:
            raise NotEveryoneJoin()
