from db.models.room import Room
from domain.controller.validator.base import ControllerValidator
from domain.controller.validator.ready.exception import NotEveryoneReady
from domain.command.game.enums import GameStatus
from domain.command.game.exception import GameCannotSwitchStart
from domain.command.game.schema import GameSchema
from domain.state.schema import GameStateSchema


class ReadyToStartStateValidator(ControllerValidator):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        if game.status != GameStatus.READY:
            raise GameCannotSwitchStart()


class ReadyToStartValidator(ControllerValidator):
    async def validate(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        for _, player in game.seats.items():
            if not player.user.is_ready:
                raise NotEveryoneReady()
